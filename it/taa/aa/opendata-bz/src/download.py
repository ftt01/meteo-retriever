#!/usr/bin/env python
# coding: utf-8

import argparse
import datetime as dt
import json
import logging
import sys
import urllib3
import pandas as pd
import numpy as np
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dateutil import parser as dt_parser
import pytz

# Specific imports from json module
from json import load as jload, loads as jloads, dump as jdump

###########

def getPathFromFilepath(existGDBPath):
    return os.path.dirname(os.path.abspath(existGDBPath))
    
def mkNestedDir(dirTree):
    # from pathlib import Path
    # Path(dirTree).mkdir(parents=True, exist_ok=True)
    os.makedirs(dirTree, exist_ok=True)

def fill_metadata(_provider_name_, _provider_id_, _provider_notes_,
                  _station_id_, _station_name_, _x_, _y_, _z_,
                  _sensor_id_, _variable_, _units_, _format_, _quality_style_: dict, _datetime_format_, _datapath_,
                  path_to_save_metadata):

    if os.path.exists(path_to_save_metadata):
        # logging.debug( "Metadata file: " + path_to_save_metadata )
        # logging.debug( "Metadata: " + metadata )
        try:
            with open(path_to_save_metadata) as f:
                metadata = jload(f)
                f.close()
            data_exist = True
        except:
            os.remove(path_to_save_metadata)
            data_exist = False
    
    else:
        data_exist = False

    if data_exist == True:
        
        sensors = metadata['sensors']

        new_sensors = []
        for item in sensors:
            if not(_sensor_id_ in item['id']):
                new_sensors.append(item)

        sensor = {}
        sensor["id"] = _sensor_id_
        sensor["status"] = None
        sensor["variable"] = _variable_
        sensor["units"] = _units_
        sensor["format"] = _format_
        sensor["quality"] = _quality_style_
        sensor["datetime_format"] = _datetime_format_
        sensor["datapath"] = _datapath_
        sensor['start_date'] = None
        sensor['end_date'] = None
        sensor['step_mins'] = None

        new_sensors.append(sensor)
        metadata['sensors'] = new_sensors
    else:
        metadata = {
            "id": "_station_id_",
            "name": "_station_name_",
            "provider": {
                "name": "_provider_name_",
                "id": "_provider_id_",
                "notes": "_provider_notes_"
            },
            "location": {
                "x": "_x_",
                "y": "_y_",
                "z": "_z_",
                "EPSG": "4326"
            },
            "sensors": []
        }

        metadata['provider']['name'] = _provider_name_
        metadata['provider']['id'] = _provider_id_
        metadata['provider']['notes'] = _provider_notes_

        metadata['id'] = _station_id_
        metadata['name'] = _station_name_
        metadata['location']['x'] = _x_
        metadata['location']['y'] = _y_
        metadata['location']['z'] = _z_

        sensors = []
        sensor = {}
        sensor["id"] = _sensor_id_
        sensor["status"] = None
        sensor["variable"] = _variable_
        sensor["units"] = _units_
        sensor["format"] = _format_
        sensor["quality"] = _quality_style_
        sensor["datetime_format"] = _datetime_format_
        sensor["datapath"] = _datapath_
        sensor['start_date'] = None
        sensor['end_date'] = None
        sensor['step_mins'] = None

        sensors.append(sensor)

        metadata['sensors'] = sensors

        # print(metadata)
        # print('HERE')

    if path_to_save_metadata != None:

        mkNestedDir( getPathFromFilepath(path_to_save_metadata) )

        with open(path_to_save_metadata, 'w') as fp:
            jdump(metadata, fp, indent=4)
            fp.close()

def appendCSV( filename, data ):

    # print(os.path.exists(filename))

    # old_data = pd.DataFrame()
    if os.path.exists(filename):
        # logging.debug("FILE EXIST: " + filename)
        with open( filename ) as f:
            old_data = pd.read_csv(f, header=0, skiprows=0, names=['values'])
            # old_data['datetime'] = 

            old_data.index.name = 'datetime'
            old_data.dropna(inplace=True)

            data = data.reset_index()
            old_data = old_data.reset_index()

            data = pd.concat( [ data[data['datetime'].isin(old_data['datetime']) == False], old_data ], ignore_index=True )
            # print(data)

            f.close()
    else:
        mkNestedDir( getPathFromFilepath(filename) )
        data = data.reset_index()

    data.dropna(subset=['datetime'], inplace=True)
    data.sort_values(by=['datetime'], inplace=True)

    data = data.set_index('datetime')
    data = data[data.index.notnull()]

    # print(data)
    # print(filename)

    data.to_csv( filename )

    return data

def download_timeseries(
    station_code, sensor_code, 
    from_YYYYmmdd=None, to_YYYYmmdd=None, 
    datetime_format="%Y-%m-%dT%H:%M:%SZ%z",
    input_timezone=dt.timezone.utc,
    output_timezone=dt.timezone.utc):

    if from_YYYYmmdd == None:
        url = "http://daten.buergernetz.bz.it/services/meteo/v1/timeseries?station_code={station_code}&sensor_code={sensor_code}"
        
        url = url.format( 
            station_code=station_code,
            sensor_code=sensor_code
            )
    else:
        url = "http://daten.buergernetz.bz.it/services/meteo/v1/timeseries?station_code={station_code}&sensor_code={sensor_code}&date_from={from_YYYYmmdd}0000&date_to={to_YYYYmmdd}2359"

        url = url.format( 
            station_code=station_code,
            sensor_code=sensor_code,
            from_YYYYmmdd=from_YYYYmmdd,
            to_YYYYmmdd=to_YYYYmmdd
            )

    logging.debug("Downloading: " + url)

    http = urllib3.PoolManager(1)
    
    station_data = http.request('GET', url)
    try:
        station_data = jloads(station_data.data)
    except:
        return 0

    station_df = pd.DataFrame()
    datetimes = []
    values = []

    if station_data == []:
        return 0
    else:
        for data in station_data:
            curr_dt = dt_parser.parse(data['DATE'], tzinfos={"CET":+3600,"CEST":+7200})
            print("Date with input TZ: " + str(curr_dt))
            curr_dt = curr_dt.astimezone( output_timezone )                
            datetimes.append( curr_dt.strftime(datetime_format) )
            values.append( data['VALUE'] )

        station_df['datetime'] = datetimes
        station_df['values'] = values

        return station_df.set_index('datetime')

def update_metadata( st_code, id_list, latitude=None, longitude=None, elevation=None ):

    try:
        old_metadata = pd.read_csv( id_list )
        old_metadata = old_metadata.loc[:,['ID','ID_UI','lat','lon','elevation']]

        c_ids = old_metadata['ID'].to_list()
        curr_id = np.max(c_ids) + 1
    except:
        old_metadata = pd.DataFrame( columns=['ID','ID_UI','lat','lon','elevation'] )
        curr_id = 1
    
    if st_code in old_metadata['ID_UI'].to_list():

        curr_id = old_metadata[old_metadata['ID_UI']==st_code]['ID']

        old_metadata.set_index('ID',inplace=True)
        old_metadata.to_csv( id_list )

    else:
        df2 = pd.DataFrame(
            [[curr_id,st_code,latitude,longitude,elevation]],
            columns=['ID','ID_UI','lat','lon','elevation'])
        new_metadata = pd.concat([df2, old_metadata])
        new_metadata = new_metadata.sort_values('ID')

        new_metadata.set_index('ID',inplace=True)
    
        new_metadata.to_csv( id_list )
    
    return curr_id

def main(configuration_file, output_path):

    mkNestedDir(output_path)

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    # Initialize the Chrome driver
    driver = webdriver.Chrome(options=chrome_options, executable_path='/usr/local/bin/chromedriver')

    # Load configuration
    project_name = configuration["project_name"]
    provider_name = configuration["input"]["provider_name"]
    input_timezone_str = configuration["input"]["timezone"]
    input_timezone = pytz.timezone(input_timezone_str)
    
    metadata_path = output_path + configuration["output"]["metadata"]
    mkNestedDir(metadata_path)
    output_datetime_format = configuration["output"]["datetime_format"]
    output_timezone_str = configuration["output"]["timezone"]
    output_timezone = pytz.timezone(output_timezone_str)
    method = configuration["output"]["method"]
    script_authors = configuration["script"]["authors"]
    script_version = configuration["script"]["version"]

    start_date = configuration["start_date"]
    try:
        start_datetime = dt.datetime.strptime(start_date, "%Y%m%d")
    except:
        start_datetime = dt.datetime.today()
        start_date = dt.datetime.strftime(start_datetime, format="%Y%m%d")

    end_date = configuration["end_date"]
    try:
        end_datetime = dt.datetime.strptime(end_date, "%Y%m%d")
    except:
        end_datetime = dt.datetime.today()
        end_date = dt.datetime.strftime(end_datetime, format="%Y%m%d")

    quality_check = configuration["quality_check"]
    log_path = output_path + configuration["log"]["path"]
    mkNestedDir(log_path)

    if configuration["log"]["level"] == "info":
        logging_level = logging.INFO
    elif configuration["log"]["level"] == "debug":
        logging_level = logging.DEBUG
    else:
        logging_level = logging.ERROR

    email_notification = configuration["email"]

    # Set up logging
    log_filename = log_path + provider_name + "_download_" + dt.datetime.now().strftime("%Y%m%dT%H%M%S") + ".log"
    logging.basicConfig(
        filename=log_filename,
        format='%(asctime)s - %(message)s',
        filemode='a',
        level=logging_level)

    computation_start = dt.datetime.now()

    # Fetch stations data
    url = "http://dati.retecivica.bz.it/services/meteo/v1/stations"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    stations = jloads(soup.body.string)
    driver.close()
    driver.quit()

    # Log initial information
    logging.info("Project name: " + project_name)
    logging.info("Script authors: " + str(script_authors))
    logging.info("Provider name: " + provider_name)
    logging.info("Output path: " + output_path)
    logging.info("Log filename path: " + str(log_path))

    # Reinitialize the Chrome driver
    driver = webdriver.Chrome(options=chrome_options, executable_path='/usr/local/bin/chromedriver')

    counter = 0
    for st in stations['features']:
        st_code = st['properties']['SCODE']
        logging.info("Station code: " + st_code)

        url = "http://daten.buergernetz.bz.it/services/meteo/v1/sensors?station_code=" + st_code
        try:
            driver.get(url)
        except Exception as e:
            logging.warning('Missing ' + st_code + ' ' + str(e))
            continue
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        sensors = jloads(soup.body.string)

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
            station_id = int(update_metadata(st_code, metadata_path + "stations_list.csv", longitude=x, latitude=y, elevation=z))

            sensor_id = sensor_code
            units = item['UNIT']
            quality_style = None
            datapath = output_path_tmp + st_code + ".csv"
            output_metadata_path = metadata_path + "stations/" + st_code + ".json"

            fill_metadata(provider_name, provider_id, provider_notes,
                          station_id, station_name, x, y, z,
                          sensor_id, variable, units, format_data, quality_style, output_datetime_format, datapath,
                          output_metadata_path)

            curr_start_datetime = start_datetime
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
                    output_timezone=output_timezone)

                if type(station_df) != int:
                    data_temp = appendCSV(datapath, station_df)

                if curr_end_datetime == end_datetime:
                    break

                curr_start_datetime = curr_end_datetime

        counter = counter + 1

    logging.info("Number of saved stations: " + str(counter))

    driver.close()
    driver.quit()

    with open(log_filename, 'r') as log_file:
        lines = log_file.readlines()
        last_lines = lines[-5:]

    log_file.close()

if __name__ == "__main__":

    # Parse command line arguments
    input_parser = argparse.ArgumentParser()

    input_parser.add_argument('--configuration_file', type=str, default="/home/chromedriver/etc/conf/config.json", required=False)
    input_parser.add_argument('--output_path', type=str, default="/home/chromedriver/output/", required=False)
    input_parser.add_argument('--no-docker', action='store_true', help='Disable Docker')
    args = input_parser.parse_args()

    with open(args.configuration_file) as config_file:
        configuration = jload(config_file)
    
        if args.no_docker:
            output_path = configuration['output']['path']
        else:
            output_path = args.output_path
            print("test")

        main(configuration, output_path)
        
        config_file.close()