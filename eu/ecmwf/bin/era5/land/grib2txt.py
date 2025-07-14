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
input_parser.add_argument('-i','--input_path', type=str, default='/media/lacie2022/data/meteo/ecmwf/era5/land/AA/pippo/')
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

def execute(params):

    input_path = params[0]
    filename = params[1].split('.')[-2]
    model_varname = params[2]

    print(f"Input path: {input_path}")
    print(f"File name: {filename}")
    print(f"Model variable name: {model_varname}")

    tmp_txt = dt.datetime.strftime(
        dt.datetime.now(),
        format="%Y%m%dT%H%M%S") + '_' + str(random.randint(1,100000)) + "_" + model_varname

    if model_varname == 'tp':
        variable = 'tp'
        um = 'm'
        var_n = '228'

    elif model_varname == '2t':
        variable = '2t'
        um = 'K'
        var_n = '167'

    mkNestedDir( f"{input_path}tmp/" )

    # current_date = dt.datetime.strptime(filename.split('_')[-1][:-5], "%Y%m%d")

    # if exist_data( current_date, variable ):
    #     print(f"Data complete in the DB: {current_date}")
    #     return None 

    ## create a file for each variable
    pre_cmd = '''docker run --rm -v {input_path}:/home/conda/ ftt01cdo /bin/bash -c "cdo -selname,var{var_n} /home/conda/{filename}.grib /home/conda/tmp/{var}_{filename}.grib"'''.format(
        var = variable,
        var_n = var_n,
        filename = filename,
        input_path = input_path
    )
    print(pre_cmd)
    pre_process = subprocess.Popen(pre_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = pre_process.communicate()

    if ('Error' in str(stderr) or 'Warning' in str(stderr)):
        print(stderr)
        
    else:
        ## read the meta info in a table with cdo
        meta_cmd = '''docker run --rm -v {input_path}:/home/conda/ ftt01cdo /bin/bash -c "cdo -info /home/conda/tmp/{var}_{filename}.grib > /home/conda/tmp/meta_{var}_{filename}.txt"'''.format(
            var = variable,
            input_path = input_path,
            filename = filename        )
        print(meta_cmd)
        process = subprocess.Popen(meta_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if ('Error' in str(stderr) or 'Warning' in str(stderr)):
            print(stderr)  
        else:
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
            
                pre_cmd = '''docker run --rm -v {input_path}:/home/conda/ ftt01cdo /bin/bash -c "cdo -seltimestep,{step} /home/conda/tmp/{var}_{filename}.grib /home/conda/tmp/{idx}_{var}_{filename}.grib"'''.format(
                    var = model_varname,
                    step = ts,
                    input_path = input_path,
                    filename = filename,
                    idx = idx
                )
                print(pre_cmd)

                process = subprocess.Popen(pre_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                    
                cmd = '''grib_get_data -w shortName={var} {input_path}tmp/{idx}_{var}_{filename}.grib > {input_path}tmp/{var}_{filename}_{ts}.txt'''.format(
                    idx = idx,
                    filename = filename,
                    input_path = input_path,
                    var = model_varname,
                    ts = ts
                )
                print(cmd)
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()                

print(f"Variable: {variable}")

available_data = glob.glob(f"{args.input_path}{args.variable}/{args.year}/todo/*.grib")

params = [
        [f"{args.input_path}{args.variable}/{args.year}/todo/",
        d.split('/')[-1],
        variable] for d in available_data
]

# create a process pool that uses all cpus
pool = multiprocessing.Pool()
with multiprocessing.Pool(4) as pool:
    pool.map(execute, params)
# close the process pool
pool.close()