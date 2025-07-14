from sys import path as syspath

lib_dir = "/media/windows/projects/hydro_data_driven/01_code/hydrological_DDF/hydrological_forecasting/lib"
syspath.insert( 0, lib_dir )

## general
from locallib import json, logging, argparse, Polygon, dt, date_range, DataFrame, mkNestedDir, getPathFromFilepath, Path
## db
from locallib import extract_era5land

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--conf_file", type=str)
parser.add_argument("--bias", action=argparse.BooleanOptionalAction, required=False, default=False)
args = parser.parse_args()

# class local_args():

#     def __init__(self) -> None:
#         pass

#     def add_configuration_file(self,  conf_file):
#         self.conf_file = conf_file
    
#     def add_bias(self,  bias):
#         self.bias = bias

# args = local_args()
# args.add_configuration_file("/media/windows/projects/hydro_data_driven/02_material_and_methods/02_operative/C/conf/input/ECMWF_ERA5land_data.json")
# args.add_bias(True)

with open(args.conf_file) as file_config:
    conf_file = json.load(file_config)
    file_config.close()

with open(conf_file['roi_config']) as roi_config_f:
    roi_configuration = json.load(roi_config_f)
    main_key = roi_configuration["main"]["key"]
    basins = roi_configuration["basins"]
    roi_config_f.close()

if conf_file["logging_level"] == "info":
    logging_level = logging.INFO
elif conf_file["logging_level"] == "debug":
    logging_level = logging.DEBUG
else:
    logging_level = logging.ERROR

provider_name = conf_file['provider_name']

log_path = Path( conf_file["log_path"] )
mkNestedDir(log_path)

log_filename = str(log_path) + "/" + provider_name + "_extract_" +  dt.datetime.now().strftime("%Y%m%dT%H%M%S") + ".log"

logging.basicConfig(
    filename = log_filename,
    format = '%(asctime)s - %(message)s',
    filemode = 'a',
    level = logging_level)

start_date_str = conf_file['start_date']
end_data_date_str = conf_file['end_date']

start_data_datetime = dt.datetime.strptime( start_date_str, "%Y%m%d" )
end_data_datetime = dt.datetime.strptime( end_data_date_str, "%Y%m%d" )

dr = date_range(start=start_data_datetime, end=end_data_datetime, freq='1D')

variables = conf_file['output']['variables']

releases = conf_file['model']['release']
forecast_horizon = conf_file['model']['lead_hours']
ens_size = conf_file['model']['ensemble']

output_path = conf_file['output']['path']

for release in releases:

    c_rel = f"R{str(release).zfill(3)}"
    logging.info(f"Extraction of release: {c_rel}")

    for subbasin in basins:
        c_sub = subbasin["key"]
        logging.info(f"Subbasin: {c_sub}")
        
        lat_min = subbasin['bbox']['lat_min']
        lat_max = subbasin['bbox']['lat_max']
        lon_min = subbasin['bbox']['lon_min']
        lon_max = subbasin['bbox']['lon_max']

        c_poly = Polygon([(lon_min, lat_min), (lon_min, lat_max), (lon_max, lat_max), (lon_max, lat_min)])

        for variable in variables:

            c_var = conf_file['model']['variables'][variable]  
            logging.info(f"Variable: {c_var}") 

            for d in dr:

                logging.info(f"Extraction for date: {d.strftime('%Y%m%d')}") 

                c_start_date = d + dt.timedelta(hours = int(release))
                c_end_date = c_start_date + dt.timedelta(hours = int(forecast_horizon)-1)

                df = extract_era5land(
                    c_start_date, c_end_date, c_var, 
                    lat=c_poly.centroid.y, lon=c_poly.centroid.x, n=ens_size, bias=args.bias)
                
                ## save as ensemble
                curr_output_path_ens = output_path + f"{main_key}/{c_sub}/{c_rel}/{variable}/ensemble/{d.strftime('%Y%m%d')}.csv"

                logging.info(f"Saving to: {curr_output_path_ens}")               
                current_df = DataFrame(df.values, index=df.index, columns=[str(i).zfill(3) for i in range(1,ens_size+1)])

                mkNestedDir(getPathFromFilepath(curr_output_path_ens))
                current_df.to_csv( curr_output_path_ens )

                ## save as mean
                curr_output_path = output_path + f"{main_key}/{c_sub}/{c_rel}/{variable}/mean/{d.strftime('%Y%m%d')}.csv"

                logging.info(f"Saving to: {curr_output_path}") 
                current_df = DataFrame(df.mean(axis=1).values, index=df.index, columns=["values"])

                current_df = current_df.round(decimals=3)

                mkNestedDir(getPathFromFilepath(curr_output_path))
                current_df.to_csv( curr_output_path )