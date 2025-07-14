#!/bin/bash
vars=("precipitation" "temperature")

for i in {1990..2023}; do
    for v in "${vars[@]}"; do
        screen -dmS "era5_land_${i}_${v}_2DB" bash -c "trap 'echo gotsigint' INT; python3 /home/daniele/documents/github/ftt01/phd/data/meteo/providers/ecmwf/bin/era5/land/txt2DB.py -i /media/lacie2022/data/meteo/ecmwf/era5/land/AA/ -v ${v} -y ${i} > /media/lacie2022/data/meteo/ecmwf/era5/land/AA/era5_land_${i}_${v}_2DB.log; bash";
    done
done