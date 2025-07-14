import xarray
import datetime as dt
import pandas as pd
import argparse
import glob

input_parser = argparse.ArgumentParser()
## must give a list comma separated: "path1,path2,path3"
# input_parser.add_argument('files_to_import', type=lambda s: [str(item) for item in s.split(',')])

input_parser.add_argument('lat_max')
input_parser.add_argument('lat_min')
input_parser.add_argument('lon_max')
input_parser.add_argument('lon_min')

# input_parser.add_argument('model_variables')
model_variables = {'temperature':'t_2m', 'precipitation':'tot_prec', 'snow':'w_snow'}

args = input_parser.parse_args()

t_2m_df = pd.DataFrame()
tot_prec_df = pd.DataFrame()
w_snow_df = pd.DataFrame()

input_path = "/mnt/data/"
output_path = input_path

files_to_import = glob.glob( input_path + '*regular*.grib2' ) + \
        glob.glob( input_path + '*regridded*.grib2' ) + \
                glob.glob( input_path + '*extracted*.grib2' )

for file_to_import in files_to_import:
    ds = xarray.open_dataset(file_to_import, engine='pynio')

    variable_mapped_name = list(ds.keys())[0]
    variable_mapped_meta = ds.variables.get(list(ds.keys())[0]).attrs

    init_time = variable_mapped_meta['initial_time']
    fct_time = variable_mapped_meta['forecast_time']

    current_datetime = dt.datetime.strptime(init_time, "%m/%d/%Y (%H:%M)") + dt.timedelta(minutes=int(fct_time[0]))

    ds_red = ds.sel(lat_0=slice(args.lat_max,args.lat_min),lon_0=slice(args.lon_min,args.lon_max))
    df = ds.to_dataframe()
    df.reset_index(inplace=True)

    if model_variables["temperature"] in file_to_import:
        variable = 'temperature'
        ens_keyname = 'ensemble0'

        if t_2m_df.empty:

            t_2m_df = df

            # t_2m_df.insert(0, 'id', range(1, 1 + len(df)))

            t_2m_df['lat'] = [round(idy,6) for idy in t_2m_df['lat_0']]
            t_2m_df['lon'] = [round(idx,6) for idx in t_2m_df['lon_0']]

            # t_2m_df.set_index(['lat','lon','band'], inplace=True)
            
            t_2m_df[current_datetime] = [round(idy,2) for idy in df[variable_mapped_name]]
            t_2m_df = t_2m_df.loc[:, ['lat','lon',ens_keyname,current_datetime]]

        else:
            t_2m_df[current_datetime] = [round(idy,2) for idy in df[variable_mapped_name]]

    elif model_variables["precipitation"] in file_to_import:
        variable = 'precipitation'
        ens_keyname = 'ensemble0'

        if tot_prec_df.empty:

            tot_prec_df = df

            # tot_prec_df.insert(0, 'id', range(1, 1 + len(df)))

            tot_prec_df['lat'] = [round(idy,6) for idy in tot_prec_df['lat_0']]
            tot_prec_df['lon'] = [round(idx,6) for idx in tot_prec_df['lon_0']]

            # tot_prec_df.set_index(['lat','lon','band'], inplace=True)
            
            tot_prec_df[current_datetime] = [round(idy,2) for idy in df[variable_mapped_name]]
            tot_prec_df = tot_prec_df.loc[:, ['lat','lon',ens_keyname,current_datetime]]

        else:
            tot_prec_df[current_datetime] = [round(idy,2) for idy in df[variable_mapped_name]]

    elif model_variables["snow"] in file_to_import:
        variable = 'snow'
        ens_keyname = 'ensemble0'

        if w_snow_df.empty:

            w_snow_df = df

            # w_snow_df.insert(0, 'id', range(1, 1 + len(df)))

            w_snow_df['lat'] = [round(idy,6) for idy in w_snow_df['lat_0']]
            w_snow_df['lon'] = [round(idx,6) for idx in w_snow_df['lon_0']]

            # w_snow_df.set_index(['lat','lon','band'], inplace=True)
            
            w_snow_df[current_datetime] = [round(idy,2) for idy in df[variable_mapped_name]]
            w_snow_df = w_snow_df.loc[:, ['lat','lon',ens_keyname,current_datetime]]

        else:
            w_snow_df[current_datetime] = [round(idy,2) for idy in df[variable_mapped_name]]
    else:
        raise KeyError

t_2m_df.to_csv(output_path + 'temperature.csv')
tot_prec_df.to_csv(output_path + 'precipitation.csv')
w_snow_df.to_csv(output_path + 'snow.csv')