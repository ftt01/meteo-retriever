$date = Get-Date -Format "yyyy-MM-dd"
$date_dir = Get-Date -Format "yyyyMMdd"

# $date = "2022-01-31"
# $date_dir = "20220131"

#$cloud_dir = '\\smb.scientificnet.org\natec_hyse\Users\Andrea Menapace\meteoData\cosmo_d2_eps\'
$local_dir ='G:\data\meteo\dwd\icon-eu\'
mkdir ${local_dir}${date_dir}
#mkdir ${cloud_dir}${date_dir}

Set-Location ${local_dir}${date_dir}

$hour = "00:00:00"
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 78 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 81 --max-time-step 81 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 84 --max-time-step 84 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 87 --max-time-step 87 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 90 --max-time-step 90 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 93 --max-time-step 93 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 96 --max-time-step 96 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 99 --max-time-step 99 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 102 --max-time-step 102 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 105 --max-time-step 105 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 108 --max-time-step 108 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 111 --max-time-step 111 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 114 --max-time-step 114 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 117 --max-time-step 117 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 120 --max-time-step 120 --timestamp ${date}T${hour} --directory /mydata

$hour = "03:00:00"
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 78 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 81 --max-time-step 81 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 84 --max-time-step 84 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 87 --max-time-step 87 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 90 --max-time-step 90 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 93 --max-time-step 93 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 96 --max-time-step 96 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 99 --max-time-step 99 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 102 --max-time-step 102 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 105 --max-time-step 105 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 108 --max-time-step 108 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 111 --max-time-step 111 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 114 --max-time-step 114 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 117 --max-time-step 117 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 120 --max-time-step 120 --timestamp ${date}T${hour} --directory /mydata

$hour = "06:00:00"
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 78 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 81 --max-time-step 81 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 84 --max-time-step 84 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 87 --max-time-step 87 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 90 --max-time-step 90 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 93 --max-time-step 93 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 96 --max-time-step 96 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 99 --max-time-step 99 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 102 --max-time-step 102 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 105 --max-time-step 105 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 108 --max-time-step 108 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 111 --max-time-step 111 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 114 --max-time-step 114 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 117 --max-time-step 117 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 120 --max-time-step 120 --timestamp ${date}T${hour} --directory /mydata

$hour = "09:00:00"
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 78 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 81 --max-time-step 81 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 84 --max-time-step 84 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 87 --max-time-step 87 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 90 --max-time-step 90 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 93 --max-time-step 93 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 96 --max-time-step 96 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 99 --max-time-step 99 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 102 --max-time-step 102 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 105 --max-time-step 105 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 108 --max-time-step 108 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 111 --max-time-step 111 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 114 --max-time-step 114 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 117 --max-time-step 117 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 120 --max-time-step 120 --timestamp ${date}T${hour} --directory /mydata

$hour = "12:00:00"
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 78 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 81 --max-time-step 81 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 84 --max-time-step 84 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 87 --max-time-step 87 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 90 --max-time-step 90 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 93 --max-time-step 93 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 96 --max-time-step 96 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 99 --max-time-step 99 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 102 --max-time-step 102 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 105 --max-time-step 105 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 108 --max-time-step 108 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 111 --max-time-step 111 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 114 --max-time-step 114 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 117 --max-time-step 117 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 120 --max-time-step 120 --timestamp ${date}T${hour} --directory /mydata

$hour = "15:00:00"
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 78 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 81 --max-time-step 81 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 84 --max-time-step 84 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 87 --max-time-step 87 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 90 --max-time-step 90 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 93 --max-time-step 93 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 96 --max-time-step 96 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 99 --max-time-step 99 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 102 --max-time-step 102 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 105 --max-time-step 105 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 108 --max-time-step 108 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 111 --max-time-step 111 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 114 --max-time-step 114 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 117 --max-time-step 117 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 120 --max-time-step 120 --timestamp ${date}T${hour} --directory /mydata

$hour = "18:00:00"
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 78 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 81 --max-time-step 81 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 84 --max-time-step 84 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 87 --max-time-step 87 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 90 --max-time-step 90 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 93 --max-time-step 93 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 96 --max-time-step 96 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 99 --max-time-step 99 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 102 --max-time-step 102 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 105 --max-time-step 105 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 108 --max-time-step 108 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 111 --max-time-step 111 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 114 --max-time-step 114 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 117 --max-time-step 117 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 120 --max-time-step 120 --timestamp ${date}T${hour} --directory /mydata

$hour = "21:00:00"
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 78 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 81 --max-time-step 81 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 84 --max-time-step 84 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 87 --max-time-step 87 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 90 --max-time-step 90 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 93 --max-time-step 93 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 96 --max-time-step 96 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 99 --max-time-step 99 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 102 --max-time-step 102 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 105 --max-time-step 105 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 108 --max-time-step 108 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 111 --max-time-step 111 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 114 --max-time-step 114 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 117 --max-time-step 117 --timestamp ${date}T${hour} --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-eu --single-level-fields t_2m,tot_prec,w_snow --min-time-step 120 --max-time-step 120 --timestamp ${date}T${hour} --directory /mydata


#Copy-Item -Path ${local_dir}* -Destination ${cloud_dir} -force -recurse

#Remove-Item -r -fo ${local_dir}*