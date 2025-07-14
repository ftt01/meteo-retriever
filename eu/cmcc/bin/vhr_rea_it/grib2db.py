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

input_path = "/media/lacie2022/data/meteo/cmcc/vhr_rea_it/"
# tmp_path = "/media/lacie2022/data/meteo/cmcc/vhr_rea_it/tmp/"
# mkNestedDir( tmp_path )

if args.file == None:
    args.files = [os.path.basename(el) for el in glob.glob(input_path + "*.nc")]
else:
    args.files = [args.file]


# In[ ]:


start_date = dt.datetime.strptime( args.start_date, '%Y-%m-%dT%H:%M:%S' )
end_date = dt.datetime.strptime( args.end_date, '%Y-%m-%dT%H:%M:%S' )
dates = pd.date_range(start_date, end_date, freq='1H')


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
        FROM cmcc.vhr_rea_it_points
        WHERE ST_Contains(
            ST_Transform(
                ST_MakeEnvelope({min_lon}, {min_lat}, {max_lon}, {max_lat}, {epsg}), 4326 ),
            vhr_rea_it_points.geom)
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
        INSERT INTO cmcc.vhr_rea_it_points(geom)
        VALUES ( ST_SetSRID(ST_MakePoint({x},{y}),{epsg}) )
        ON CONFLICT DO NOTHING;'''.format(
            x=x,
            y=y,
            epsg=epsg
    )

    sql_select = '''
        SELECT cmcc.vhr_rea_it_points.id
        FROM cmcc.vhr_rea_it_points
        ORDER BY cmcc.vhr_rea_it_points.geom <#> ST_SetSRID(ST_MakePoint({x},{y}),{epsg})
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
        INSERT INTO cmcc.vhr_rea_it_values(
	        datetime, value, point, variable, um)
	    VALUES ('{datetime}'::timestamp, {value},
            (
                SELECT cmcc.vhr_rea_it_points.id
                FROM cmcc.vhr_rea_it_points
                ORDER BY ST_Distance(ST_SetSRID(ST_MakePoint({x},{y}),{epsg}), cmcc.vhr_rea_it_points.geom)
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


def execute(arg):
    idx, row, variable, um = arg

    lat = row['lat']
    lon = row['lon']
    date = row['time']
    c_id = add_point( lat, lon, epsg=4326 )
    add_data( lat, lon, 4326, date, row[variable], variable, um )


# In[ ]:


for c_file in args.files:
    print('Processing: ' + str(c_file))

    c_df = xr.open_dataset(input_path+c_file)
    try:
        cc_df = c_df['T_2M'].to_dataframe()
        variable = 'T_2M'
        um = 'K'
    except KeyError as e:
        print(c_file + " has no temperature!")

        try:
            cc_df = c_df['TOT_PREC'].to_dataframe()
            variable = 'TOT_PREC'
            um = 'm'
        except KeyError as e:
            print(c_file + " has no precipitation!")
            continue
    
    try:
        cc_df.reset_index(inplace = True)

        # create a process pool that uses all cpus
        n_cpus = multiprocessing.cpu_count()
        with multiprocessing.Pool(processes=int(n_cpus*0.8)) as pool:
            pool.map(execute, [(idx,rows, variable, um) for idx,rows in cc_df.iterrows()])
        # close the process pool
        pool.close()
        
    except:
        print('Not extracted: ' + c_file)
        continue


# In[ ]:




