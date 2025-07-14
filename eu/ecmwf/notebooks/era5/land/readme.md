##### ERA5 land
## to extract from grib to DB
#!/bin/bash
directory="./"
for file in "$directory"/*; do
    if [[ -f "$file" ]]; then
        filename=$(basename "$file")
        screen -dmS "era5_land" bash -c "trap 'echo gotsigint' INT; python3 /home/daniele/documents/github/ftt01/phd/data/meteo/providers/ecmwf/bin/era5/land/grib2db.py -f $filename; bash"
    fi
done
## to extract from DB use the lib