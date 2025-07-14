#!/bin/sh
date_str=$(date +%Y-%m-%d)
date_dir=$(date +%Y%m%d)

local_dir='/media/lacie2022/data/meteo/dwd/icon-d2/'
mkdir -p ${local_dir}${date_dir}

docker run --rm --volume ${local_dir}${date_dir}:/mydata deutscherwetterdienst/downloader downloader \
 --model icon-d2 --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 48 \
 --timestamp ${date_str}T00:00:00 --directory /mydata
docker run --rm --volume ${local_dir}${date_dir}:/mydata deutscherwetterdienst/downloader downloader \
 --model icon-d2 --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 48 \
 --timestamp ${date_str}T03:00:00 --directory /mydata
docker run --rm --volume ${local_dir}${date_dir}:/mydata deutscherwetterdienst/downloader downloader \
 --model icon-d2 --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 48 \
 --timestamp ${date_str}T06:00:00 --directory /mydata
docker run --rm --volume ${local_dir}${date_dir}:/mydata deutscherwetterdienst/downloader downloader \
 --model icon-d2 --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 48 \
 --timestamp ${date_str}T09:00:00 --directory /mydata
docker run --rm --volume ${local_dir}${date_dir}:/mydata deutscherwetterdienst/downloader downloader \
 --model icon-d2 --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 48 \
 --timestamp ${date_str}T12:00:00 --directory /mydata
docker run --rm --volume ${local_dir}${date_dir}:/mydata deutscherwetterdienst/downloader downloader \
 --model icon-d2 --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 48 \
 --timestamp ${date_str}T15:00:00 --directory /mydata
docker run --rm --volume ${local_dir}${date_dir}:/mydata deutscherwetterdienst/downloader downloader \
 --model icon-d2 --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 48 \
 --timestamp ${date_str}T18:00:00 --directory /mydata
docker run --rm --volume ${local_dir}${date_dir}:/mydata deutscherwetterdienst/downloader downloader \
 --model icon-d2 --single-level-fields t_2m,tot_prec,w_snow --min-time-step 0 --max-time-step 48 \
 --timestamp ${date_str}T21:00:00 --directory /mydata
