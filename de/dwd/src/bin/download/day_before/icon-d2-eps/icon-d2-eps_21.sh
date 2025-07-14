#!/bin/sh
date_str=$(date --date="yesterday" +%Y-%m-%d)
date_dir=$(date --date="yesterday" +%Y%m%d)

local_dir='/media/lacie2022/data/meteo/dwd/icon-d2-eps/'
mkdir -p ${local_dir}${date_dir}

docker run --rm --volume ${local_dir}${date_dir}:/mydata deutscherwetterdienst/downloader downloader \
 --model icon-d2-eps --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 48 \
 --timestamp ${date_str}T21:00:00 --directory /mydata
