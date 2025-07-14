$date = Get-Date -Format "yyyy-MM-dd"
$date_dir = Get-Date -Format "yyyyMMdd"

# $date = "2022-01-31"
# $date_dir = "20220131"

#$cloud_dir = '\\smb.scientificnet.org\natec_hyse\Users\Andrea Menapace\meteoData\icon-d2-eps\'
$local_dir ='G:\data\meteo\dwd\icon-d2-eps\'
mkdir ${local_dir}${date_dir}
#mkdir ${cloud_dir}${date_dir}

Set-Location ${local_dir}${date_dir}

docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-d2-eps --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 48 --timestamp ${date}T00:00:00 --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-d2-eps --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 48 --timestamp ${date}T03:00:00 --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-d2-eps --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 48 --timestamp ${date}T06:00:00 --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-d2-eps --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 48 --timestamp ${date}T09:00:00 --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-d2-eps --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 48 --timestamp ${date}T12:00:00 --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-d2-eps --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 48 --timestamp ${date}T15:00:00 --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-d2-eps --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 48 --timestamp ${date}T18:00:00 --directory /mydata
docker run --rm --volume ${pwd}:/mydata deutscherwetterdienst/downloader downloader --model icon-d2-eps --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 48 --timestamp ${date}T21:00:00 --directory /mydata

#Copy-Item -Path ${local_dir}* -Destination ${cloud_dir} -force -recurse

#Remove-Item -r -fo ${local_dir}*