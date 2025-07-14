$cloud_dir = '\\smb.scientificnet.org\natec_hyse\Users\Andrea Menapace\meteoData\'
$local_dir ='D:\hydrology\data\GFS_models\DWD_v2\'

Copy-Item -Path ${local_dir}* -Destination ${cloud_dir} -force -recurse