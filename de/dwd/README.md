## direct_download.ipynb
This download the data directly in accordance with the configuration file specified.
```
cd /home/daniele/documents/github/ftt01/phd/data/meteo/providers/dwd/src/bin/ && 
python3 direct_download.py ../../etc/conf/download/dwd_de_icon-d2-eps_config.json
```

## extract_grib2.ipynb
This extract to CSV the data directly in accordance with the configuration file specified.
```
cd /home/daniele/documents/github/ftt01/phd/data/meteo/providers/dwd/src/bin/ && 
python3 extract_grib2.py ../../etc/conf/extraction/config.json
```

## postprocess.ipynb
This extract derivates [mean, median, etc..] from CSV data, directly in accordance with the configuration file specified.
```
cd /home/daniele/documents/github/ftt01/phd/data/meteo/providers/dwd/src/bin/ && 
python3 postprocess.py ../../etc/conf/extraction/postprocess.json
```

## extract_data.py
### CSV
FOR EACH FILE GRIB2
1. open with rasterio the grib > xarray format
2. select only the region of interest (B001) and transform to DataFrame
3. create a new DataFrame with lat,lon,band and datetime as column, the data as lines
4. extract_on_subbasins
    a. 