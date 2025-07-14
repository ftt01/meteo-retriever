from sys import path as syspath
import subprocess

lib_dir = "/home/daniele/documents/github/ftt01/phd/share/lib"

syspath.insert( 0, lib_dir )

from lib import send_email

start_date = "2014-08-02T00:00:00"
end_date = "2023-12-31T23:59:00"
variables = ["tp","2t"]
output_path = "/media/windows/projects/hydro_data_driven/00_data/meteo/era5land/bias_correction/inputs/"
#### grig_meta must be coerent: id (int), lat (float), lon (float)
grid_meta = "/media/windows/projects/hydro_data_driven/00_data/meteo/era5land/bias_correction/inputs/AA2700buffer_wElevation.csv"

for variable in variables:

    cmd = '''python3 /home/daniele/documents/github/ftt01/phd/data/meteo/providers/ecmwf/bin/era5/land/extract_from_DB_v1.py {start_date} {end_date} {variable} {output_path} {grid_meta}'''.format(
            start_date = start_date,
            end_date = end_date,
            variable = variable,
            output_path = output_path,
            grid_meta = grid_meta
    )
    print(cmd)
    process = subprocess.Popen( cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        send_email(
            subject="ERROR: ERA5land NOT extracted",
            body="Error: " + str(stderr.decode('utf-8'))
        )
    else:
        
        send_email(
            subject="ERA5land EXTRACTED!",
            body="Successfully extracted: {}, from {} to {} in {}\n".format(variable,start_date,end_date,output_path)
        )