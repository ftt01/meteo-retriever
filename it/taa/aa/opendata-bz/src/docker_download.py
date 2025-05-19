#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sys import path as syspath
from json import load as jload
from json import loads as jloads
import argparse


# In[ ]:


# from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--remote-debugging-port=9222')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
# chrome_options.binary_location = '/home/daniele/.wdm/chrome/chrome-linux/chrome'

## driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# service = Service(executable_path="/home/daniele/.wdm/chromedriver/chromedriver_linux64/chromedriver")
# driver = webdriver.Chrome(service=service, options=chrome_options)
driver = webdriver.Chrome(options=chrome_options, executable_path='/usr/local/bin/chromedriver')


# In[ ]:


input_parser = argparse.ArgumentParser()
input_parser.add_argument('wdir', type=str)
input_parser.add_argument('configuration_file', type=str)
args = input_parser.parse_args()

wdir = args.wdir
configuration_file = args.configuration_file


# In[ ]:


# ### jload script libraries
# with open(configuration_file) as config_file:
#     configuration = jload(config_file)
#     lib_dirs = configuration["script_libs"]
#     config_file.close()
# for lib_dir in lib_dirs:
#     syspath.insert( 0, lib_dir )  


# In[ ]:


with open(configuration_file) as config_file:
    configuration = jload(config_file)

    project_name = configuration["project_name"]    

    provider_name = configuration["input"]["provider_name"]
    input_timezone_str = configuration["input"]["timezone"]
    input_timezone = pytz.timezone(input_timezone_str)


    # metadata_path = configuration["output"]["metadata"]
    metadata_path = output_path + configuration["output"]["metadata"]
    mkNestedDir(metadata_path)
    output_datetime_format = configuration["output"]["datetime_format"]
    output_timezone_str = configuration["output"]["timezone"]
    output_timezone = pytz.timezone(output_timezone_str)
    method = configuration["output"]["method"]

    method = configuration["output"]["method"]
    script_authors = configuration["script"]["authors"]
    script_version = configuration["script"]["version"]

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
    
    quality_check = configuration["quality_check"]

    # log_path = configuration["log"]["path"]
    log_path = output_path + configuration["log"]["path"]
    mkNestedDir(log_path)
    
    if configuration["log"]["level"] == "info":
        logging_level = logging.INFO
    elif configuration["log"]["level"] == "debug":
        logging_level = logging.DEBUG
    else:
        logging_level = logging.ERROR

    email_notification = configuration["email"]

config_file.close()


# In[ ]:


log_filename = log_path + provider_name + "_download_" +  dt.datetime.now().strftime("%Y%m%dT%H%M%S") + ".log"
print(log_filename)

logging.basicConfig(
    filename = log_filename,
    format = '%(asctime)s - %(message)s',
    filemode = 'a',
    level = logging_level)


# In[ ]:


computation_start = dt.datetime.now()


# In[ ]:


url = "http://dati.retecivica.bz.it/services/meteo/v1/stations"
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')

print(soup.body.string)
stations = jloads(soup.body.string)

driver.close()
driver.quit()

# url = "http://daten.buergernetz.bz.it/services/meteo/v1/sensors/"
# driver.get(url)
# soup = BeautifulSoup(driver.page_source, 'html.parser')

# sensors = jloads(soup.body.string)


# In[ ]:


# stations


# In[ ]:


# url = "http://daten.buergernetz.bz.it/services/meteo/v1/sensors?station_code=89940PG"
# driver.get(url)
# soup = BeautifulSoup(driver.page_source, 'html.parser')

# sensors = jloads(soup.body.string)


# In[ ]:


logging.info( "Project name: " + project_name )
logging.info( "Script authors: " + str(script_authors) )

logging.info( "Provider name: " + provider_name )
logging.info( "Output path: " + output_path )
logging.info( "Log filename path: " + str(log_path) )


# In[ ]:


# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# driver = webdriver.Chrome(service=service, options=chrome_options)
driver = webdriver.Chrome(options=chrome_options, executable_path='/usr/local/bin/chromedriver')


# In[ ]:


counter = 0
for st in stations['features']:
    st_code = st['properties']['SCODE']

    logging.info("Station code: " + st_code)

    # if (st_code in saved_id_ui) & (method == "integrate"):
    #     # print('here')
    #     continue

    url = "http://daten.buergernetz.bz.it/services/meteo/v1/sensors?station_code=" + st_code
    try:
        driver.get(url)
    except Exception as e:
        logging.warning('Missing ' + st_code + ' ' + str(e))
        continue
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    sensors = jloads(soup.body.string)
    # print(sensors)
    for item in sensors:
        sensor_code = item['TYPE']

        logging.info("Sensor code: " + sensor_code)
        if sensor_code == 'Q':
            variable = "streamflow"
            format_data = "float"
        elif sensor_code == 'LT':
            variable = "temperature"
            format_data = "float"
        elif sensor_code == 'N':
            variable = "precipitation"
            format_data = "float"
        elif sensor_code == 'W':
            variable = "hydro_level"
            format_data = "float"
        elif sensor_code == 'WG':
            variable = "wind_velocity"
            format_data = "float"
        elif sensor_code == 'WG.BOE':
            variable = "wind_burst"
            format_data = "float"
        elif sensor_code == 'LF':
            variable = "relative_humidity"
            format_data = "float"
        elif sensor_code == 'LD.RED':
            variable = "pressure"
            format_data = "float"
        elif sensor_code == 'HS':
            variable = "snow_depth"
            format_data = "float"
        elif sensor_code == 'GS':
            variable = "global_radiation"
            format_data = "float"
        elif sensor_code == 'SSTF':
            variable = "suspended_solid"
            format_data = "float"
        elif sensor_code == 'SD':
            variable = "sunshine_duration"
            format_data = "float"
        else:
            continue

        output_path_tmp = output_path + variable + "/"

        provider_id = None
        provider_notes = st['properties']
        
        station_name = st_code
        status = "active"
        x = st['properties']['LONG']
        y = st['properties']['LAT']
        z = st['properties']['ALT']
        station_id = int(update_metadata( st_code, metadata_path + "stations_list.csv", longitude=x, latitude=y, elevation=z ))

        sensor_id = sensor_code
        units = item['UNIT']
        quality_style = None
        datapath = output_path_tmp + st_code + ".csv"
        output_metadata_path = metadata_path + "stations/" + st_code + ".json"

        fill_metadata(wdir+"etc/conf/metadata.json", provider_name, provider_id, provider_notes,
                      station_id, station_name, x, y, z,
                      sensor_id, variable, units, format_data, quality_style, output_datetime_format, datapath,
                      output_metadata_path)

        curr_start_datetime = start_datetime
        # end_datetime = output_timezone.localize( dt.datetime.now() )
        curr_end_datetime = end_datetime

        while curr_end_datetime <= end_datetime:        
            if (end_datetime - curr_start_datetime).days > 90:
                curr_end_datetime = curr_start_datetime + dt.timedelta(days=90)
            else:
                curr_end_datetime = end_datetime

            station_df = download_timeseries(
                st_code, sensor_code, 
                dt.datetime.strftime(curr_start_datetime, format="%Y%m%d"),
                dt.datetime.strftime(curr_end_datetime, format="%Y%m%d"),
                datetime_format=output_datetime_format,
                input_timezone=input_timezone,
                output_timezone=output_timezone )

            if type(station_df) != int:
                data_temp = appendCSV(datapath, station_df)
            
            if curr_end_datetime == end_datetime:
                break

            curr_start_datetime = curr_end_datetime
        
    counter = counter + 1
        
logging.info("Number of saved stations: " + str(counter))


# In[ ]:


driver.close()
driver.quit()


# In[ ]:


with open(log_filename, 'r') as log_file:
    lines = log_file.readlines()
    last_lines = lines[-5:]

    log_file.close()


# In[ ]:


# if email_notification == True:
#     send_email(
#         subject="Meteo AltoAdige updated",
#         body="Started at " + computation_start.strftime(format="%Y-%m-%dT%H:%M:%SZ%z") + 
#             "\nFinish at " + dt.datetime.now().strftime(format="%Y-%m-%dT%H:%M:%SZ%z") +
#             "\nNumber of stations saved: " + str(counter) +
#             "\nConfiguration file: " + jdumps(configuration, indent=2, default=str)
#     )

