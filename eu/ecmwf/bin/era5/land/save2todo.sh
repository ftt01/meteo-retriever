#!/bin/bash
vars=("precipitation" "temperature")

for i in {2012..2012}; do
    for v in "${vars[@]}"; do
        screen -dmS "era5_land_${i}_${v}_2todo" bash -c "trap 'echo gotsigint' INT; python3 /home/daniele/documents/github/ftt01/phd/data/meteo/providers/ecmwf/bin/era5/land/grib2todo.py -i /media/lacie2022/data/meteo/ecmwf/era5/land/AA/ -v ${v} -y ${i} > /media/lacie2022/data/meteo/ecmwf/era5/land/AA/era5_land_${i}_${v}_2todo.log; bash";
    done
done
