$date = Get-Date -Format "yyyy-MM-dd"
$date_dir = Get-Date -Format "yyyyMMdd"

# $date = "2022-01-31"
# $date_dir = "20220131"

#$cloud_dir = '\\smb.scientificnet.org\natec_hyse\Users\Andrea Menapace\meteoData\cosmo_d2_eps\'
$local_dir ='G:\data\meteo\dwd\icon-eu-eps\'
mkdir ${local_dir}${date_dir}
#mkdir ${cloud_dir}${date_dir}

Set-Location ${local_dir}${date_dir}

$hour = "00:00:00"
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 0 --max-time-step 48 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 51 --max-time-step 51 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 54 --max-time-step 54 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 57 --max-time-step 57 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 60 --max-time-step 60 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 63 --max-time-step 63 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 66 --max-time-step 66 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 69 --max-time-step 69 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 72 --max-time-step 72 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 78 --max-time-step 78 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 84 --max-time-step 84 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 90 --max-time-step 90 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 96 --max-time-step 96 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 102 --max-time-step 102 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 108 --max-time-step 108 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 114 --max-time-step 114 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 120 --max-time-step 120 --timestamp ${date}T${hour} --directory /mydata

$hour = "06:00:00"
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 0 --max-time-step 48 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 51 --max-time-step 51 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 54 --max-time-step 54 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 57 --max-time-step 57 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 60 --max-time-step 60 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 63 --max-time-step 63 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 66 --max-time-step 66 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 69 --max-time-step 69 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 72 --max-time-step 72 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 78 --max-time-step 78 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 84 --max-time-step 84 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 90 --max-time-step 90 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 96 --max-time-step 96 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 102 --max-time-step 102 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 108 --max-time-step 108 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 114 --max-time-step 114 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 120 --max-time-step 120 --timestamp ${date}T${hour} --directory /mydata

docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 0 --max-time-step 0 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 6 --max-time-step 6 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 12 --max-time-step 12 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 18 --max-time-step 18 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 24 --max-time-step 24 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 30 --max-time-step 30 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 36 --max-time-step 36 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 42 --max-time-step 42 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 48 --max-time-step 48 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 54 --max-time-step 54 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 60 --max-time-step 60 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 66 --max-time-step 66 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 72 --max-time-step 72 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 78 --max-time-step 78 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 84 --max-time-step 84 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 96 --max-time-step 96 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 102 --max-time-step 102 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 108 --max-time-step 108 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 114 --max-time-step 114 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 120 --max-time-step 120 --timestamp ${date}T${hour} --directory /mydata

$hour = "12:00:00"
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 0 --max-time-step 48 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 51 --max-time-step 51 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 54 --max-time-step 54 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 57 --max-time-step 57 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 60 --max-time-step 60 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 63 --max-time-step 63 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 66 --max-time-step 66 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 69 --max-time-step 69 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 72 --max-time-step 72 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 78 --max-time-step 78 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 84 --max-time-step 84 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 90 --max-time-step 90 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 96 --max-time-step 96 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 102 --max-time-step 102 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 108 --max-time-step 108 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 114 --max-time-step 114 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec,snow_con --min-time-step 120 --max-time-step 120 --timestamp ${date}T${hour} --directory /mydata

$hour = "18:00:00"
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 0 --max-time-step 48 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 51 --max-time-step 51 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 54 --max-time-step 54 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 57 --max-time-step 57 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 60 --max-time-step 60 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 63 --max-time-step 63 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 66 --max-time-step 66 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 69 --max-time-step 69 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 72 --max-time-step 72 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 78 --max-time-step 78 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 84 --max-time-step 84 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 90 --max-time-step 90 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 96 --max-time-step 96 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 102 --max-time-step 102 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 108 --max-time-step 108 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 114 --max-time-step 114 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields t_2m,tot_prec --min-time-step 120 --max-time-step 120 --timestamp ${date}T${hour} --directory /mydata

docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 0 --max-time-step 0 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 6 --max-time-step 6 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 12 --max-time-step 12 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 18 --max-time-step 18 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 24 --max-time-step 24 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 30 --max-time-step 30 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 36 --max-time-step 36 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 42 --max-time-step 42 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 48 --max-time-step 48 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 54 --max-time-step 54 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 60 --max-time-step 60 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 66 --max-time-step 66 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 72 --max-time-step 72 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 78 --max-time-step 78 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 84 --max-time-step 84 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 96 --max-time-step 96 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 102 --max-time-step 102 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 108 --max-time-step 108 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 114 --max-time-step 114 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu-eps --single-level-fields snow_con --min-time-step 120 --max-time-step 120 --timestamp ${date}T${hour} --directory /mydata

#Copy-Item -Path ${local_dir}* -Destination ${cloud_dir} -force -recurse

#Remove-Item -r -fo ${local_dir}*