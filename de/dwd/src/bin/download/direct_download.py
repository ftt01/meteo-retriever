#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys

lib_dir = "/home/daniele/documents/github/ftt01/phd/share/lib"
sys.path.insert( 0, lib_dir )


# In[ ]:


from lib import *


# In[ ]:


import argparse

import requests
import bz2


# ## takes in input the JSON config file

# In[ ]:


try:
    input_parser = argparse.ArgumentParser()
    input_parser.add_argument('configuration_file', type=str)
    args = input_parser.parse_args()
    jsonConfig = args.configuration_file
except:
    configuration_file = "../../etc/conf/download/dwd_de_icon-d2-eps_config.json"


# In[ ]:


with open(jsonConfig) as config_file:
    configuration = json.load(config_file)

    reference_name = configuration["reference_name"]
    basepath_provider = configuration["basepath_provider"]
    basename_gribfile = configuration["basename_gribfile"]

    ensembles_cardinality = configuration["ensembles_cardinality"]
    forecast_hours = int(configuration["forecast_hours"])
    forecast_hours_step = int(configuration["forecast_hours_step"])

    release_delay = int(configuration["release_delay"])
    release_time = [int(el) for el in configuration["release_time"].strip("[]").split(',')]

    out_path = configuration["out_path"]
    log_path = configuration["log_path"]

    variables = configuration["variables"]
  
    hour_now = int(dt.datetime.utcnow().hour)
    print("Current time: " + str(hour_now) )

    date_to_download = None
    init_hour = None

    if hour_now <= release_time[0] + release_delay:
        date_now = (dt.datetime.utcnow() - timedelta(days=1)).strftime('%Y%m%d')
        currentReleaseHour = release_time[len(release_time) - 1]
        if currentReleaseHour == 1:
            init_hour = "0" + str(currentReleaseHour)
        else:
            init_hour = str(currentReleaseHour)
    else:
        date_now = dt.datetime.utcnow().strftime('%Y%m%d')
        for t in release_time:
            if hour_now >= t + release_delay:
                if len(str(t)) == 1:
                    init_hour = "0" + str(t)
                else:
                    init_hour = str(t)
        date_to_download = date_now + init_hour

    print( "Release delay: " + str(release_delay) )
    print( "Current date: " + str(date_now) )
    print( "To download date: " + str(date_to_download) )

    log_file = log_path + date_to_download + "_" + reference_name + ".txt"
    print( "Log file location: " + str(log_file) )

    for v in list(variables):

        for e in range(0,forecast_hours + 1,forecast_hours_step):

            url = '''{basepath_provider}{init_hour}/{var}/{basename_gribfile}_{date_with_hour}_{three_digit_forecast_hours}_2d_{var}.grib2.bz2'''
            grib_filepath = '''{out_path}{date}/{var}/'''
            grib_filename = '''{grib_filepath}{date_with_hour}.grib2'''

            three_digit_forecast_hours = ""
            zeros = 3 - len(str(e))
            for i in range(zeros):
                three_digit_forecast_hours += "0"
            three_digit_forecast_hours += str(e)

            URL = url.format(basepath_provider=basepath_provider,
                                init_hour=init_hour,
                                var=v,
                                basename_gribfile=basename_gribfile,
                                date_with_hour=date_to_download,
                                three_digit_forecast_hours=three_digit_forecast_hours)

            # print( "Current URL: " + URL)

            r = requests.get(URL, allow_redirects=True)
            grbfile = bz2.decompress(r.content)
            grib_filepath = grib_filepath.format(out_path=out_path,
                                                    date=date_to_download,
                                                    var=v)
            
            os.makedirs(grib_filepath, exist_ok=True)

            grib_name = grib_filename.format(grib_filepath=grib_filepath,
                                                date_with_hour=(dt.datetime.strptime(date_now + init_hour, '%Y%m%d%H') + dt.timedelta(seconds=3600 * int(e))).strftime('%Y%m%d%H'))

            print( "Current file saving: " + grib_name )
            open(grib_name, 'wb').write(grbfile)           

