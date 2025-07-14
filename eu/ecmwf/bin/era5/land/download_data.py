#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import sys

lib_dir = "/home/daniele/documents/github/ftt01/phd/share/lib"
sys.path.insert( 0, lib_dir )


# In[ ]:


from lib import mkNestedDir, dt, pd


# In[ ]:


import cdsapi


# In[ ]:


############## example - 20230602

# import cdsapi

# c = cdsapi.Client()

# c.retrieve(
#     'reanalysis-era5-single-levels',
#     {
#         'product_type': 'reanalysis',
#         'variable': [
#             '2m_temperature', 'total_precipitation',
#         ],
#         'year': '2010',
#         'month': '01',
#         'day': '01',
#         'time': [
#             '00:00', '01:00', '02:00',
#             '03:00', '04:00', '05:00',
#             '06:00', '07:00', '08:00',
#             '09:00', '10:00', '11:00',
#             '12:00', '13:00', '14:00',
#             '15:00', '16:00', '17:00',
#             '18:00', '19:00', '20:00',
#             '21:00', '22:00', '23:00',
#         ],
#         'area': [
#             47, 5, 43,
#             17,
#         ],
#         'format': 'grib',
#     },
#     'download.grib')


# In[ ]:


output_path = "/media/lacie2022/data/meteo/ecmwf/era5/land/AA/"
mkNestedDir( output_path )

# lat_min = 43
# lat_max = 49
# lon_min = 5
# lon_max = 17

lat_min = 45
lat_max = 47.5
lon_min = 9.80
lon_max = 13

# lat_min = 45.00
# lat_max = 47.50
# lon_min = 12.40
# lon_max = 12.40

years = [
    # 1990,
    # 1991,
    # 1992,
    # 1993,
    # 1994,
    # 1995,
    # 1996,
    # 1997,
    # 1998,
    # 1999,
    # 2000,
    # 2001,
    # 2002,
    # 2003,
    # 2004,
    # 2005,
    # 2006,
    # 2007,
    # 2008,
    # 2009,
    # 2010,
    # 2011,
    # 2012,
    # 2013,
    2014
    # 2015,
    # 2016,
    # 2017,
    # 2018,
    # 2019,
    # 2020,
    # 2021,
    # 2022,
    # 2023
]

# variables = [
#     '10m_u_component_of_wind', '10m_v_component_of_wind', '2m_dewpoint_temperature',
#     '2m_temperature', 'evaporation_from_bare_soil', 'evaporation_from_open_water_surfaces_excluding_oceans',
#     'evaporation_from_the_top_of_canopy', 'evaporation_from_vegetation_transpiration', 'forecast_albedo',
#     'leaf_area_index_high_vegetation', 'leaf_area_index_low_vegetation', 'potential_evaporation',
#     'runoff', 'skin_temperature', 'snow_albedo',
#     'snow_cover', 'snow_density', 'snow_depth',
#     'snow_depth_water_equivalent', 'snow_evaporation', 'snowfall',
#     'snowmelt', 'sub_surface_runoff', 'surface_latent_heat_flux',
#     'surface_net_solar_radiation', 'surface_net_thermal_radiation', 'surface_pressure',
#     'surface_runoff', 'surface_sensible_heat_flux', 'surface_solar_radiation_downwards',
#     'surface_thermal_radiation_downwards', 'temperature_of_snow_layer', 'total_evaporation',
#     'total_precipitation'
# ]

variables = [
    'total_precipitation'
]

hours = [
    "00:00",
    "01:00",
    "02:00",
    "03:00",
    "04:00",
    "05:00",
    "06:00",
    "07:00",
    "08:00",
    "09:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
    "18:00",
    "19:00",
    "20:00",
    "21:00",
    "22:00",
    "23:00",
]


# In[ ]:


os.chdir( output_path )


# In[ ]:


json_conf = {
    'product_type': 'reanalysis',
    'format': 'grib'
}

json_conf['area'] = [ lat_max, lon_min, lat_min, lon_max ]


# In[ ]:


def run_download(c_json, var, hours, day, month, year):

    c_json['variable'] = var
    c_json['time'] = hours
    c_json['day'] = day
    c_json['month'] = month
    c_json['year'] = year

    print(c_json)

    c = cdsapi.Client()

    try:
        c.retrieve(
            'reanalysis-era5-land',
            c_json,
            '''{var}_{year}{month}{day}.grib'''.format(
                var=var,
                year=year,
                month=month.zfill(2),
                day=day.zfill(2)
            ))
    except:
        run_download(c_json, var, hours, day, month, year)


# In[ ]:


def execute(args):
    var, date = args
    # for run in runs:
    # for var in variables:
    run_download(
        json_conf.copy(),
        var,
        hours,
        str(date.day),
        str(date.month),
        str(date.year) )


# In[ ]:


import multiprocessing

n_cpus = multiprocessing.cpu_count()

for year in years:
    for var in variables:
        start_date = dt.datetime.strptime( str(year)+'-01-01', '%Y-%m-%d' )
        end_date = dt.datetime.strptime( str(year)+'-12-31', '%Y-%m-%d' )
        dates = pd.date_range(start_date, end_date, freq='d')
        args = [(var,i) for i in dates]
        with multiprocessing.Pool(processes=int(n_cpus*0.8)) as pool:
            pool.map(execute, args)
        
        # close the process pool
        pool.close()
    
# close the process pool
pool.close()