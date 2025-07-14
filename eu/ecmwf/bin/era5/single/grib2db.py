#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys

lib_dir = "/home/daniele/documents/github/ftt01/phd/share/lib"
sys.path.insert( 0, lib_dir )

from lib import *
import subprocess
import psycopg2


# In[ ]:


class Input():
    def add_start_date(self, start_date):
        self.start_date = start_date
    def add_end_date(self, end_date):
        self.end_date = end_date
    def add_files(self, files):
        self.files = files
    def add_variables(self, variables):
        self.variables = variables

input_parser = argparse.ArgumentParser()
input_parser.add_argument('start_date', type=str, nargs='?', default="1990-01-01T00:00:00")
input_parser.add_argument('end_date', type=str, nargs='?', default="2022-12-31T23:00:00")
input_parser.add_argument('files', type=list, nargs='?', default=[
    "1991-1992.grib",
    "2001-2002.grib",
    "2020.grib",
    "1993-1994.grib",
    "2003-2004.grib",
    "adaptor.mars.internal-1682269507.0764832-26888-6-391bb193-5ba5-403e-a882-ef8b710cb741.grib",
    "1995-1996.grib",
    "2005-2006.grib",
    "adaptor.mars.internal-1682273299.9890068-2454-15-2c5bdfd9-2d84-4efa-b656-f54c57c56c3f.grib",
    "1997-1998.grib",
    "2007-2008.grib"
    "1999-2000.grib",
    "2009.grib"])
input_parser.add_argument('variables', type=list, nargs='?', default=['tp','2t'])
args = input_parser.parse_args()

input_path = "/media/lacie2022/data/meteo/ecmwf/era5/original/reanalysis/"
tmp_path = "/media/lacie2022/data/meteo/ecmwf/era5/original/reanalysis/tmp/"
mkNestedDir( tmp_path )


# In[ ]:


start_date = dt.datetime.strptime( args.start_date, '%Y-%m-%dT%H:%M:%S' )
end_date = dt.datetime.strptime( args.end_date, '%Y-%m-%dT%H:%M:%S' )
dates = pd.date_range(start_date, end_date, freq='3H')


# In[ ]:





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
        FROM ecmwf.era5_land_points
        WHERE ST_Contains(
            ST_Transform(
                ST_MakeEnvelope({min_lon}, {min_lat}, {max_lon}, {max_lat}, {epsg}), 4326 ),
            era5_land_points.geom)
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
        INSERT INTO ecmwf.era5_land_points(geom)
        VALUES ( ST_SetSRID(ST_MakePoint({x},{y}),{epsg}) )
        ON CONFLICT DO NOTHING;'''.format(
            x=x,
            y=y,
            epsg=epsg
    )

    sql_select = '''
        SELECT ecmwf.era5_land_points.id
        FROM ecmwf.era5_land_points
        ORDER BY ecmwf.era5_land_points.geom <#> ST_SetSRID(ST_MakePoint({x},{y}),{epsg})
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


def add_data( y, x, epsg, datetime_UTC, values, variable, um ):

    # print(point)

    sql_insert = '''
        INSERT INTO ecmwf.era5_land_values(
	        datetime, value, point, variable, um)
	    VALUES ('{datetime}'::timestamp, ARRAY{value},
            (
                SELECT ecmwf.era5_land_points.id
                FROM ecmwf.era5_land_points
                ORDER BY ST_Distance(ST_SetSRID(ST_MakePoint({x},{y}),{epsg}), ecmwf.era5_land_points.geom)
                LIMIT 1
            ), '{variable}', '{um}')
        ON CONFLICT DO NOTHING;'''.format(
            x=x,
            y=y,
            epsg=epsg,
            datetime=datetime_UTC, 
            value=values, 
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


def load_on_db( date, var_meta, n_points:int, c_file ):

    c_ens_df = pd.read_csv(c_file, nrows=n_points, sep='\s+')
    c_ens_df = c_ens_df.rename(columns={'Value':1})
    ens = 2

    for i in range((n_points+1),(n_points+1)*10,(n_points+1)):
        c_df = pd.read_csv(c_file, skiprows=i, nrows=n_points, sep='\s+')
        c_ens_df[ens] = c_df['Value'].values
        ens = ens + 1
    
    c_ens_df = c_ens_df.set_index(['Latitude','Longitude'])

    for idx in c_ens_df.index:

        lat = idx[0]
        lon = idx[1]
        c_id = add_point( lat, lon, epsg=4326 )
        add_data( lat, lon, 4326, date, list(c_ens_df.loc[idx].values), var_meta[0], var_meta[1] )


# In[ ]:


try:
    os.remove( tmp_path + '{tmp_txt}.txt'.format(tmp_txt=tmp_txt) )
except:
    print( 'All clear!' )

for c_file in args.files:
    print('Processing: ' + str(c_file))
    for model_varname in args.variables:

        tmp_txt = dt.datetime.strftime(
            start_date,
            format="%Y%m%d") + '_' + dt.datetime.strftime(
                 end_date,
                 format="%Y%m%d") + "_" + model_varname

        if model_varname == 'tp':
            variable = 'tp'
            um = 'm'

        elif model_varname == '2t':
            variable = '2t'
            um = 'K'

        ## create a file for each variable
        pre_cmd = '''cdo -selname,{var} {input_path}{file_grib} {input_path}{var}_{file_grib}'''.format(
            var = model_varname,
            input_path = input_path,
            file_grib = c_file
        )
        print(pre_cmd)
        process = subprocess.Popen(pre_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        ## read the meta info in a table with cdo
        meta_cmd = '''cdo -info {input_path}{var}_{file_grib} > {tmp_path}meta.txt'''.format(
            var = model_varname,
            input_path = input_path,
            file_grib = c_file,
            tmp_path = tmp_path
        )
        print(meta_cmd)
        process = subprocess.Popen(pre_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        ## load the meta
        df_meta = pd.read_csv('''{tmp_path}meta.txt'''.format(
            tmp_path = tmp_path
            ), sep='\s+'
        )
        
        for idx in df_meta.index:
            try:
                ts = int(df_meta.loc[idx]['-1'])
            except:
                break

            c_date = dt.datetime.strptime(
                df_meta.loc[idx]['Date'] + 'T' + df_meta.loc[idx]['Time'],
                "%Y-%m-%dT%H:%M:%S")
            
            if not(c_date in dates):
                continue

            n_points = df_meta.loc[idx]['Gridsize']
        
            pre_cmd = '''cdo -seltimestep,{step} {input_path}{var}_{file_grib} {input_path}tmp_{idx}_{var}_{file_grib}'''.format(
                var = model_varname,
                step = ts,
                input_path = input_path,
                idx = idx,
                file_grib = c_file
            )
            print(pre_cmd)
            process = subprocess.Popen(pre_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
               
            cmd = '''grib_get_data {input_path}tmp_{idx}_{var}_{file_grib} >> {tmp_path}{tmp_txt}.txt'''.format(
                idx = idx,
                file_grib = c_file,
                input_path = input_path,
                tmp_path = tmp_path,
                tmp_txt=tmp_txt,
                var = model_varname
            )
            print(cmd)
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            load_on_db( c_date, (variable, um), int(n_points), tmp_path + '{tmp_txt}.txt'.format(tmp_txt=tmp_txt) )

            try:
                os.remove( tmp_path + '{tmp_txt}.txt'.format(tmp_txt=tmp_txt) )
                os.remove( '{input_path}tmp_{idx}_{var}_{file_grib}'''.format(
                    input_path = input_path,
                    idx = idx,
                    file_grib = c_file,
                    var = model_varname
                    )
                )
            except:
                continue

