### Description
The postprocess of DWD results are saved in this directory.
The directories are 2: data and logs.
	1. data: contains the data organized as ***./data/main_basin/B001/R003/variable/type_of_data/points/date.csv***
		- data: the main folder
		- main_basin [e.g., alto_adige]: the basin that physically contains all the area of interest
		- B001: subbasin key_name
		- R003: release
		- variable [e.g., temperature]
		- type_of_data: ensemble or deterministic
		- points: id of the point or 'spatial_mean'
		- date.csv: name of the file with the date when the event starts  
	2. logs: all logs of the postprocess and the stats
## run the docker to crop
docker run -it -v /media/lacie2022/data/meteo/dwd/icon-d2-eps/extraction_alps/data/:/home/icon-d2-eps/data/ --entrypoint cdo cdo-ftt_cdo -f grb2 -sellonlatbox,6,7,45,46 regridded_icon-d2-eps_germany_icosahedral_single-level_2022100100_000_2d_t_2m.grib2 regridded_icon-d2-eps_germany_icosahedral_single-level_2022100100_000_2d_t_2m.grib2