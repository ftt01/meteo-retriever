#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import sys

lib_dir = "/home/daniele/documents/github/ftt01/phd/share/lib"
sys.path.insert( 0, lib_dir )


# In[2]:


from lib import *


# In[3]:


import logging
from pathlib import Path


# In[ ]:


input_parser = argparse.ArgumentParser()
input_parser.add_argument("-c","--configuration_file", type=str, required=False, default="/home/daniele/documents/github/ftt01/phd/data/meteo/providers/dwd/etc/conf/extract/icon-d2-eps.json")
args = input_parser.parse_args()
configuration_file = args.configuration_file


# In[ ]:


# configuration_file = "/media/windows/projects/turbidity/turbidity_DDF/etc/conf/bias/input_DWD_data.json"


# In[ ]:


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


# In[ ]:


## takes all files in the directory, that contains one of the keywords and apply the grib_copy
## the results are saved in a directory called to_regrid
## remove the unuseful files in to_regrid directory

def reorder_grib2(path_dir, reorder_keywords=None, regrid_keywords=None):

    mkNestedDir( path_dir + "to_regrid/" )

    logging.info("Reordering using keywords: " + str(reorder_keywords))

    files_to_reorder = glob.glob(path_dir + "*.grib2")
    for file_to_reorder in files_to_reorder:
        if all(word in file_to_reorder for word in reorder_keywords):
            subprocess.run('''grib_copy {path_dir}{file}.grib2 {path_dir}to_regrid/{file}_[stepRange].grib2'''.format(
                    path_dir=path_dir,
                    file=os.path.basename(file_to_reorder)[:-6]),
                    shell=True, check=True, executable='/bin/bash')
    
    logging.info("Remove using keywords: " + str(regrid_keywords))
    
    files_to_regrid = glob.glob(path_dir + "to_regrid/" + "*.grib2")
    for file_to_regrid in files_to_regrid:
        if any(word in file_to_regrid for word in regrid_keywords):
            continue
        else:
            os.remove( file_to_regrid )


# In[ ]:


def move_to_regrid(path_dir, regrid_keywords=None, vars=None, mode='any'):

    mkNestedDir( path_dir + "to_regrid/" )

    logging.info("Moving to regrid using keywords: " + str(regrid_keywords))

    files_to_regrid = glob.glob(path_dir + "*.grib2")
    for file_to_regrid in files_to_regrid:

        for c_var in vars:

            if not(c_var in file_to_regrid):
                continue

            if mode == 'any':

                if any(word in file_to_regrid for word in regrid_keywords):
                    try:
                        shutil.copy(file_to_regrid, path_dir + "to_regrid/" + os.path.basename(file_to_regrid))
                    except IOError as e:
                        print("Unable to copy file. %s" % e)
                    except:
                        print("Unexpected error:", sys.exc_info())
            
            elif mode == 'all':

                if all(word in file_to_regrid for word in regrid_keywords):
                    try:
                        shutil.copy(file_to_regrid, path_dir + "to_regrid/" + os.path.basename(file_to_regrid))
                    except IOError as e:
                        print("Unable to copy file. %s" % e)
                    except:
                        print("Unexpected error:", sys.exc_info())


# In[ ]:


def regrid_dir(project_name, path_dir, model_name=None, keywords=None, remove_unregridded=False):

    if keywords != None:

        logging.info("Regridding using keywords: " + str(keywords))

        files_to_regrid = glob.glob(path_dir + "*.grib2")

        for file_to_regrid in files_to_regrid:
            if any(word in file_to_regrid for word in keywords):
                # subprocess.run('''docker run --name regrid_{model_name}_{prj} --rm                     --volume {path_dir}:/local                     --env INPUT_FILE=/local/{file}                     --env OUTPUT_FILE=/local/regridded_{file}                     deutscherwetterdienst/regrid:{model_name}                     /convert.sh'''.format(
                subprocess.run('''docker run --rm                     --volume {path_dir}:/local                     --env INPUT_FILE=/local/{file}                     --env OUTPUT_FILE=/local/regridded_{file}                     deutscherwetterdienst/regrid:{model_name}                     /convert.sh'''.format(
                    prj=project_name,
                    model_name=model_name,
                    path_dir=path_dir,
                    file=os.path.basename(file_to_regrid)),
                    shell=True, check=True,
                    executable='/bin/bash')
    else:

        logging.info("Regridding entire directory: " + path_dir)

        # subprocess.run('''docker run --name regrid_{model_name}_{prj} --rm                 --volume {path_dir}:/local                 --env INPUT_FILE=/local                 --env OUTPUT_FILE=/local                 deutscherwetterdienst/regrid:{model_name}                 /convert.sh'''.format(
        subprocess.run('''docker run --rm --volume {path_dir}:/local --env INPUT_FILE=/local --env OUTPUT_FILE=/local deutscherwetterdienst/regrid:{model_name} /convert.sh'''.format(
            prj=project_name,
            path_dir=path_dir,
            model_name=model_name),
            shell=True, check=True,
            executable='/bin/bash')

    if remove_unregridded == True:
        remove_unuseful_grib2(path_dir, keywords=['regridded'], mirror=True)


# In[ ]:


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


# In[ ]:


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

            # curr_lat_min,curr_lat_max,curr_lon_min,curr_lon_max = bbox_extraction( 
            #     bbox_lat_min=el['bbox']['lat_min'],
            #     bbox_lat_max=el['bbox']['lat_max'],
            #     bbox_lon_min=el['bbox']['lon_min'],
            #     bbox_lon_max=el['bbox']['lon_max'],
            #     spatial_resolution=model_resolution,
            #     lon_factor=0)
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

                    output_file_path = dir + "{main_basin}/{subbasin}/{release_hour}/{variable}/{input_type}/{point_id}/".format(
                        main_basin = main_basin_name,
                        subbasin = el['key'],
                        release_hour = "R" + str( rel_time ).zfill(3),
                        variable = variable,
                        input_type = input_type,
                        point_id = str(id).zfill(3),
                        )
                    mkNestedDir(output_file_path)

                    output_file_name = output_file_path + dt.datetime.strftime( current_df.index[0], format='%Y%m%d' ) + ".csv" 
                    current_df.index = [ dt.datetime.strftime( ix, output_datetime_format ) for ix in current_df.index ]
                    current_df.index.name = "datetime"
                    current_df.to_csv( output_file_name )

                    id = id + 1

            if generate_meta == True:
                meta_df = pd.DataFrame(index=grid_ids)
                meta_df["lon"] = grid_lons
                meta_df["lat"] = grid_lats

                metadata_filename = Path(output_file_path)
                meta_df.to_csv( str(metadata_filename.parent.absolute()) + "/grid.csv" )

            del current_df
    except:
        logging.info("Uncomplete: " + variable)


# In[ ]:


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


# In[ ]:





# In[ ]:


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
            # df['lon'] = [round(idx,6) for idx in df['x']]
            # df['lat'] = [round(idy,6) for idy in df['y']]

            # release_time = ( current_datetime - dt.timedelta(hours=1) ).hour
            # if not(release_time in model_releases):
            #     continue

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


# In[ ]:


def crop_grib2( project_name, c_file, model_name="icon-d2-eps", bbox=[5,17,43,49], output_path=None, logging=None ):

    file_path = parent_directory(c_file)
    file_name = extract_filename(c_file)

    # c_cmd = '''docker run --name cropper_{model}_{prj}         --rm -v {file_path}:/home/{model}/data/             --entrypoint cdo                 cdo-ftt_{model} -f grb2                     -sellonlatbox,{lon_min},{lon_max},{lat_min},{lat_max}                         {i_file_name} {o_file_name}'''

    c_cmd = '''docker run --rm -v {file_path}:/home/{model}/data/ --entrypoint cdo ftt01cdo -f grb2 -sellonlatbox,{lon_min},{lon_max},{lat_min},{lat_max} /home/{model}/data/{i_file_name} /home/{model}/data/{o_file_name}'''

    complete_cmd = c_cmd.format(
        prj=project_name,
        file_path=file_path,
        model=model_name,
        lon_min=bbox[0],
        lon_max=bbox[1],
        lat_min=bbox[2],
        lat_max=bbox[3],
        i_file_name=file_name,
        o_file_name="extracted_"+file_name )

    logging.debug("Running CMD: " + complete_cmd)

    subprocess.run( complete_cmd,
            shell=True, check=True,
            executable='/bin/bash')

    # if output_path != None:
    #     mv_cmd = "mv {infile} {outfile}".format(
    #         infile=file_path + "extracted_" + file_name,
    #         outfile=output_path + file_name
    #     )
    #     subprocess.run( mv_cmd,
    #         shell=True, check=True,
    #         executable='/bin/bash')


# In[ ]:


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


# In[ ]:


def postprocess(
    input_path, 
    days_to_compute, 
    roi_name, roi_key, basins, 
    releases, lead_hours, model_ensemble,
    output_datetime_format="%Y-%m-%dT%H:%M:%SZ%z", output_timezone='UTC',
    input_type="ensemble", output_type="mean", logging=logging):

    for day in days_to_compute:

        logging.debug( "Processing date: " + day )
        logging.info( "Basin: " + roi_name )

        for subbasin in basins:
            sb_key = subbasin['key']
            logging.info( "Subbasin: " + sb_key )
            
            for release in releases:

                c_rel = "R" + str(release).zfill(3)
                logging.info( "Release: " + c_rel )

                utc_timezone = pytz.timezone('UTC')
                c_start_datetime = utc_timezone.localize( dt.datetime.strptime(
                    day + str(int(release)+1).zfill(2), "%Y%m%d%H" ) )
                c_start_datetime = c_start_datetime.astimezone(output_timezone)
                logging.debug( "Current start datetime: " + c_start_datetime.strftime(format="%Y-%m-%dT%H:%M:%SZ%z") )

                c_path_rel = input_path + roi_key + "/" + sb_key + "/" + c_rel + "/" 
                path_vars = glob.glob( c_path_rel + "*/" )
                logging.debug( "Vars path: " + str(path_vars) )
                
                for path_var in path_vars:
                    
                    c_var = path_var.split('/')[-2]
                    logging.info( "Variable: " + c_var )
                    
                    point_matrix = pd.DataFrame()
                    for lead_hour in range(lead_hours):

                        c_dt = c_start_datetime + dt.timedelta(hours=lead_hour) 

                        tmp_ens_points = pd.DataFrame( index = [str(n).zfill(3) for n in range( 1, model_ensemble + 1 )] )

                        nodes_dir = glob.glob( c_path_rel + c_var + '/' + input_type + "/*/" )
                        for node_dir in nodes_dir:

                            file_to_open = node_dir + day + ".csv"
                            logging.debug( "Opening: " + file_to_open )
                            # print(file_to_open)

                            point_id = str(node_dir.split('/')[-2]).zfill(3)
                            logging.debug( "Current node: " + point_id )
                            # print(point_id)

                            try:
                                current_file = pd.read_csv( file_to_open, index_col=0 )
                                current_file.index = pd.to_datetime( current_file.index, format=output_datetime_format )
                                current_file.index = [ output_timezone.localize(
                                    idx).astimezone(output_timezone) for idx in current_file.index ]
                            except FileNotFoundError as fnf:
                                # logging.warning( "Not found: " + file_to_open )
                                continue

                            try:
                                current_data = pd.DataFrame( current_file.loc[ c_dt ] )
                                tmp_ens_points = pd.concat( [tmp_ens_points,current_data], axis=1 )
                            except KeyError as ke:
                                # logging.warning( "Not available: " + c_dt.strftime(format="%Y-%m-%d %H:%M:%S") )
                                continue
                            except Exception:
                                break
                        
                        point_matrix[c_dt] = round( tmp_ens_points.mean(axis=1),2 )

                        del tmp_ens_points

                    mean_matrix = point_matrix.T
                    mean_matrix.index = [ dt.datetime.strftime(i, format='%Y-%m-%d %H:%M:%S') for i in mean_matrix.index ]
                    mean_matrix.index.name = 'datetime'

                    if c_var == 'temperature':
                        ### Kelvin to Celsius
                        # mean_matrix = mean_matrix - 273.15
                        mean_matrix = mean_matrix

                    if output_type == "mean":
                        mean_matrix = mean_matrix.mean( axis=1 )
                        mean_matrix = round(mean_matrix,2)

                        mean_matrix = pd.DataFrame(mean_matrix.values, index=mean_matrix.index, columns=["values"])

                    else:
                        mean_matrix.columns = [str(m).zfill(3) for m in mean_matrix.columns]

                    # output_file = input_path + "postprocessed/" + roi_key + '/' + sb_key + '/' + c_rel + '/' + c_var + '/' + \
                    #     output_type + '/spatial_mean/' + day + '.csv'
                    output_file = input_path + "postprocessed/" + roi_key + '/' + sb_key + '/' + c_rel + '/' + c_var + '/' +                         output_type + '/' + day + '.csv'
                    mkNestedDir(os.path.dirname(output_file))

                    logging.info( "Saving: " + output_file )
                    mean_matrix.to_csv( output_file )

def all_done_check(curr_date, output_path):
    ## check done_dates
    for model_release in model_releases:
        for c_var in output_variables:
            for el in basins:
                output_file_path = output_path + "{main_basin}/{subbasin}/{release_hour}/{variable}/{input_type}/".format(
                        main_basin = roi_key,
                        subbasin = el['key'],
                        release_hour = "R" + str( model_release ).zfill(3),
                        variable = c_var,
                        input_type = input_type
                )
                cur_dirs = glob.glob(f"{output_file_path}*/")
                if len(cur_dirs) == 0:
                    cur_list = glob.glob(f"{output_file_path}*.csv")
                    cur_list = [c[-12:-4] for c in cur_list]
                    if not(curr_date in cur_list):
                        return False
                else:
                    for d in cur_dirs:
                        cur_list = glob.glob(f"{d}/*.csv")
                        cur_list = [c[-12:-4] for c in cur_list]
                        if not(curr_date in cur_list):
                            return False
    return True

computation_start = dt.datetime.now()


# In[ ]:


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


# In[ ]:


# log_filename = str(log_path) + "/" + start_date + "_" + end_date + "_extract_" + script_version + ".log"
log_filename = str(log_path) + "/" + provider_name + "_extract_" +  dt.datetime.now().strftime("%Y%m%dT%H%M%S") + ".log"

logging.basicConfig(
    filename = log_filename,
    format = '%(asctime)s - %(message)s',
    filemode = 'a',
    level = logging_level)


# In[ ]:


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


# In[ ]:


# # download grid definition and generate weights
# ARG GRID_FILENAME=icon_grid_0047_R19B07_L.nc.bz2
# ARG NC_GRID_NUMBER=2
# RUN set -ex \
#     && mkdir -p /data/grids/${MODEL_NAME} \
#     && cd /data/grids/${MODEL_NAME} \
#     && wget -O ${MODEL_NAME}_grid.nc.bz2 https://opendata.dwd.de/weather/lib/cdo/${GRID_FILENAME} \
#     && bunzip2 ${MODEL_NAME}_grid.nc.bz2 \
#     && mkdir -p /data/weights/${MODEL_NAME} \
#     && cd /data/weights/${MODEL_NAME} \
#     && echo Generating weights for ${MODEL_NAME} ... \
#     && cdo \
#          gennn,/data/descriptions/${MODEL_NAME}/${MODEL_NAME}_description.txt \
#             -setgrid,/data/grids/${MODEL_NAME}/${MODEL_NAME}_grid.nc:${NC_GRID_NUMBER} \
#             /data/samples/${MODEL_NAME}/${MODEL_NAME}_sample.grib2 \
#             /data/weights/${MODEL_NAME}/${MODEL_NAME}_weights.nc \
#     && cdo \
#          gennn,/data/descriptions/${MODEL_NAME}/${MODEL_NAME}_rotated_description.txt \
#             -setgrid,/data/grids/${MODEL_NAME}/${MODEL_NAME}_grid.nc:${NC_GRID_NUMBER} \
#             /data/samples/${MODEL_NAME}/${MODEL_NAME}_sample.grib2 \
#             /data/weights/${MODEL_NAME}/${MODEL_NAME}_rotated_weights.nc


# All of the regrid is done using directly with the docker developed by DWD:
# 
# ```
# docker run --rm \
#     --volume ~/mydata:/mydata \
#     --env INPUT_FILE=/mydata/my_icon-eps_icosahedral_file.grib2 \
#     --env OUTPUT_FILE=/mydata/regridded_regular_lat_lon_output.grib2 \
#     deutscherwetterdienst/regrid:icon-eps
# ```

# Alternative is the cdo command:
# 
# ```
# cdo -f grb2 remap,${descriptionFile},${weightsFile} ${input} ${output}
# ```

# In[ ]:


logging.info( "ROI name: " + roi_name )

# lat_min,lat_max,lon_min,lon_max = bbox_extraction( 
#     bbox_lat_min=roi_bbox_lat_min,
#     bbox_lat_max=roi_bbox_lat_max,
#     bbox_lon_min=roi_bbox_lon_min,
#     bbox_lon_max=roi_bbox_lon_max,
#     spatial_resolution=model_resolution,
#     lon_factor=0)

# logging.info( "Main basin BBOX: [{lat_min} {lat_max}, {lon_min} {lon_max}]".format(
#     lat_min=lat_min,
#     lat_max=lat_max,
#     lon_min=lon_min,
#     lon_max=lon_max)
#     )

logging.info( "Main basin BBOX: [{lat_min} {lat_max}, {lon_min} {lon_max}]".format(
    lat_min=roi_bbox_lat_min,
    lat_max=roi_bbox_lat_max,
    lon_min=roi_bbox_lon_min,
    lon_max=roi_bbox_lon_max)
    )


# In[ ]:


dirs = glob.glob( input_path + "*/" )


# ### transform precipitation grib2 to 20 bands: reorder
# 1. grib_copy {name}.grib2 {name}_[stepRange].grib2
# 2. mv all that are 0-60 or multiples
# 3. mv all temperature
# 4. mv all snow

# In[ ]:


# for dir in dirs:

#     curr_date = dir.split('/')[-2]
#     if not(curr_date in date_range):
#         continue
    
#     if output_extension == 'csv':

#         output_files_path = []
#         for vv in model_variables:
#             if (vv == 'tot_prec') or (vv == 'TOT_PREC'):
#                 c_var = 'precipitation'
#             elif vv == 't_2m'  or (vv == 'T_2M'):
#                 c_var = 'temperature'
#             elif vv == 'w_snow'  or (vv == 'W_SNOW'):
#                 c_var = 'snow'
#             else:
#                 logging.error("Not implemented variable: " + vv)
#             for it in output_types:
#                 for release in model_releases:
#                     c_rel = "R" + str(release).zfill(3)

#                     for el in basins:
#                         logging.debug("Check if exist: " + el['name'])

#                         output_files_path.append( 
#                             output_path + "postprocessed/{main_basin}/{subbasin}/{release_hour}/{variable}/{input_type}/{c_date}.csv".format(
#                                 main_basin = roi_key,
#                                 subbasin = el['key'],
#                                 release_hour = c_rel,
#                                 variable = c_var,
#                                 input_type = it,
#                                 c_date = curr_date
#                             )
#                         )
                        
#         # print( output_files_path )
#         if all([os.path.isfile(f) for f in output_files_path]):
#             date_range.remove(curr_date)

#     elif output_extension == 'grib2':
        
#         c_out_file = output_path + "/" + curr_date + "/"
#         try:
#             c_files = glob.glob(c_out_file)
#             if len(c_files) != 0:
#                 date_range.remove(curr_date)
#                 continue
#         except:
#             logging.debug( "No previous data, extracting: " + curr_date )

#     else:
#         logging.error('Not a valid output_extension! [csv,grib2]')


# In[ ]:


prec_keys = [
    '0-60',
    '0-120',
    '0-180',
    '0-240',
    '0-300',
    '0-360',
    '0-420',
    '0-480',
    '0-540',
    '0-600',
    '0-660',
    '0-720',
    '0-780',
    '0-840',
    '0-900',
    '0-960',
    '0-1020',
    '0-1080',
    '0-1140',
    '0-1200',
    '0-1260',
    '0-1320',
    '0-1380',
    '0-1440',
    '0-1500',
    '0-1560',
    '0-1620',
    '0-1680',
    '0-1740',
    '0-1800',
    '0-1860',
    '0-1920',
    '0-1980',
    '0-2040',
    '0-2100',
    '0-2160',
    '0-2220',
    '0-2280',
    '0-2340',
    '0-2400',
    '0-2460',
    '0-2520',
    '0-2580',
    '0-2640',
    '0-2700',
    '0-2760',
    '0-2820',
    '0-2880']

temp_keys = ['t_2m']
snow_keys = ['w_snow']


# In[ ]:

if apply_preprocess == True:

    for dir in dirs:

        curr_date = dir.split('/')[-2]
        if not(curr_date in date_range):
            continue

        if all_done_check(curr_date, output_path) == True:
            continue

        logging.info("Processing: " + dir)

        for model_release in model_releases:

            c_keyword_release = ["_{date}{r}_".format(date=curr_date,r=str(model_release).zfill(2))]
            
            if regrid == True:

                for c_var in output_variables:

                    if c_var == "precipitation":
                        ### copy the precipitation to to_regrid folder
                        regrid_keywords=prec_keys
                        reorder_grib2(dir, reorder_keywords=c_keyword_release+[model_variables["precipitation"]], 
                            regrid_keywords=regrid_keywords)

                    elif c_var == "temperature":

                        ### copy the temperature to_regrid
                        move_to_regrid( dir, regrid_keywords=c_keyword_release, vars=[model_variables["temperature"]], mode='any' )
                    
                    elif c_var == "snow":

                        ### copy the temperature to_regrid
                        move_to_regrid( dir, regrid_keywords=c_keyword_release, vars=[model_variables["snow"]], mode='any' )

                if not(model_name == 'icon-eu'):
                    remove_unuseful_grib2( dir + 'to_regrid/', keywords=['_000_'] )
                    regrid_dir( 
                        project_name,
                        dir + 'to_regrid/', 
                        model_name=model_name, 
                        remove_unregridded=True )
                    convertion_key = 'regridded'
                else:
                    convertion_key = ''

                files_to_convert = glob.glob( 
                    dir + 'to_regrid/{convertion_key}*.grib2'.format(
                        convertion_key=convertion_key) )
            else:
                move_to_output(input_dir=dir+'to_regrid/', output_dir=dir,move_keywords=['regridded'])
                files_to_convert = glob.glob( dir + '*regular*.grib2' ) +                         glob.glob( dir + '*regridded*.grib2' ) +                                 glob.glob( dir + '*extracted*.grib2' )
                # glob.glob( dir + 'to_regrid/*regridded*.grib2' ) + \
                
            # release_time = None
            remove_unuseful_grib2( dir, keywords=['_000_'], mirror=False )
            
            if model_name != 'icon-eu':  ## check only if ensemble
                files_to_convert = [ f for f in files_to_convert if any(word in f for word in prec_keys + temp_keys + snow_keys) ]

            files_to_convert = [ f for f in files_to_convert if curr_date+str(model_release).zfill(2) in f ]

            if output_extension == 'csv':

                # try:
                t_2m_df, tot_prec_df, w_snow_df = extract_csv(
                    files_to_convert, model_variables,logging, 
                    roi_bbox=[
                        roi_bbox_lat_min,
                        roi_bbox_lat_max,
                        roi_bbox_lon_min,
                        roi_bbox_lon_max], implementation='local')
                # except:
                #     t_2m_df, tot_prec_df, w_snow_df = extract_csv(
                #         files_to_convert, model_variables,logging, 
                #         roi_bbox=[
                #             roi_bbox_lat_min,
                #             roi_bbox_lat_max,
                #             roi_bbox_lon_min,
                #             roi_bbox_lon_max], 
                #         implementation='docker',
                #         input_path=dir)

                # if regrid == True:
                #     shutil.rmtree( dir + 'to_regrid/' )

                ### save all points to a different CSV
                if "precipitation" in output_variables:
                    extract_on_subbasins(
                        output_path, tot_prec_df, "precipitation", roi_key, model_release, input_type,
                        output_datetime_format=output_datetime_format, input_timezone=model_timezone, 
                        subbasins=basins, model_resolution=model_resolution, generate_meta=generate_meta)
                if "temperature" in output_variables:
                    extract_on_subbasins(
                        output_path, t_2m_df, "temperature", roi_key, model_release, input_type,
                        output_datetime_format=output_datetime_format, input_timezone=model_timezone, 
                        subbasins=basins, model_resolution=model_resolution, generate_meta=generate_meta)
                if "snow" in output_variables:
                    extract_on_subbasins(
                        output_path, w_snow_df, "snow", roi_key, model_release, input_type,
                        output_datetime_format=output_datetime_format, input_timezone=model_timezone, 
                        subbasins=basins, model_resolution=model_resolution, generate_meta=generate_meta)

            elif output_extension == "grib2":
                
                for file in files_to_convert:

                    ## just cut the grib2 and save the cut files for future extraction
                    logging.debug("Cut to new grib2: " + file)

                    ## run docker container with cdo command to cut the BBOX of the current basin
                    ## cdo -f grb2 -sellonlatbox,6.5,14.5,44,47.5 in.grib2 out.grib2
                    ## to overwrite the files just use the same name
                    c_out_file = output_path + curr_date + "/"
                    mkNestedDir(c_out_file)
                    try:
                        crop_grib2(
                            project_name,
                            file, 
                            model_name=model_name, 
                            bbox=[
                                roi_bbox_lon_min,
                                roi_bbox_lon_max,
                                roi_bbox_lat_min,
                                roi_bbox_lat_max
                                ], 
                            output_path=c_out_file,
                            logging=logging )
                    except:
                        logging.debug('Unable to convert: ' + file)
                        continue    
                
                if model_name != 'icon-eu':
                    move_to_output(input_dir=dir+"to_regrid/",output_dir=output_path+curr_date+"/",move_keywords=['extracted'])
                    shutil.rmtree( dir+"to_regrid/" )
                else:
                    move_to_output(input_dir=dir,output_dir=output_path+curr_date+"/",move_keywords=['extracted'])
            
            else:
                logging.error( "Not a valid extension to extract to..[csv,grib2]" )
        
        logging.info(f"Directory {dir} can be deleted!")


# In[ ]:


if update_start_date == True:
    new_start_date = (dt.datetime( 
        end_datetime.year,end_datetime.month,end_datetime.day ) + dt.timedelta(days=1)).strftime(format="%Y%m%d")

    logging.info("Set up the last date: " + str(new_start_date))

    configuration['start_date'] = new_start_date

    with open(configuration_file, 'w') as config_file:
        json.dump(configuration, config_file, indent=2)
        config_file.close()


# In[ ]:


if apply_postprocess == True:
    logging.info('''\n
        ###############################\n
            POSTPROCESS\n
        ###############################\n''')
    
    for curr_date in date_range:

        if all_done_check(curr_date, output_path+'postprocessed/') == True:
            date_range.remove(curr_date)

    for output_type in output_types:

        postprocess(
            output_path, 
            date_range, 
            roi_name, roi_key, basins, 
            model_releases, model_lead_hours, model_ensemble, 
            output_datetime_format=output_datetime_format, output_timezone=output_timezone,
            input_type=input_type, output_type=output_type, logging=logging
        )


# In[ ]:


if email_notification == True:
    send_email(
        subject="DWD extracted!",
        body="Started at " + computation_start.strftime(format="%Y-%m-%dT%H:%M:%SZ%z") + 
            "\nFinish at " + dt.datetime.now().strftime(format="%Y-%m-%dT%H:%M:%SZ%z") +
            "\nJSON config: " + json.dumps(configuration, indent=2, default=str)
    )

