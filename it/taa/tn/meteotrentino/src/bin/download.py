#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys

lib_dir = "/home/daniele/documents/github/ftt01/phd/share/lib"
sys.path.insert( 0, lib_dir )


# In[ ]:


from lib import *


# In[ ]:


import logging


# In[ ]:


import xmltodict
import requests
from pathlib import Path


# In[ ]:


def appendCSV( filename, data, datetime_format="%Y-%m-%dT%H:%M:%SZ%z" ):

    # print(os.path.exists(filename))

    # old_data = pd.DataFrame()
    if os.path.exists(filename):
        # print("FILE EXIST: " + filename)
        with open( filename ) as f:
            old_data = pd.read_csv(f, header=0, skiprows=0, parse_dates=True, names=['values'])
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

    # print(data)
    data.dropna(subset=['datetime'], inplace=True)
    data.sort_values(by=['datetime'], inplace=True)
    data['datetime'] = [ dt.datetime.strftime(c_dt, format=datetime_format) for c_dt in data['datetime'] ]

    data = data.set_index('datetime')
    data = data[data.index.notnull()]

    data.to_csv( filename )

    return data


# In[ ]:


def decode_json(
    station, json_complete, variable, format_data, datetime_format, current_timezone, 
    quality_check, var_1, var_2, var_3, output_path, metadata_path):

    logging.debug(var_1)
    # print(json_complete)

    provider_id = None
    provider_notes = None
    station_id = station['codice']
    station_name = station['nome']

    x = station['longitudine']
    y = station['latitudine']
    z = station['quota']

    if json_complete['datiOggi'][var_1] != None:
        # dict_temp = {}

        station_df = pd.DataFrame()
        datetimes = []
        values = []

        for el in json_complete['datiOggi'][var_1][var_2]:

            tmp_dt = dt_parser.parse(el['data'])
            # tmp_dt = tmp_dt.replace(tzinfo=tz.gettz(current_timezone))
            # datetimes.append( tmp_dt.fromtimestamp(tmp_dt.timestamp()) )
            datetimes.append( tmp_dt.replace(tzinfo=tz.gettz(current_timezone)) )
            values.append( el[var_3] )

        #     # print(el['data'])

        #     tmp_dt = dt_parser.parse(el['data'], tzinfos=tzinfos)
        #     datetimes.append( tmp_dt.fromtimestamp(tmp_dt.timestamp(), tz=dt.timezone.utc) )
        #     values.append( el[var_3] )

        #     # dt = pd.to_datetime(el['data'], format=datetime_format).to_pydatetime()
        #     # dt.replace(tzinfo=tz.gettz('Europe/Berlin'))
        #     # dt = dt.astimezone(tz.gettz("UTC")).replace(tzinfo=None)

        #     # dict_temp[dt] = el[var_3]
        
        # # data_temp = appendCSV(out_temperature + st['codice'] + ".csv", dict_temp )

        station_df['datetime'] = datetimes
        station_df['values'] = values

        station_df = station_df.set_index('datetime')

        sensor_id = station['codice'] + "_" + variable
        
        units = None
        if variable == "wind_velocity":
            units = el['@UM_VV']
        if variable == "wind_dir":
            units = el['@UM_DV']
        if units == None:
            units = el['@UM']
            
        datapath = output_path + station['codice'] + ".csv"
        metadata_path = metadata_path + station['codice'] + ".json"

        fill_metadata("../../etc/conf/metadata.json", provider_name, provider_id, provider_notes,
                station_id, station_name, x, y, z,
                sensor_id, variable, units, format_data, quality_check, datetime_format, datapath, 
                metadata_path)

        return appendCSV( datapath, station_df, datetime_format )
    
    else:
        return 0


# In[ ]:


try:
    input_parser = argparse.ArgumentParser()
    input_parser.add_argument('configuration_file', type=str)
    args = input_parser.parse_args()
    configuration_file = args.configuration_file
except:
    configuration_file = "../../etc/conf/config.json"


# In[ ]:


with open(configuration_file) as config_file:
    configuration = json.load(config_file)

    provider_name = configuration["provider_name"]
    output_path = configuration["output_path"]
    mkNestedDir(output_path)
    metadata_path = configuration["metadata_path"]
    mkNestedDir(metadata_path)
    log_path = Path( configuration["log_path"] )
    mkNestedDir(log_path.parent.absolute())

    datetime_format = configuration["datetime_format"]
    current_tz = configuration["timezone"]
    quality_check = configuration["quality_check"]

    if configuration["logging_level"] == "info":
        logging_level = logging.INFO
    elif configuration["logging_level"] == "debug":
        logging_level = logging.DEBUG
    else:
        logging_level = logging.ERROR

config_file.close()


# In[ ]:


logging.basicConfig(
    # filename=log_path + dt.datetime.today().strftime("%Y%m%d%H%M%S") + ".log",
    filename = log_path,
    format = '%(asctime)s - %(message)s',
    filemode = 'a',
    level = logging_level)


# In[ ]:


url = "http://dati.meteotrentino.it/service.asmx/listaStazioni"

data = requests.get(url)
xpars = xmltodict.parse(data.text)
json_complete = json.loads(json.dumps(xpars))
stations = json_complete['ArrayOfAnagrafica']['anagrafica']


# In[ ]:


mycodes = []
n_codes = 0
for st in stations:
    mycodes.append( st['codice'] )
    n_codes = n_codes + 1

logging.info("Number of stations online: " + str(n_codes))


# In[ ]:


for st in stations:

    logging.debug("Downloading.." + st['codice'])
    url = "http://dati.meteotrentino.it/service.asmx/ultimiDatiStazione?codice={station_code}"
    logging.debug(url.format(station_code=st['codice']))
    
    data = requests.get(url.format(station_code=st['codice']))
    
    xpars = xmltodict.parse(data.text)
    json_complete = json.loads(json.dumps(xpars))

    logging.debug("JSON data: " + str(json_complete))
    decode_json(
        st, json_complete, "temperature", "float", datetime_format, current_tz, quality_check, 
        "temperature", "temperatura_aria", "temperatura", 
        output_path + "temperature/", metadata_path)
    decode_json(
        st, json_complete, "precipitation", "float", datetime_format, current_tz, quality_check,
        "precipitazioni", "precipitazione", "pioggia", 
        output_path + "precipitation/", metadata_path)
    decode_json(
        st, json_complete, "wind_velocity", "float", datetime_format, current_tz, quality_check,
        "venti", "vento_al_suolo", "v", 
        output_path + "wind/", metadata_path)
    decode_json(
        st, json_complete, "wind_dir", "float", datetime_format, current_tz, quality_check,
        "venti", "vento_al_suolo", "d", 
        output_path + "wind_dir/", metadata_path)
    decode_json(
        st, json_complete, "global_radiation", "float", datetime_format, current_tz, quality_check,
        "radiazione", "radiazioneglobale", "rsg", 
        output_path + "radiation/", metadata_path)
    decode_json(
        st, json_complete, "relative_humidity", "float", datetime_format, current_tz, quality_check,
        "umidita_relativa", "umidita_relativa", "rh", 
        output_path + "relative_humidity/", metadata_path)


# In[ ]:


logging.info("DONE!")

