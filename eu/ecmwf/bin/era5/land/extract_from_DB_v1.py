# %%
import sys

lib_dir = "/home/daniele/documents/github/ftt01/phd/share/lib"
sys.path.insert( 0, lib_dir )

from lib import *
import subprocess
import psycopg2
# import datetime as dt

# %%
class local_args():

    def __init__(self) -> None:
        pass

    def add_start_date(self,  start_date):
        self.start_date = start_date
    
    def add_end_date(self,  end_date):
        self.end_date = end_date

    def add_variable(self,  variable):
        self.variable = variable
    
    def add_meta_grid(self,  meta_grid):
        self.meta_grid = meta_grid

    def add_output_path(self,  output_path):
        self.output_path = output_path
        mkNestedDir( output_path )

# %%
try:
    input_parser = argparse.ArgumentParser()
    input_parser.add_argument('start_date', type=str)
    input_parser.add_argument('end_date', type=str)
    input_parser.add_argument('variable', type=str)
    input_parser.add_argument('output_path', type=str)
    input_parser.add_argument('meta_grid', type=str)
    args = input_parser.parse_args()
except:
    args = local_args()
    args.add_start_date("2014-08-02T00:00:00")
    args.add_end_date("2023-12-31T23:59:00")
    args.add_variable("2t")
    args.add_output_path("/media/windows/projects/hydro_data_driven/00_data/meteo/era5land/bias_correction/inputs/")
    args.add_meta_grid("/media/windows/projects/hydro_data_driven/00_data/meteo/era5land/bias_correction/inputs/AA2700buffer_wElevation.csv")

start_date = dt.datetime.strptime( args.start_date, '%Y-%m-%dT%H:%M:%S' )
end_date = dt.datetime.strptime( args.end_date, '%Y-%m-%dT%H:%M:%S' )
aggregation_at = '1H'
dates = pd.date_range(start_date, end_date, freq=aggregation_at)

def get_postgres_connection():

    db_name = 'meteo'
    db_user = 'postgres'
    db_password = 'postgres'
    db_host = '172.20.0.2'

    return psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host)

def get_point( y, x, epsg=4326, tolerance=0.01 ):

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
            cur.execute(sql_exist)
            rows = cur.fetchall()
            if rows[0][0] != 0:
                cur.execute(sql_select)
                c_id = int(cur.fetchall()[0][0])
            else:
                print("Not existing point!")
    finally:
        conn.close()

    return c_id

# %%
def sql_to_dataframe(conn, query, column_names):

    # print(query)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    # The execute returns a list of tuples:
    tuples_list = cursor.fetchall()
    cursor.close()
    # Now we need to transform the list into a pandas DataFrame:
    df = pd.DataFrame(tuples_list, columns=column_names)
    return df

# %%
full_df = pd.DataFrame(index=dates)
full_df.index.name = 'datetime'

# %%
sql_get_data_metadata_tp = '''
SELECT datetime,
    CASE
        WHEN EXTRACT(hour FROM datetime) = 1 THEN value
        ELSE (value - LAG(value) OVER (ORDER BY datetime))
    END AS value
FROM ecmwf.era5land_values
WHERE datetime >= '{start_datetime}' 
    AND datetime <= '{end_datetime}' 
    AND variable = '{variable}'
    AND point = {c_id}
GROUP BY datetime, value
ORDER BY datetime
'''

# %%
sql_get_data_geom_tp = '''
WITH inner_points AS (
    WITH poly AS (
        SELECT ST_Buffer(geom::geography, 2700)::geometry as geom
        FROM geometries.eu_ita_regions
        WHERE name = 'Trentino-Alto Adige'
    ),
    points AS (
        SELECT id, geom
        FROM ecmwf.era5land_points
    )
    SELECT points.id as id, points.geom
    FROM points, poly
    WHERE ST_Contains(poly.geom, points.geom)
)
SELECT point, datetime,
    CASE
        WHEN EXTRACT(hour FROM datetime) = 1 THEN value
        ELSE (value - LAG(value) OVER (ORDER BY datetime))
    END AS value
FROM ecmwf.era5land_values, inner_points
WHERE datetime >= '{start_datetime}' 
    AND datetime <= '{end_datetime}' 
    AND variable = '{variable}'
    AND point = inner_points.id
GROUP BY point, datetime, value
ORDER BY point, datetime
'''

# %%
sql_get_data_metadata_2t = '''
SELECT datetime, value 
FROM ecmwf.era5land_values
WHERE datetime >= '{start_datetime}' 
    AND datetime <= '{end_datetime}' 
    AND variable = '{variable}'
    AND point = {c_id}
ORDER BY datetime
'''

# %%
sql_get_data_geom_2t = '''
WITH inner_points AS (
    WITH poly AS (
        SELECT ST_Buffer(geom::geography, 2700)::geometry as geom
        FROM geometries.eu_ita_regions
        WHERE name = 'Trentino-Alto Adige'
    ),
    points AS (
        SELECT id, geom
        FROM ecmwf.era5land_points
    )
    SELECT points.id as id, points.geom
    FROM points, poly
    WHERE ST_Contains(poly.geom, points.geom)
)
SELECT point, datetime, value
FROM ecmwf.era5land_values, inner_points
WHERE datetime >= '{start_datetime}' 
    AND datetime <= '{end_datetime}' 
    AND variable = '{variable}'
    AND point = inner_points.id
GROUP BY point, datetime, value
ORDER BY point, datetime
'''

def extract_lines(l, start_date, end_date, var, aggregation_at):

    print(f"Extracting: {l}")

    splitted = l.split(',')
    old_id = int(splitted[0])
    lat = float(splitted[1])
    lon = float(splitted[2])

    c_id = get_point(lat,lon)

    if var == 'tp':
        sql_get_data = sql_get_data_metadata_tp.format(
                start_datetime = (start_date-dt.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M'),
                end_datetime = end_date.strftime('%Y-%m-%d %H:%M'),
                variable = var,
                c_id = c_id
            )
    elif var == '2t':
        sql_get_data = sql_get_data_metadata_2t.format(
                start_datetime = start_date.strftime('%Y-%m-%d %H:%M'),
                end_datetime = end_date.strftime('%Y-%m-%d %H:%M'),
                variable = var,
                c_id = c_id
            )
    c_df = sql_to_dataframe( get_postgres_connection(), sql_get_data, column_names = ['datetime', 'value'])
    c_df.set_index('datetime', inplace=True)
    ### put the old_id or the c_id in the columns of full_df
    c_df.rename(columns={'value':old_id}, inplace=True)
    
    ## precipitation
    if var == 'tp':
        c_df = resample_timeseries( 
            c_df, res_type='sum', 
            step=aggregation_at, offset=False )
        # from meters to mm
        c_df = c_df * 1000
        c_df = c_df[start_date:end_date]
    ## temperature
    elif var == '2t':
        c_df = resample_timeseries( 
            c_df, res_type='mean', 
            step=aggregation_at, offset=False )
        # from Kelvin to Celsius
        c_df = c_df - 273.15
    
    return c_df

# %%
try:
    with open(args.meta_grid, 'r') as ff:
        lines = ff.readlines()[1:]
        ff.close()

    import multiprocessing

    with multiprocessing.Pool(1) as pool:
        # Use starmap to pass multiple arguments to the function
        c_dfs = pool.starmap(extract_lines, [(l, start_date, end_date, args.variable, aggregation_at) for l in lines])
    
    full_df = pd.concat([full_df] + c_dfs, axis=1, join='inner')

except:
    print("No metadata file, using DB IDs")

    if args.variable == 'tp':
        sql_get_data = sql_get_data_geom_tp.format(
                start_datetime = (start_date-dt.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M'),
                end_datetime = end_date.strftime('%Y-%m-%d %H:%M'),
                variable = args.variable
            )
    elif args.variable == '2t':
        sql_get_data = sql_get_data_geom_2t.format(
                start_datetime = start_date.strftime('%Y-%m-%d %H:%M'),
                end_datetime = end_date.strftime('%Y-%m-%d %H:%M'),
                variable = args.variable
            )
    c_full_df = sql_to_dataframe( get_postgres_connection(), sql_get_data, column_names = ['point', 'datetime', 'value'])

    points = pd.unique(c_full_df['point'])
    print('N. of points: ' + str(len(points)))
    for c_id in points:
        c_df = c_full_df[ c_full_df['point']==c_id ]

        c_df = c_df[['datetime','value']]
        c_df.set_index('datetime', inplace=True)
        ### put the old_id or the c_id in the columns of full_df
        c_df.rename(columns={'value':c_id}, inplace=True)
        
        ## precipitation
        if args.variable == 'tp':
            c_df = resample_timeseries( 
                c_df, res_type='sum', 
                step=aggregation_at, offset=True )
            # from meters to mm
            c_df = c_df * 1000
            c_df = c_df[start_date:end_date]
        ## temperature
        elif args.variable == '2t':
            c_df = resample_timeseries( 
                c_df, res_type='mean', 
                step=aggregation_at, offset=True )
            # from Kelvin to Celsius
            c_df = c_df - 273.15

        full_df = pd.concat([full_df,c_df], axis=1, join='inner')

# %%
full_df = full_df.astype('float64').round(decimals=3)

# %%
# args.output_path + args.variable + '_' + start_date.strftime('%Y%m%dT%H%M%S') + '_' + end_date.strftime('%Y%m%dT%H%M%S') + '.csv'

# %%
full_df.to_csv( args.output_path + args.variable + '_' + start_date.strftime('%Y%m%dT%H%M%S') + '_' + end_date.strftime('%Y%m%dT%H%M%S') + '.csv' )

# %%
# #### CHECK INSTANT
# sql_get_data = '''
#             SELECT datetime, value*1000 as mm, point
# 	FROM ecmwf.era5land_values
# 	WHERE datetime >= '2010-01-01 00:00' AND datetime <= '2010-12-31 23:59' AND point = 18 AND variable ='tp'
#     '''

# c_df = sql_to_dataframe( get_postgres_connection(), sql_get_data, column_names = ['datetime', 'mm', 'point'])
# c_df['datetime'] = pd.to_datetime(c_df['datetime'])
# c_df.set_index('datetime',inplace=True)
# c_df['mm'] = [float(n) for n in c_df['mm'].values]

# inst = [ float(0) ]
# for el in c_df.index:
#     if el.hour == 1:
#         inst.append( c_df.loc[el]['mm'] )
#     else:
#         try:
#             inst.append( abs(c_df.loc[el]['mm'] - c_df.loc[el-dt.timedelta(hours=1)]['mm']) )
#         except:
#             print('Skipped first')

# c_df['inst'] = inst
# c_df.replace('Y').sum()

# %%
# #### EXTRACTION TEMPERATURE
# sql_2t_get_data = '''

# WITH instant_data as (
# 	WITH c_data as (
# 		SELECT datetime, value, point
# 		FROM ecmwf.era5land_values
# 		WHERE variable ='2t'
# 		ORDER BY point,datetime
# 	),
# 	inner_points AS (
# 		WITH poly AS (
# 			SELECT geom
# 			FROM geometries.pranav
# 			WHERE name = 'TAA_15km'
# 		),
# 		points AS (
# 			SELECT id, geom
# 			FROM ecmwf.era5land_points
# 		)
# 		SELECT points.id as id, points.geom
# 		FROM points, poly
# 		WHERE ST_Contains(poly.geom, points.geom)
# 	)
# 	SELECT c_data.value-273.15 AS celsius, 
# 		inner_points.id as id, inner_points.geom as geom, c_data.datetime as dt
# 	FROM c_data, inner_points
# 	WHERE inner_points.id = c_data.point
# 	GROUP BY c_data.value,inner_points.id,c_data.datetime,inner_points.geom
# 	ORDER BY inner_points.id,c_data.datetime
# )
# SELECT EXTRACT(year FROM instant_data.dt) AS year, ROUND(AVG(instant_data.celsius),2) AS yearly_mean,
# 	instant_data.id as point, ST_X(instant_data.geom) AS lon, ST_Y(instant_data.geom) AS lat
# FROM instant_data 
# GROUP BY year,point,geom
# ORDER BY point;

# '''
# temp_df = sql_to_dataframe( get_postgres_connection(), sql_2t_get_data, column_names = ['year', 'yearly_mean', 'point', 'lon', 'lat'])
# temp_df.to_csv("/media/windows/projects/kriging/era5landland/temperature_yearly_means.csv")

# %%
# #### EXTRACTION PRECIPITATION
# sql_tp_get_data = '''

# WITH instant_data as (
# 	WITH c_data as (
# 		SELECT datetime, value, point
# 		FROM ecmwf.era5land_values
# 		WHERE variable ='tp'
# 	-- 		AND datetime >= '2010-01-01 00:00' AND datetime <= '2010-12-31 23:59'
# -- 		GROUP BY datetime, value
# 		ORDER BY point,datetime
# 	),
# 	inner_points AS (
# 		WITH poly AS (
# -- 			SELECT ST_Buffer(geom,1000) as geom
# -- 			FROM geometries.eu_ita_regions
# -- 			WHERE name = 'Trentino-Alto Adige'
# 			SELECT geom
# 			FROM geometries.pranav
# 			WHERE name = 'TAA_15km'
# 		),
# 		points AS (
# 			SELECT id, geom
# 			FROM ecmwf.era5land_points
# 		)
# 		SELECT points.id as id, points.geom
# 		FROM points, poly
# 		WHERE ST_Contains(poly.geom, points.geom)
# 	)
# 	SELECT 
# 		CASE
# 			WHEN 
# -- 				EXTRACT(hour FROM c_data.datetime) <
# -- 				EXTRACT(hour FROM LAG(c_data.datetime) OVER (ORDER BY inner_points.id,c_data.datetime))
# 				EXTRACT(hour FROM c_data.datetime) = 1
# 			THEN c_data.value*1000
# 			ELSE (c_data.value*1000 - LAG(c_data.value*1000) OVER (ORDER BY inner_points.id,c_data.datetime))
# 		END AS instant, 
# 		inner_points.id as id, inner_points.geom as geom, c_data.datetime as dt
# 	FROM c_data, inner_points
# 	WHERE inner_points.id = c_data.point
# 	GROUP BY c_data.value,inner_points.id,c_data.datetime,inner_points.geom
# 	ORDER BY inner_points.id,c_data.datetime
# )
# SELECT EXTRACT(year FROM instant_data.dt) AS year, ROUND(SUM(instant_data.instant),2) AS yearly_mean,
# 	instant_data.id as point, ST_X(instant_data.geom) AS lon, ST_Y(instant_data.geom) AS lat
# FROM instant_data 
# WHERE instant_data.instant >= 0
# GROUP BY year,point,geom
# ORDER BY point;

# '''

# prec_df = sql_to_dataframe( get_postgres_connection(), sql_tp_get_data, column_names = ['year', 'yearly_mean', 'point', 'lon', 'lat'])
# prec_df.to_csv("/media/windows/projects/kriging/era5landland/precipitation_yearly_sums.csv")

# %%
# sql_a_muzzo = '''WITH inner_points AS (
#     WITH poly AS (
#         SELECT ST_Buffer(geom::geography, 5000)::geometry as geom
#         FROM geometries.eu_ita_regions
#         WHERE name = 'Trentino-Alto Adige'
#     ),
#     points AS (
#         SELECT id, geom
#         FROM ecmwf.era5land_points
#     )
#     SELECT points.id as id, points.geom
#     FROM points, poly
#     WHERE ST_Contains(poly.geom, points.geom)
# )
# SELECT inner_points.id, ST_X(inner_points.geom) as lon, ST_Y(inner_points.geom) as lat
# FROM inner_points'''

# c_df = sql_to_dataframe( get_postgres_connection(), sql_a_muzzo, column_names = ['id', 'lon', 'lat'])
# c_df.set_index('id', inplace=True)
# c_df.to_csv("/media/windows/projects/bias_correction/applications/era5land/data/pre_processed/grid.csv")


