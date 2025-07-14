$date = Get-Date -Format "yyyy-MM-dd"
$date_dir = Get-Date -Format "yyyyMMdd"

#$date = "2021-02-06"
#$date_dir = Get-Date -Format "20210206"

#$cloud_dir = '\\smb.scientificnet.org\natec_hyse\Users\Andrea Menapace\meteoData\cosmo_d2_eps\'
$local_dir ='D:\data\GFS_models\DWD_v2\cosmo_d2_eps_45h\'
mkdir ${local_dir}${date_dir}
#mkdir ${cloud_dir}${date_dir}

docker run --rm --volume ${local_dir}${date_dir}:/mydata deutscherwetterdienst/downloader downloader --model cosmo-d2-eps --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 45 --timestamp ${date}T03:00:00 --directory /mydata

#Copy-Item -Path ${local_dir}* -Destination ${cloud_dir} -force -recurse

#Remove-Item -r -fo ${local_dir}*