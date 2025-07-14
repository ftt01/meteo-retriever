import sys

lib_dir = "/home/daniele/documents/github/ftt01/phd/share/lib"
sys.path.insert( 0, lib_dir )

from lib import *
import subprocess
import psycopg2
import random
import multiprocessing
import glob

meta = "/media/lacie2022/backup/bias_correction/applications/era5/postprocessed/grid_shifted.csv"

prec_file = "/media/lacie2022/backup/bias_correction/applications/era5/postprocessed/precipitation/20091231010000_20191231230000_merged.csv"
temp_file = "/media/lacie2022/backup/bias_correction/applications/era5/postprocessed/temperature/20100101000000_20191231230000_merged.csv"

import pandas as pd

metadata = pd.read_csv(meta, index_col=0)
precipitation_data = pd.read_csv(prec_file, index_col=0)
temperature_data = pd.read_csv(temp_file, index_col=0)

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
                # print(sql_insert)
                cur.execute(sql_insert)
                conn.commit()
                cur.execute(sql_select)
                c_id = int(cur.fetchall()[0][0])
    finally:
        conn.close()

    return c_id

def add_data( y, x, epsg, datetime_UTC, value, variable, um ):

    # print(point)

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
        ON CONFLICT DO NOTHING;'''.format(
            x=x,
            y=y,
            epsg=epsg,
            datetime=datetime_UTC, 
            value=value, 
            variable=variable,
            um=um
        )
    # print(sql_insert)
    
    conn = get_postgres_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql_insert)
            conn.commit()
    finally:
        conn.close()

for id in precipitation_data.columns:

    c_precipitation_data = precipitation_data[[id]]

    for datetime,value in c_precipitation_data.iterrows():

        # print(datetime)
        c_value = value[0] / 1000

        lat = metadata.loc[int(id)]['lat']
        lon = metadata.loc[int(id)]['lon']

        c_date = dt.datetime.strptime(
            datetime,
            "%Y-%m-%d %H:%M:%S")
        
        try:
            add_data( lat, lon, 4326, c_date, c_value, "tp", "m")
        except:
            print(f"NaN in ({lat},{lon}) for current date {c_date} in precipitation")
        

for id in temperature_data.columns:

    c_temperature_data = temperature_data[[id]]

    for datetime,value in c_temperature_data.iterrows():

        # print(datetime)
        c_value = value[0] + 273.15

        lat = metadata.loc[int(id)]['lat']
        lon = metadata.loc[int(id)]['lon']

        c_date = dt.datetime.strptime(
            datetime,
            "%Y-%m-%d %H:%M:%S")
        
        try:
            add_data( lat, lon, 4326, c_date, c_value, "2t", "K")
        except:
            print(f"NaN in ({lat},{lon}) for current date {c_date} in temperature")