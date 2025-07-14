#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys

lib_dir = "/home/daniele/documents/github/ftt01/phd/share/lib"
sys.path.insert( 0, lib_dir )

from lib import *
import subprocess
import psycopg2
import multiprocessing


# In[ ]:


class Input():
    def add_start_date(self, start_date):
        self.start_date = start_date
    def add_end_date(self, end_date):
        self.end_date = end_date
    def add_file(self, file):
        self.file = file
    def add_variable(self, variable):
        self.variable = variable

input_parser = argparse.ArgumentParser()
input_parser.add_argument('-s','--start_date', type=str, nargs='?', default="2010-01-01T00:00:00")
input_parser.add_argument('-e','--end_date', type=str, nargs='?', default="2022-12-31T23:00:00")
input_parser.add_argument('-f','--file', type=str, nargs='?', default=None)
input_parser.add_argument('-v','--variables', type=list, nargs='?', default=['tp','2t'])
args = input_parser.parse_args()

input_path = "/media/lacie2022/data/meteo/ecmwf/era5/original/ensemble/t2m/"
# tmp_path = "/media/lacie2022/data/meteo/ecmwf/era5/original/ensemble/tmp/"
# mkNestedDir( tmp_path )

if args.file == None:
    args.files = [os.path.basename(el) for el in glob.glob(input_path + "*.grib")]
else:
    args.files = [args.file]


# In[ ]:


start_date = dt.datetime.strptime( args.start_date, '%Y-%m-%dT%H:%M:%S' )
end_date = dt.datetime.strptime( args.end_date, '%Y-%m-%dT%H:%M:%S' )
dates = pd.date_range(start_date, end_date, freq='3H')


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
        FROM ecmwf.era5_ens_points
        WHERE ST_Contains(
            ST_Transform(
                ST_MakeEnvelope({min_lon}, {min_lat}, {max_lon}, {max_lat}, {epsg}), 4326 ),
            era5_ens_points.geom)
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
        INSERT INTO ecmwf.era5_ens_points(geom)
        VALUES ( ST_SetSRID(ST_MakePoint({x},{y}),{epsg}) )
        ON CONFLICT DO NOTHING;'''.format(
            x=x,
            y=y,
            epsg=epsg
    )

    sql_select = '''
        SELECT ecmwf.era5_ens_points.id
        FROM ecmwf.era5_ens_points
        ORDER BY ecmwf.era5_ens_points.geom <#> ST_SetSRID(ST_MakePoint({x},{y}),{epsg})
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
        INSERT INTO ecmwf.era5_ens_values(
	        datetime, value, point, variable, um)
	    VALUES ('{datetime}'::timestamp, ARRAY{value},
            (
                SELECT ecmwf.era5_ens_points.id
                FROM ecmwf.era5_ens_points
                ORDER BY ST_Distance(ST_SetSRID(ST_MakePoint({x},{y}),{epsg}), ecmwf.era5_ens_points.geom)
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


# def load_on_db( date, var_meta, n_points:int, c_file ):

#     c_ens_df = pd.read_csv(c_file, nrows=n_points, sep='\s+')
#     c_ens_df = c_ens_df.rename(columns={'Value':1})
#     ens = 2

#     for i in range((n_points+1),(n_points+1)*10,(n_points+1)):
#         c_df = pd.read_csv(c_file, skiprows=i, nrows=n_points, sep='\s+')
#         c_ens_df[ens] = c_df['Value'].values
#         ens = ens + 1
    
#     c_ens_df = c_ens_df.set_index(['Latitude','Longitude'])

#     for idx in c_ens_df.index:

#         lat = idx[0]
#         lon = idx[1]
#         c_id = add_point( lat, lon, epsg=4326 )
#         add_data( lat, lon, 4326, date, list(c_ens_df.loc[idx].values), var_meta[0], var_meta[1] )


# In[ ]:


def execute(c_file):
    print('Processing: ' + str(c_file))

    if 'temperature' in c_file:
        variable = 't2m'
        um = 'K'

    elif 'precipitation' in c_file:
        variable = 'tp'
        um = 'm'

    try:
        c_df = xr.open_dataset(input_path+c_file, engine='cfgrib')
        date = c_df['time'].values + c_df['step'].values
        cc_df = c_df.to_dataframe()
        del c_df
        
        for idx in cc_df.index:
            lat = idx[0]
            lon = idx[1]
            c_id = add_point( lat, lon, epsg=4326 )
            add_data( lat, lon, 4326, date, list(cc_df.loc[lat,lon,:][variable].values), variable, um )
    except:
        print('Not extracted: ' + c_file)
        return None


# In[ ]:


# create a process pool that uses all cpus
n_cpus = multiprocessing.cpu_count()
with multiprocessing.Pool(processes=int(n_cpus*0.8)) as pool:
    pool.map(execute, args.files)
# close the process pool
pool.close()

