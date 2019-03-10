#!/usr/bin/env python
# -*- coding: UTF-8 -*-
###############################################################################
# asia pop 40 unofficial
###############################################################################

import os
import sys
import requests
import shutil
import time
import re
import json
from bs4 import BeautifulSoup

base_url = 'http://asiapop40.com/'
download_base_url = 'https://www.youtube.com/watch?v='
convert_base_url = 'http://michaelbelgium.me/ytconverter/convert.php?youtubelink='
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
save_list = []

def get_now_str():
    return time.strftime("%Y%m%d_%H%M%S")

def get_today_str():
    return time.strftime("%Y%m%d")

res = requests.get(base_url, stream=True)
soup = BeautifulSoup(res.text, 'html.parser')
data_video_ids = soup.findAll('div', id=re.compile('^track-video'))
data_video_track_titles = soup.findAll('span', class_=re.compile('^chart-track-title'))
data_video_artist_titles = soup.findAll('span', class_=re.compile('^chart-artist-title'))

if data_video_ids is None:
    print('nothing to download')
    sys.exit(1)

## create download dir ##
download_dir_path = 'asia_pop_40_' + get_today_str()
try:
    os.mkdir(download_dir_path, 0o755)
except OSError as ex:
    print('create dir error')
    sys.exit(-1)

## change to download dir ##
os.chdir(download_dir_path)

for i in range(len(data_video_track_titles)):
    print(data_video_track_titles[i].text.strip('\n') + ' ' + data_video_artist_titles[i].text.strip('\n'))
    save_dict = {
        'title':  data_video_track_titles[i].text.strip('\n') + ' ' + data_video_artist_titles[i].text.strip('\n'),
        'youtube_url': download_base_url+data_video_ids[i]['data-video-id']
    }
    save_list.append(save_dict)

f = open(download_dir_path+'.txt', 'w+')
f.write(json.dumps(save_list))
f.close()
os.chdir('../')
