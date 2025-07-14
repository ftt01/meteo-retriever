#!/usr/bin/env python
# coding: utf-8

import os
import sys

lib_dir = "/home/daniele/documents/github/ftt01/phd/share/lib"
sys.path.insert( 0, lib_dir )

from lib import *

import logging
from pathlib import Path

# input_parser = argparse.ArgumentParser()
# input_parser.add_argument('configuration_file', type=str)
# args = input_parser.parse_args()
# configuration_file = args.configuration_file

configuration_file = "/home/daniele/documents/github/ftt01/phd/projects/hydrological_forecasting/etc/conf/bias/input_taa.json"

def tranform_to_instant( current_df ):
    ### the df in input is a timeseries of N ensemble on the columns
    ### datetime,001,002,003,...,020

    for c in current_df.columns:
        values = current_df[c]
        
        val = []
        val.append( values[0] )
        for i in range(1, len(values)):
            val.append( round(values[i] - values[i-1],2) )
        
        current_df[c] = val
        del [val,values]
    
    return current_df

def load_on_db(variable, c_release, longitude, latitude, datetime, data):

    sql_insert = f'''
    INSERT INTO icon.metadata(name, variable, release)
        VALUES ('icon_d2_eps', '{variable}', '{c_release}')
        ON CONFLICT DO NOTHING;

    INSERT INTO icon.icon_d2_eps_grid(geom)
        VALUES (ST_Point({longitude}, {latitude}, 4326))
        ON CONFLICT DO NOTHING;

    WITH meta AS (
        SELECT id
        FROM icon.metadata
        WHERE name='icon_d2_eps' AND variable='{variable}' AND release='{c_release}'
    ),
    points AS (
        SELECT id, ST_Distance(geom, ST_Point({longitude}, {latitude}, 4326)) AS dist
        FROM icon.icon_d2_eps_grid
        ORDER BY dist
        LIMIT 1
    )
    INSERT INTO icon.icon_d2_eps_data(
    datetime, id_meta, id_grid, "001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015", "016", "017", "018", "019", "020")
    SELECT '{datetime}', meta.id, points.id, {data[0]},  {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]}, {data[6]}, {data[7]}, {data[8]}, {data[9]}, {data[10]}, {data[11]}, {data[12]}, {data[13]}, {data[14]}, {data[15]}, {data[16]}, {data[17]}, {data[18]}, {data[19]}
    FROM meta, points
    ON CONFLICT DO NOTHING
    '''

    query_meteo( sql_insert, "insert", logging=logging )

def extract_on_subbasins( 
    dir, df, variable, main_basin_name, rel_time, input_type,
    output_datetime_format='%Y-%m-%dT%H:%M:%SZ%z', input_timezone=pytz.timezone('UTC'), 
    subbasins=[], model_resolution=0.02, generate_meta=True):

    df.dropna(inplace=True)

    logging.info("Extraction of: " + variable)
    try:
        lats = pd.unique( df['lat'] )
        lons = pd.unique( df['lon'] )

        for el in subbasins:
            logging.info("Extraction on: " + el['name'])

            curr_lat_min = el['bbox']['lat_min']
            curr_lat_max = el['bbox']['lat_max']
            curr_lon_min = el['bbox']['lon_min']
            curr_lon_max = el['bbox']['lon_max']
            
            logging.info("BBOX with buffer: [{lat_min},{lon_min},{lat_max},{lon_max}]".format(
                lat_min=curr_lat_min,
                lon_min=curr_lon_min,
                lat_max=curr_lat_max,
                lon_max=curr_lon_max
            ))

            basin_lats = lats[ 
                (lats >= curr_lat_min) &
                (lats <= curr_lat_max)]
            basin_lons = lons[
                (lons >= curr_lon_min) &
                (lons <= curr_lon_max)]

            id = 1

            grid_ids = []
            grid_lons = []
            grid_lats = []

            for lat in basin_lats:
                for lon in basin_lons:
                    
                    current_df = df[(df['lat'] > lat-model_resolution/2) &
                                    (df['lat'] < lat+model_resolution/2) &
                                    (df['lon'] > lon-model_resolution/2) &
                                    (df['lon'] < lon+model_resolution/2)]
                    
                    if current_df.empty:
                        continue

                    if generate_meta == True:
                        grid_ids.append(id)
                        grid_lons.append(lon)
                        grid_lats.append(lat)

                    current_df.loc[:,'ens'] = [str(i).zfill(3) for i in current_df['band']]
                    current_df = current_df.drop(columns=['lat','lon','band'])
                    current_df.set_index( 'ens',inplace=True )
                    current_df = current_df.T
                    # current_df.set_index( [df.iloc[0], df.columns[0]],inplace=True )
                    
                    c_idx = pd.to_datetime(current_df.index, utc=True)
                    current_df.index = [ el.astimezone(input_timezone) for el in c_idx ]
                    current_df.index.name = "datetime"

                    current_df = current_df.sort_index(ascending=True)

                    if variable == 'precipitation':
                        current_df = tranform_to_instant( current_df )

                    for idx in current_df.index:

                        data = current_df.loc[idx].to_list()

                        load_on_db(variable, "R" + str( rel_time ).zfill(3), lon, lat, idx, data)

                    # output_file_path = dir + "{main_basin}/{subbasin}/{release_hour}/{variable}/{input_type}/{point_id}/".format(
                    #     main_basin = main_basin_name,
                    #     subbasin = el['key'],
                    #     release_hour = "R" + str( rel_time ).zfill(3),
                    #     variable = variable,
                    #     input_type = input_type,
                    #     point_id = str(id).zfill(3),
                    #     )
                    # mkNestedDir(output_file_path)

                    # output_file_name = output_file_path + dt.datetime.strftime( current_df.index[0], format='%Y%m%d' ) + ".csv" 
                    # current_df.index = [ dt.datetime.strftime( ix, output_datetime_format ) for ix in current_df.index ]
                    # current_df.index.name = "datetime"
                    # current_df.to_csv( output_file_name )

                    id = id + 1

            if generate_meta == True:
                meta_df = pd.DataFrame(index=grid_ids)
                meta_df["lon"] = grid_lons
                meta_df["lat"] = grid_lats

                metadata_filename = Path(output_file_path)
                meta_df.to_csv( str(metadata_filename.parent.absolute()) + "/grid.csv" )

            del current_df

        return 0
    
    except Exception as e:
        logging.info(f"Uncomplete {variable} with error: {e}")
        return 1

def extraction_call(file, type='rasterio'):

    if type == 'rasterio':

        ds = xr.open_dataset(file, engine="rasterio")
        # <xarray.Dataset>
        # Dimensions:           (ensemble0: 20, lat_0: 745, lon_0: 1214)
        # Coordinates:
        # * lat_0             (lat_0) float32 43.18 43.2 43.22 ... 58.02 58.04 58.06
        # * lon_0             (lon_0) float32 356.1 356.1 356.1 ... 380.3 380.3 380.3
        # * ensemble0         (ensemble0) int32 0 1 2 3 4 5 6 7 ... 13 14 15 16 17 18 19
        # Data variables:
        #     TMP_P1_L103_GLL0  (ensemble0, lat_0, lon_0) float32 ...
        #     ensemble0_info    (ensemble0) |S0 ...
        variable_mapped_meta = ds.variables.get(list(ds.keys())[0]).attrs
        # {
        # 'center': 'Offenbach (RSMC)',
        # 'production_status': 'Operational products',
        # 'long_name': 'Temperature',
        # 'units': 'K',
        # 'grid_type': 'Latitude/longitude',
        # 'parameter_discipline_and_category': 'Meteorological products, Temperature',
        # 'parameter_template_discipline_category_number': array([1, 0, 0, 0], dtype = int32),
        # 'level_type': 'Specified height level above ground (m)',
        # 'level': array([2.], dtype = float32),
        # 'forecast_time': array([60], dtype = int32),
        # 'forecast_time_units': 'minutes',
        # 'initial_time': '02/17/2021 (00:00)'
        # }
        current_datetime = dt.datetime.utcfromtimestamp(variable_mapped_meta['GRIB_VALID_TIME'])
        ds_red = ds.sel(y=slice(roi_bbox_lat_max,roi_bbox_lat_min),x=slice(roi_bbox_lon_min,roi_bbox_lon_max))

        lat_key = 'y'
        lon_key = 'x'
        ens_keyname = 'band'
    
    elif type == 'cfgrib':

        ds = xr.open_dataset(file, engine="cfgrib")
        variable_mapped_meta = ds.variables.get(list(ds.keys())[0]).attrs
        current_datetime = pd.Timestamp(ds.valid_time.values)
        logging.debug("Extracting file related to UTC datetime: " + str(current_datetime))
        ds_red = ds.sel(latitude=slice(roi_bbox_lat_min,roi_bbox_lat_max),longitude=slice(roi_bbox_lon_min,roi_bbox_lon_max))

        lat_key = 'latitude'
        lon_key = 'longitude'
        ens_keyname = 'number'
    
    variable_mapped_name = list(ds.keys())[0]
    del [ds]

    return current_datetime, ds_red, lat_key, lon_key, ens_keyname, variable_mapped_name


def extract_csv(files_to_convert, model_variables, logging, roi_bbox=[], implementation='local', input_path=None):

    roi_bbox_lat_min = roi_bbox[0]
    roi_bbox_lat_max = roi_bbox[1]
    
    roi_bbox_lon_min = roi_bbox[2]
    roi_bbox_lon_max = roi_bbox[3]

    if implementation=='local':

        t_2m_df = pd.DataFrame()
        tot_prec_df = pd.DataFrame()
        w_snow_df = pd.DataFrame()

        for file in files_to_convert:

            logging.debug("Converting to csv: " + file)
            try:
                logging.debug("Converting to csv using rasterio on: " + file)
                current_datetime, ds_red, lat_key, lon_key, ens_keyname, variable_mapped_name = extraction_call(file, type='rasterio')                
            except:
                logging.debug("Failed to convert to csv using rasterio on: " + file)
                logging.debug("Converting to csv using rasterio on: " + file)
                current_datetime, ds_red, lat_key, lon_key, ens_keyname, variable_mapped_name = extraction_call(file, type='cfgrib')
            
            df = ds_red.to_dataframe()
            del [ds_red]

            df.reset_index(inplace=True)

            if model_variables["temperature"] in file:
                variable = 'temperature'
                
                if t_2m_df.empty:

                    t_2m_df = df

                    # t_2m_df.insert(0, 'id', range(1, 1 + len(df)))

                    t_2m_df['lat'] = [round(idy,6) for idy in df[lat_key]]
                    t_2m_df['lon'] = [round(idx,6) for idx in df[lon_key]]

                    # t_2m_df.set_index(['lat','lon','band'], inplace=True)
                    
                    t_2m_df[current_datetime] = [round(idy,2) for idy in df[variable_mapped_name]]
                    t_2m_df = t_2m_df.loc[:, ['lat','lon',ens_keyname,current_datetime]]
                    t_2m_df = t_2m_df.rename(columns={ens_keyname:'band'})

                else:
                    t_2m_df[current_datetime] = [round(idy,2) for idy in df[variable_mapped_name]]
            
            elif model_variables["precipitation"] in file:
                variable = 'precipitation'
                
                if tot_prec_df.empty:

                    tot_prec_df = df

                    # tot_prec_df.insert(0, 'id', range(1, 1 + len(df)))

                    tot_prec_df['lat'] = [round(idy,6) for idy in tot_prec_df[lat_key]]
                    tot_prec_df['lon'] = [round(idx,6) for idx in tot_prec_df[lon_key]]

                    # tot_prec_df.set_index(['lat','lon','band'], inplace=True)
                    
                    tot_prec_df[current_datetime] = [round(idy,2) for idy in df[variable_mapped_name]]
                    tot_prec_df = tot_prec_df.loc[:, ['lat','lon',ens_keyname,current_datetime]]
                    tot_prec_df = tot_prec_df.rename(columns={ens_keyname:'band'})

                else:
                    tot_prec_df[current_datetime] = [round(idy,2) for idy in df[variable_mapped_name]]

            elif model_variables["snow"] in file:
                variable = 'snow'
               
                if w_snow_df.empty:

                    w_snow_df = df

                    # w_snow_df.insert(0, 'id', range(1, 1 + len(df)))

                    w_snow_df['lat'] = [round(idy,6) for idy in w_snow_df[lat_key]]
                    w_snow_df['lon'] = [round(idx,6) for idx in w_snow_df[lon_key]]

                    # w_snow_df.set_index(['lat','lon','band'], inplace=True)
                    
                    w_snow_df[current_datetime] = [round(idy,2) for idy in df[variable_mapped_name]]
                    w_snow_df = w_snow_df.loc[:, ['lat','lon',ens_keyname,current_datetime]]
                    w_snow_df = w_snow_df.rename(columns={ens_keyname:'band'})

                else:
                    w_snow_df[current_datetime] = [round(idy,2) for idy in df[variable_mapped_name]]
            else:
                raise KeyError
    
    ### if the local implementation does not work, use pynio in docker
    elif implementation == 'docker':

        ## run a docker on a list of files, the input_path and the output_pathnames
        # docker run --rm -v /media/windows/data/dwd/icon-d2-eps/extracted/extracted/20210222/:/mnt/data/ -it --entrypoint /bin/bash ftt01/pynio "regridded_icon-d2-eps_germany_icosahedral_single-level_2021022221_027_2d_w_snow.grib2" 47.6 45.5 11.2 10.2
        extractor_cmd = '''docker run --rm -v {c_data_path}:/mnt/data/ ftt01/pynio {lat_max} {lat_min} {lon_max} {lon_min}'''
        extractor_cmd = extractor_cmd.format(
            c_data_path = input_path,
            lat_max=roi_bbox_lat_max,
            lat_min=roi_bbox_lat_min,
            lon_max=roi_bbox_lon_max,
            lon_min=roi_bbox_lon_min
        )
        process = subprocess.Popen(extractor_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
        ## read the output_pathnames as CSV and return the dataframes
        t_2m_df = pd.read_csv(input_path+'temperature.csv')
        tot_prec_df = pd.read_csv(input_path+'precipitation.csv')
        w_snow_df = pd.read_csv(input_path+'snow.csv')
    
    return t_2m_df, tot_prec_df, w_snow_df


def move_to_output(input_dir, output_dir, move_keywords=[], mirror=False):

    mkNestedDir( output_dir )

    logging.info("Moving to {output_dir} using keywords: ".format(output_dir=output_dir) + str(move_keywords))

    if mirror == True:
        files_to_move = glob.glob( input_dir + "*.grib2")
        for k in move_keywords:
            files_to_move = list( set(files_to_move) - set(glob.glob( input_dir + "{kw}*.grib2".format(kw=k))) )
    else:
        files_to_move = []
        for k in move_keywords:
            files_to_move = files_to_move + list(set(glob.glob( input_dir + "{kw}*.grib2".format(kw=k))))

    if files_to_move != None:
        for f in files_to_move:
            logging.debug("Moving: " + f)
            try:
                shutil.move(f, output_dir + os.path.basename(f))
            except IOError as e:
                print("Unable to copy file. %s" % e)
            except:
                print("Unexpected error:", sys.exc_info())


def remove_unuseful_grib2( path_dir, keywords=[], mirror=False ):
    logging.info("Removing unuseful files in: " + path_dir)

    if mirror == True:
        files_to_remove = glob.glob( path_dir + "*.grib2")
        for k in keywords:
            files_to_remove = list( set(files_to_remove) - set(glob.glob( path_dir + "{kw}*.grib2".format(kw=k))) )
    else:
        files_to_remove = []
        for k in keywords:
            files_to_remove = files_to_remove + list(set(glob.glob( path_dir + "*{kw}*.grib2".format(kw=k))))

    if files_to_remove != None:
        for f in files_to_remove:
            logging.debug("Removing: " + f)
            os.remove( f )


computation_start = dt.datetime.now()

with open(configuration_file) as config_file:
    configuration = json.load(config_file)

    project_name = configuration["project_name"]

    provider_name = configuration["provider_name"]
    model_name = configuration["model"]["name"]
    model_ensemble = configuration["model"]["ensemble"]
    model_resolution = configuration["model"]["resolution"]
    model_releases = configuration["model"]["release"]
    model_variables = configuration["model"]["variables"]
    model_lead_hours = configuration["model"]["lead_hours"]
    model_timezone_str = configuration["model"]["timezone"]
    model_timezone = pytz.timezone(model_timezone_str)

    if model_ensemble != 1:
        input_type = "ensemble"
    else:
        input_type = "mean"
    
    input_path = configuration["input_path"]
    output_path = configuration["output"]["path"]
    mkNestedDir(output_path)
    
    output_datetime_format = configuration["output"]["datetime_format"]
    output_timezone_str = configuration["output"]["timezone"]
    output_timezone = pytz.timezone(output_timezone_str)
    output_types = configuration["output"]["type"]
    output_variables = configuration["output"]["variables"]
    output_extension = configuration["output"]["extension"]
    
    log_path = Path( configuration["log_path"] )
    mkNestedDir(log_path)

    regrid = configuration["regrid"]
    generate_meta = configuration["generate_meta"]
    apply_preprocess = configuration["apply_preprocess"]
    apply_postprocess = configuration["apply_postprocess"]

    start_date = configuration["start_date"]
    try:
        start_datetime = dt.datetime.strptime( start_date, "%Y%m%d" )
    except:
        start_datetime = dt.datetime.today()
        start_date = dt.datetime.strftime( start_datetime, format="%Y%m%d" )
    
    end_date = configuration["end_date"]
    try:
        end_datetime = dt.datetime.strptime( end_date, "%Y%m%d" )
    except:
        end_datetime = dt.datetime.today()
        end_date = dt.datetime.strftime( end_datetime, format="%Y%m%d" )
    
    update_start_date = configuration["update_start_date"]

    date_range = []
    c_dt = start_datetime
    while c_dt <= end_datetime:
        date_range.append( dt.datetime.strftime( c_dt, "%Y%m%d" ) )
        c_dt = c_dt + dt.timedelta(days=1)

    roi_config_file = configuration["roi_config"]
    with open(roi_config_file) as roi_config_f:
        roi_configuration = json.load(roi_config_f)

        roi_key = roi_configuration["main"]["key"]
        roi_name = roi_configuration["main"]["name"]
        roi_bbox_lat_min = roi_configuration["main"]["bbox"]["lat_min"]
        roi_bbox_lat_max = roi_configuration["main"]["bbox"]["lat_max"]
        roi_bbox_lon_min = roi_configuration["main"]["bbox"]["lon_min"]
        roi_bbox_lon_max = roi_configuration["main"]["bbox"]["lon_max"]
        
        basins = roi_configuration["basins"]

    roi_config_f.close()

    if configuration["logging_level"] == "info":
        logging_level = logging.INFO
    elif configuration["logging_level"] == "debug":
        logging_level = logging.DEBUG
    else:
        logging_level = logging.ERROR

    email_notification = configuration["email"]
    
    script_version = configuration["script_version"]

config_file.close()

log_filename = str(log_path) + "/" + provider_name + "_extract_" +  dt.datetime.now().strftime("%Y%m%dT%H%M%S") + ".log"

logging.basicConfig(
    filename = log_filename,
    format = '%(asctime)s - %(message)s',
    filemode = 'a',
    level = logging_level)


logging.info( "Project name: " + project_name )
logging.info( "Provider name: " + provider_name )
logging.info( "Model name: " + model_name )
logging.info( "Model ensemble number: " + str(model_ensemble) )
logging.info( "Model releases: " + str(model_releases) )
logging.info( "Model variables: " + str(model_variables) )

logging.info( "Output types: " + str(output_types) )
logging.info( "Output variables: " + str(output_variables) )

logging.info( "Input path: " + input_path )
logging.info( "Output path: " + output_path )
logging.info( "Log filename path: " + str(log_path) )

logging.info( "Start date: " + str(start_date) )
logging.info( "End date: " + str(end_date) )

logging.info( "ROI name: " + roi_name )

logging.info( "Main basin BBOX: [{lat_min} {lat_max}, {lon_min} {lon_max}]".format(
    lat_min=roi_bbox_lat_min,
    lat_max=roi_bbox_lat_max,
    lon_min=roi_bbox_lon_min,
    lon_max=roi_bbox_lon_max)
    )

dirs = glob.glob( input_path + "*/" )



def extract(dir):

    curr_date = dir.split('/')[-2]
    if not(curr_date in date_range):
        return 0
    
    logging.info("Processing: " + dir)

    for model_release in model_releases:

        c_keyword_release = ["_{date}{r}_".format(date=curr_date,r=str(model_release).zfill(2))]
        
        # move_to_output(
        #     input_dir=dir+'to_regrid/', output_dir=dir,move_keywords=['regridded'])
        files_to_convert = glob.glob(dir + '*regular*.grib2' ) + \
            glob.glob( dir + '*regridded*.grib2' ) + \
                glob.glob( dir + '*extracted*.grib2' )

        #remove_unuseful_grib2( dir, keywords=['_000_'], mirror=False )

        files_to_convert = [ f for f in files_to_convert if curr_date+str(model_release).zfill(2) in f ]

        if output_extension == 'csv':

            t_2m_df, tot_prec_df, w_snow_df = extract_csv(
                files_to_convert, model_variables,logging, 
                roi_bbox=[
                    roi_bbox_lat_min,
                    roi_bbox_lat_max,
                    roi_bbox_lon_min,
                    roi_bbox_lon_max], implementation='local')

            ### save all points to a different CSV
            if "precipitation" in output_variables:
                extration_status = extract_on_subbasins(
                    output_path, tot_prec_df, "precipitation", roi_key, model_release, input_type,
                    output_datetime_format=output_datetime_format, input_timezone=model_timezone, 
                    subbasins=basins, model_resolution=model_resolution, generate_meta=generate_meta)
            if "temperature" in output_variables:
                extration_status = extract_on_subbasins(
                    output_path, t_2m_df, "temperature", roi_key, model_release, input_type,
                    output_datetime_format=output_datetime_format, input_timezone=model_timezone, 
                    subbasins=basins, model_resolution=model_resolution, generate_meta=generate_meta)
            if "snow" in output_variables:
                extration_status = extract_on_subbasins(
                    output_path, w_snow_df, "snow", roi_key, model_release, input_type,
                    output_datetime_format=output_datetime_format, input_timezone=model_timezone, 
                    subbasins=basins, model_resolution=model_resolution, generate_meta=generate_meta)
            
            if extration_status == 1:
                continue
    
    logging.info(f"Directory {dir} can be deleted!")

from multiprocessing import Pool, cpu_count

count = cpu_count()

pool = Pool(processes=count)
pool.map(extract, dirs)
pool.close()
pool.join()

if update_start_date == True:
    new_start_date = (dt.datetime( 
        end_datetime.year,end_datetime.month,end_datetime.day ) + dt.timedelta(days=1)).strftime(format="%Y%m%d")

    logging.info("Set up the last date: " + str(new_start_date))

    configuration['start_date'] = new_start_date

    with open(configuration_file, 'w') as config_file:
        json.dump(configuration, config_file, indent=2)
        config_file.close()
