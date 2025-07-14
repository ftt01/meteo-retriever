#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys

lib_dir = "/home/daniele/documents/github/ftt01/phd/share/lib"
sys.path.insert( 0, lib_dir )


# In[ ]:


from lib import *


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


output_path = "/media/lacie2022/data/meteo/ecmwf/era5/original/single/"
mkNestedDir( output_path )

lat_min = 43
lat_max = 49
lon_min = 5
lon_max = 17

years = [
    2010,
    2011,
    2012,
    2013,
    2014,
    2015,
    2016,
    2017,
    2018,
    2019,
    2020,
    2021,
    2022
]

variables = ['2m_temperature', 'total_precipitation']

runs = [
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

json_conf['area'] = [ lat_max, lon_min, lat_min, lon_max]


# In[ ]:


def run_download(c_json, var, run, day, month, year):

    c_json['variable'] = var
    c_json['time'] = run
    c_json['day'] = day
    c_json['month'] = month
    c_json['year'] = year

    print(c_json)

    c = cdsapi.Client()

    c.retrieve(
        'reanalysis-era5-single-levels',
        c_json,
        '''{var}_{run}_{year}{month}{day}.grib'''.format(
            var=var,
            run=run[0:2],
            year=year,
            month=month.zfill(2),
            day=day.zfill(2)
        ))


# In[ ]:


def execute(date):
    for run in runs:
        for var in variables:
            run_download(json_conf.copy(), var, run, str(date.day), str(date.month), str(date.year) )


# In[ ]:


import multiprocessing

n_cpus = multiprocessing.cpu_count()

for year in years:
    start_date = dt.datetime.strptime( str(year)+'-01-01', '%Y-%m-%d' )
    end_date = dt.datetime.strptime( str(year)+'-12-31', '%Y-%m-%d' )
    dates = pd.date_range(start_date, end_date, freq='d')
    
    with multiprocessing.Pool(processes=int(n_cpus*0.8)) as pool:
        pool.map(execute, dates)
        
    # close the process pool
    pool.close()

