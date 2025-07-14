#!/bin/bash

# Define the source path and the target directory
source_path="/media/lacie2022/data/meteo/ecmwf/era5/land/AA/update202405/temperature"
target_directory="/media/lacie2022/data/meteo/ecmwf/era5/land/AA/temperature"

# Check if the target directory exists; if not, create it
if [ ! -d "$target_directory" ]; then
    mkdir -p "$target_directory"
fi

# Loop through all directories in the source path
for dir in "$source_path"/*; do
    if [ -d "$dir" ]; then
        # Extract the last 4 characters from the directory name
        subdir=$(basename "$dir")
        subdir=${subdir: -4}
        
        # Create the target subdirectory if it doesn't exist
        if [ ! -d "$target_directory/$subdir" ]; then
            mkdir -p "$target_directory/$subdir"
        fi
        
        # Enter each directory and copy all .grib files to the target subdirectory
        find "$dir" -maxdepth 1 -type f -name "*.grib" -exec mv {} "$target_directory/$subdir" \;
    fi
done

echo "All .grib files have been copied to $target_directory."
