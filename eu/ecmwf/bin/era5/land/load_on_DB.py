#!/usr/bin/env python
# coding: utf-8

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

metadata = pd.read_csv("/media/windows/projects/hydro_data_driven/00_data/meteo/era5land/bias_correction/inputs/AA2700buffer_wElevation.csv")
# 
variable = "temperature"
data = pd.read_csv("/media/windows/projects/hydro_data_driven/00_data/meteo/era5land/bias_correction/outputs/hour_aggregation/hour_bias/dtr_t.csv")
bc_method = "dtr"
# 
# variable = "precipitation"
# data = pd.read_csv("/media/windows/projects/hydro_data_driven/00_data/meteo/era5land/bias_correction/outputs/hour_aggregation/hour_bias/MBCp_p.csv")
# bc_method = "MBCp"

start_date = dt.datetime.strptime( "2014-08-02T00:00:00", '%Y-%m-%dT%H:%M:%S' )
end_date = dt.datetime.strptime( "2023-12-31T23:00:00", '%Y-%m-%dT%H:%M:%S' )
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
        SELECT COUNT(*) FROM biascorrection.era5land_unbiased
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

def add_data( params ):

    point = params[0]
    datetime_UTC = params[1]
    value = params[2]
    variable = params[3]
    um = params[4]
    method = params[5]
    update = params[6]

    print(f"Loading on DB: {datetime_UTC}")

    if not(isinstance(value,float)):
        value = float(value[0])

    # print(point)
    if update == True:
        on_conflict = "(datetime, point, variable) DO UPDATE SET value = EXCLUDED.value, um = EXCLUDED.um"
    else:
        on_conflict = "DO NOTHING"

    sql_insert = '''
        INSERT INTO biascorrection.era5land_unbiased(
	        datetime, value, point, variable, um, method)
	    VALUES ('{datetime}'::timestamp, {value},
            {point}, '{variable}', '{um}', '{method}')
        ON CONFLICT {on_conflict};'''.format(
            datetime=datetime_UTC, 
            value=value,
            point=point,
            variable=variable,
            um=um,
            method=method,
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

def load_on_db( lat, lon, df, variable, um, method, update=True ):

    if variable == 'tp':
        df[df.columns[0]] = df.groupby(df.index.floor('D'))[df.columns[0]].cumsum().values
        df[df.columns[0]] = round(df[df.columns[0]]*0.001,6)
    elif variable == '2t':
        df[df.columns[0]] = round(df[df.columns[0]]+273.15,6)

    c_id = add_point( lat, lon, epsg=4326 )

    params = [
        [ c_id, date, df.loc[date][0], variable, um, method, update ] for date in df.index
    ]
        
    pool = multiprocessing.Pool()
    with multiprocessing.Pool(8) as pool:
        pool.map(add_data, params)
    # close the process pool
    pool.close() 

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
        SELECT COUNT(*) FROM biascorrection.era5land_unbiased
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
            print(f".. COMPLETE")
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

if variable == 'precipitation':
    variable = 'tp'
    um = 'm'
    var_n = '228'

elif variable == 'temperature':
    variable = '2t'
    um = 'K'
    var_n = '167'

for index, row in metadata.iterrows():
    id = str(int(row['ID']))
    lat = row['lat']
    lon = row['lon']

    df = pd.DataFrame(data[id].values, index=dates, columns=[id])

    load_on_db(lat, lon, df, variable, um, bc_method, True)