#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys

lib_dir = "/home/daniele/documents/github/ftt01/phd/share/lib"
sys.path.insert( 0, lib_dir )

from lib import *
import subprocess
import psycopg2
# import datetime as dt


# In[ ]:


input_parser = argparse.ArgumentParser()
input_parser.add_argument('start_date', type=str)
input_parser.add_argument('end_date', type=str)
input_parser.add_argument('file', type=str)
input_parser.add_argument('variable', type=str)
args = input_parser.parse_args()


# In[17]:


# start_date_str = "2010-01-01T00:00:00"
# end_date_str = "2019-12-31T23:00:00"
start_date_str = args.start_date + "T00:00:00"
end_date_str = args.end_date + "T23:00:00"
start_date = dt.datetime.strptime( start_date_str, '%Y-%m-%dT%H:%M:%S' )
end_date = dt.datetime.strptime( end_date_str, '%Y-%m-%dT%H:%M:%S' )
dates = pd.date_range(start_date, end_date, freq='d')


# In[ ]:


input_path = "/media/lacie2022/data/meteo/ecmwf/era5/land/"
output_path = "/media/windows/projects/bias_correction/applications/era5/postprocessed/"
mkNestedDir( output_path )

# variables = ['2t', 'tp']
             
# files = ['20102011.grib', '20122013.grib',
#          '20142015.grib', '20162017.grib',
#          '20182019.grib']

variables = []
variables.append(args.variable)

files = []
files.append(args.file)

tmp_txt = args.start_date + '_' + args.end_date + "_" + args.variable


# In[ ]:


def get_postgres_connection():

    db_name = 'meteo'
    db_user = 'postgres'
    db_password = 'pgAifa2Bias?'
    db_host = '172.20.0.2'

    return psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host)


# In[ ]:


def add_point( y, x, epsg=4326, tolerance=0.01 ):

    c_id = None

    sql_exist = '''
        SELECT COUNT(*)
        FROM ecmwf.era5_points
        WHERE ST_Contains(
            ST_Transform(
                ST_MakeEnvelope({min_lon}, {min_lat}, {max_lon}, {max_lat}, {epsg}), 4326 ),
            era5_points.geom)
        LIMIT 1;'''

    min_lat = y - tolerance
    max_lat = y + tolerance
    min_lon = x - tolerance
    max_lon = x + tolerance

    sql_exist = sql_exist.format(
        min_lat=min_lat,
        min_lon=min_lon,
        max_lat=max_lat,
        max_lon=max_lon,
        epsg=epsg
    )
    
    # print(sql_exist)

    sql_insert = '''
        INSERT INTO ecmwf.era5_points(geom)
        VALUES ( ST_SetSRID(ST_MakePoint({x},{y}),{epsg}) )
        ON CONFLICT DO NOTHING;'''.format(
            x=x,
            y=y,
            epsg=epsg
    )

    sql_select = '''
        SELECT ecmwf.era5_points.id
        FROM ecmwf.era5_points
        ORDER BY ecmwf.era5_points.geom <#> ST_SetSRID(ST_MakePoint({x},{y}),{epsg})
        LIMIT 1;'''.format(
            x=x,
            y=y,
            epsg=epsg
        )
    
    # print(sql_select)

    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            # print(sql_insert)
            # cur.execute(sql_insert)
            # conn.commit()

            # cur.execute(sql_select)
            # c_id = int(cur.fetchall()[0][0])
            cur.execute(sql_exist)
            rows = cur.fetchall()
            if rows[0][0] != 0:
                cur.execute(sql_select)
                c_id = int(cur.fetchall()[0][0])
            else:
                print(sql_insert)
                cur.execute(sql_insert)
                conn.commit()
                cur.execute(sql_select)
                c_id = int(cur.fetchall()[0][0])
    finally:
        conn.close()

    return c_id


# In[ ]:


def add_data( y, x, epsg, datetime_UTC, value, variable, um ):

    # print(point)

    sql_insert = '''
        INSERT INTO ecmwf.era5_values(
	        datetime, value, point, variable, um)
	    VALUES ('{datetime}'::timestamp, {value},
            (
                SELECT ecmwf.era5_points.id
                FROM ecmwf.era5_points
                ORDER BY ST_Distance(ST_SetSRID(ST_MakePoint({x},{y}),{epsg}), ecmwf.era5_points.geom)
                LIMIT 1
            ), '{variable}', '{um}')
        ON CONFLICT DO NOTHING;'''.format(
            x=x,
            y=y,
            epsg=epsg,
            datetime=datetime_UTC, 
            value=value, 
            variable=variable,
            um=um
        )
    print(sql_insert)
    
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql_insert)
            conn.commit()
    finally:
        conn.close()


# In[ ]:


def load_on_db( date, var_meta, c_file, start_hour=0 ):

    ## data from 00:00 to 01:00 is saved as data at 00:00 if i= -1 + start_hour
    i = 0 + start_hour

    ## read file and for each line add the point if it does not exist, then add the data to era5_values
    with open(c_file, 'r') as f:
        for line in f.readlines():
            try:
                l = line.split()
                # print(l)
                lat = round(float(l[0]),6)
                lon = round(float(l[1]),6)
                value = round(float(l[2]),6)
            except:
                i = i + 1
                continue
            
            datetime = '{date} {h}:00:00'.format(
                date=date.strftime( '%Y-%m-%d' ),
                h=str(i).zfill(2) 
            )
            c_id = add_point( lat, lon, epsg=4326 )
            add_data( lat, lon, 4326, datetime, 
                value, var_meta[0], var_meta[1] )
                    
        f.close()


# In[ ]:


try:
    os.remove( output_path + '{tmp_txt}.txt'.format(tmp_txt=tmp_txt) )
except:
    print( 'All clear!' )

for c_file in files:
    print('Processing: ' + str(c_file))
    first_value = True
    for model_varname in variables:
        for dd in dates:

            if first_value == True:
                ### if present save the first hour of the start_date (i.e., 2010-01-01 00:00:00)
                cmd = '''grib_get_data -w shortName={var},dataDate={YYYYmmdd},step=24 {input_path}{file_grib} >> {output_path}{tmp_txt}.txt'''.format(
                    var = model_varname,
                    YYYYmmdd = (dd - dt.timedelta(days=1)).strftime(format='%Y%m%d'),
                    # h = dd.hour,
                    file_grib = c_file,
                    input_path = input_path,
                    output_path = output_path,
                    tmp_txt=tmp_txt
                )

                print(cmd)
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()

                # print(process.returncode)
                
                if model_varname == 'tp':
                    variable = 'tp'
                    um = 'm'
                elif model_varname == '2t':
                    variable = '2t'
                    um = 'K'

                load_on_db( dd, (variable, um), output_path + '{tmp_txt}.txt'.format(tmp_txt=tmp_txt), start_hour=-1 )

                first_value = False

            else:
                dd = dd + dt.timedelta(hours=1)

                cmd = '''grib_get_data -w shortName={var},dataDate={YYYYmmdd} {input_path}{file_grib} >> {output_path}{tmp_txt}.txt'''.format(
                    var = model_varname,
                    YYYYmmdd = dd.strftime(format='%Y%m%d'),
                    # h = dd.hour,
                    file_grib = c_file,
                    input_path = input_path,
                    output_path = output_path,
                    tmp_txt=tmp_txt
                )

                print(cmd)
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()

                # print(process.returncode)
                
                if model_varname == 'tp':
                    variable = 'tp'
                    um = 'm'
                elif model_varname == '2t':
                    variable = '2t'
                    um = 'K'

                load_on_db( dd, (variable, um), output_path + '{tmp_txt}.txt'.format(tmp_txt=tmp_txt), start_hour=-1 )

                os.remove( output_path + '{tmp_txt}.txt'.format(tmp_txt=tmp_txt) )


# In[ ]:


grid_metadata = "/media/windows/projects/bias_correction/applications/era5/biasDownscaling/data/testcase01/grid.csv"


# In[ ]:




