$date = Get-Date -Format "yyyy-MM-dd"
$date_dir = Get-Date -Format "yyyyMMdd"

# $date = "2021-11-17"
# $date_dir = "20211117"

#$cloud_dir = '\\smb.scientificnet.org\natec_hyse\Users\Andrea Menapace\meteoData\cosmo_d2_eps\'
$local_dir ='G:\data\meteo\dwd\icon-d2-eps_45h\'
mkdir ${local_dir}${date_dir}
#mkdir ${cloud_dir}${date_dir}

docker run --rm --volume ${local_dir}${date_dir}:/mydata deutscherwetterdienst/downloader downloader --model icon-d2-eps --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 45 --timestamp ${date}T03:00:00 --directory /mydata

#Copy-Item -Path ${local_dir}* -Destination ${cloud_dir} -force -recurse

#Remove-Item -r -fo ${local_dir}*