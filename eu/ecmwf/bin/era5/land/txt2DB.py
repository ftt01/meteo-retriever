#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import shutil
import os
import sys

from math import ceil

def remove_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
        print(f"Directory '{directory_path}' and all its contents have been removed.")
    else:
        print(f"Directory '{directory_path}' does not exist.")

lib_dir = "/home/daniele/documents/github/ftt01/phd/share/lib"
sys.path.insert( 0, lib_dir )

from lib import *
import subprocess
import psycopg2
import random
import multiprocessing
import glob

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
input_parser.add_argument('-i','--input_path', type=str, default='/media/lacie2022/data/meteo/ecmwf/era5/land/AA/')
input_parser.add_argument('-v','--variable', type=str, default='precipitation')
input_parser.add_argument('-y','--year', type=str, default='2000')

# input_parser = argparse.ArgumentParser()
# input_parser.add_argument('-s','--start_date', type=str, nargs='?', default="1990-01-01T00:00:00")
# input_parser.add_argument('-e','--end_date', type=str, nargs='?', default="2024-12-31T23:00:00")
# input_parser.add_argument('-f','--file', type=str, nargs='?', default="/media/lacie2022/data/meteo/ecmwf/era5/land/AA/update202405/2m_temperature_19900101.grib")
# input_parser.add_argument('-v','--variable', type=str, nargs='?', default='tp')
args = input_parser.parse_args()

start_date = f"{args.year}-01-01T00:00:00"
end_date = f"{int(args.year)+1}-01-01T00:00:00"

# args.input_path = "/media/lacie2022/data/meteo/ecmwf/era5/land/AA/update202405/"
if args.variable == "precipitation":
    variable = "tp"
    file_var = "total_precipitation"
elif args.variable == "temperature":
    variable = "2t"
    file_var = "2m_temperature"
else:
    raise Exception(f"Not a valid variable: {args.variable}")

start_date = dt.datetime.strptime( start_date, '%Y-%m-%dT%H:%M:%S' )
end_date = dt.datetime.strptime( end_date, '%Y-%m-%dT%H:%M:%S' )
dates = pd.date_range(start_date, end_date, freq='1H')

def get_postgres_connection():

    db_name = 'meteo'
    db_user = 'postgres'
    db_password = 'postgres'
    db_host = '172.20.0.2'

    return psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host)

def add_point( y, x, epsg=4326, tolerance=0.01 ):

    c_id = None

    sql_exist = '''
        SELECT COUNT(*)
        FROM ecmwf.era5land_points
        WHERE ST_Contains(
            ST_Transform(
                ST_MakeEnvelope({min_lon}, {min_lat}, {max_lon}, {max_lat}, {epsg}), 4326 ),
            era5land_points.geom)
        LIMIT 1;'''

    if not(isinstance(y,float)):
        y = float(y)

    if not(isinstance(x,float)):
        x = float(x)

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
        INSERT INTO ecmwf.era5land_points(geom)
        VALUES ( ST_SetSRID(ST_MakePoint({x},{y}),{epsg}) )
        ON CONFLICT DO NOTHING;'''.format(
            x=x,
            y=y,
            epsg=epsg
    )

    sql_select = '''
        SELECT ecmwf.era5land_points.id
        FROM ecmwf.era5land_points
        ORDER BY ecmwf.era5land_points.geom <#> ST_SetSRID(ST_MakePoint({x},{y}),{epsg})
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

def exist_data( datetime, variable ):

    datetime_plus24 = datetime + dt.timedelta(hours=24)

    sql_count = f'''
        WITH points AS (
            SELECT id, geom
            FROM ecmwf.era5land_points
            WHERE ST_Y(geom) >= 45.70 AND ST_Y(geom) <= 47.10 AND ST_X(geom) >= 10.40 AND ST_X(geom) <= 12.40
        )
        SELECT COUNT(*) FROM ecmwf.era5land_values
        WHERE point IN (SELECT id FROM points) 
        AND datetime >= '{datetime}' 
        AND datetime < '{datetime_plus24}'
        AND variable = '{variable}'
    '''
    # print(sql_count)
    
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql_count)
            res = int(cur.fetchall()[0][0])
    finally:
        conn.close()

    if res == 7560:
        return True
    else:
        return False

def add_data( y, x, epsg, datetime_UTC, value, variable, um, update=False ):

    if not(isinstance(value,float)):
        value = float(value[0])

    # print(point)
    if update == True:
        on_conflict = "(datetime, point, variable) DO UPDATE SET value = EXCLUDED.value, um = EXCLUDED.um"
    else:
        on_conflict = "DO NOTHING"

    sql_insert = '''
        INSERT INTO ecmwf.era5land_values(
	        datetime, value, point, variable, um)
	    VALUES ('{datetime}'::timestamp, {value},
            (
                SELECT ecmwf.era5land_points.id
                FROM ecmwf.era5land_points
                ORDER BY ST_Distance(ST_SetSRID(ST_MakePoint({x},{y}),{epsg}), ecmwf.era5land_points.geom)
                LIMIT 1
            ), '{variable}', '{um}')
        ON CONFLICT {on_conflict};'''.format(
            x=x,
            y=y,
            epsg=epsg,
            datetime=datetime_UTC, 
            value=value, 
            variable=variable,
            um=um,
            on_conflict=on_conflict
        )
    print(sql_insert)
    
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql_insert)
            conn.commit()
    except Exception as e:
        print(f"Not inserted: {e}")
    finally:
        conn.close()

def load_on_db( date, var_meta, n_points:int, filename, update=False ):

    print(f"Loading on DB: {date}")

    c_ens_df = pd.read_csv(filename, nrows=n_points, sep='\s+')
    c_ens_df = c_ens_df.rename(columns={'Value':1})

    c_ens_df.rename(columns={'Latitude,':'Latitude','Longitude,':'Longitude'}, inplace=True)
    
    c_ens_df = c_ens_df.set_index(['Latitude','Longitude'])
    
    for idx in c_ens_df.index:

        lat = idx[0]
        lon = idx[1]

        if (lat < 45.70) or (lat > 47.10):
            continue

        if (lon < 10.40) or (lon > 12.40):
            continue
     
        c_id = add_point( lat, lon, epsg=4326 )
        add_data( lat, lon, 4326, date, c_ens_df.loc[idx].values[0], var_meta[0], var_meta[1], update )

def execute(params):

    input_path = params[0]
    filename = params[1].split('.')[-2]
    model_varname = params[2]

    print(f"Input path: {input_path}")
    print(f"File name: {filename}")
    print(f"Model variable name: {model_varname}")

    # tmp_txt = dt.datetime.strftime(
    #     dt.datetime.now(),
    #     format="%Y%m%dT%H%M%S") + '_' + str(random.randint(1,100000)) + "_" + model_varname

    if model_varname == 'tp':
        variable = 'tp'
        um = 'm'
        var_n = '228'

    elif model_varname == '2t':
        variable = '2t'
        um = 'K'
        var_n = '167'

    ## load the meta
    df_meta = pd.read_csv('''{input_path}tmp/meta_{var}_{filename}.txt'''.format(
        input_path = input_path,
        var = model_varname,
        filename = filename), sep='\s+'
    )

    for idx in df_meta.index:
        try:
            ts = int(df_meta.loc[idx]['-1'])
        except:
            break

        # if ts < 22:
        #     continue

        c_date = dt.datetime.strptime(
            df_meta.loc[idx]['Date'] + 'T' + df_meta.loc[idx]['Time'],
            "%Y-%m-%dT%H:%M:%S")
        
        if not(c_date in dates):
            continue

        n_points = df_meta.loc[idx]['Gridsize']

        load_on_db( c_date, (variable, um), int(n_points), f'{input_path}tmp/{model_varname}_{filename}_{ts}.txt', update=True )

def check_data(params, days_window=30, missing=[]):

    date = params[0]
    variable = params[1]

    check_start_date = date
    if days_window == 0:
        check_end_date = date + dt.timedelta(days=1)
    else:
        check_end_date = date + dt.timedelta(days=days_window)
    
    if check_end_date.year > check_start_date.year:
        check_end_date = dt.datetime(check_end_date.year, 1, 1, 0, 0, 0)
        days_window = (check_end_date - check_start_date).days
    
    print(f"Check between {check_start_date} and {check_end_date}")

    sql_count = f'''
        WITH points AS (
            SELECT id, geom
            FROM ecmwf.era5land_points
            WHERE ST_Y(geom) >= 45.70 AND ST_Y(geom) <= 47.10 AND ST_X(geom) >= 10.40 AND ST_X(geom) <= 12.40
        )
        SELECT COUNT(*) FROM ecmwf.era5land_values
        WHERE point IN (SELECT id FROM points) 
        AND datetime >= '{check_start_date}' 
        AND datetime < '{check_end_date}'
        AND variable = '{variable}'
    '''
    # print(sql_count)
    
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql_count)
            res = int(cur.fetchall()[0][0])
    finally:
        conn.close()

    if days_window == 0:
        if res == 7560:
            print(f".. {date} COMPLETE")
            return (True,[])
        else:
            print(f"{date} incomplete by {res}/{7560}")
            if not(date in missing):
                missing.append(date)
            return (False,missing)       
        
    if res == 7560*days_window:
        print(f".. COMPLETE")
        return (True,[])
    else:
        print(f"..incomplete by {res}/{7560*days_window}")
        if days_window == 1:
            if len(missing) == 0:
                missing.append(date)
            return (False,missing)
        half_days_window = ceil(days_window/2)
        if half_days_window == 1:
            first_half_check = check_data((date,variable), days_window=0, missing=missing)
            second_half_check = check_data((date+dt.timedelta(days=1),variable), days_window=0, missing=missing)
            return (False,missing)
        elif half_days_window < 1:
            if not(date in missing):
                missing.append(date)
            return (False,missing)
        else:
            first_half_check = check_data((date,variable), days_window=half_days_window, missing=missing)
            second_half_check = check_data((date+dt.timedelta(days=half_days_window),variable), days_window=half_days_window, missing=missing)

        if (first_half_check[0] == True):
            if (second_half_check[0] == False):
                return (False,missing)
            else:
                return (True,missing)
        else:
            if (second_half_check[0] == False):
                return (False,missing)
            else:
                return (False,missing)

print(f"Variable: {variable}")
for date in pd.date_range(dates[0],dates[-1],freq='30D'):
    dates_to_do = check_data( (date,variable), missing=[] )

    if dates_to_do[0] == False:

        # c_dates = pd.date_range(dates_to_do[1][0],dates_to_do[1][1],freq='1D')

        params = [
                [f"{args.input_path}{args.variable}/{args.year}/todo/",
                f"{file_var}_{dt.datetime.strftime(d,'%Y%m%d')}.grib",
                variable] for d in dates_to_do[1]
        ]

        # create a process pool that uses all cpus
        pool = multiprocessing.Pool()
        with multiprocessing.Pool(1) as pool:
            pool.map(execute, params)
        # close the process pool
        pool.close()

    del dates_to_do