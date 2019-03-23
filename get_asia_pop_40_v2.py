#!/usr/bin/env python
# -*- coding: UTF-8 -*-

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
# youtubemp3music.info
convert_base_url = 'https://youtubemp3music.info/@api/json/mp3/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def get_now_str():
    return time.strftime("%Y%m%d_%H%M%S")

def get_today_str():
    return time.strftime("%Y%m%d")
    
res = requests.get(base_url, stream=True)
soup = BeautifulSoup(res.text, 'html.parser')
data_video_ids = soup.findAll('div', id=re.compile('^track-video'))
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

f = open(download_dir_path+'.txt', 'w+')
for id in data_video_ids:
    download_url = download_base_url+id['data-video-id']
    print('download now: ' + download_url)

    try:
        res = requests.get(convert_base_url+id['data-video-id'], headers=headers, stream=True)
        json_obj = json.loads(res.text)
        title = json_obj['vidTitle']
        file = 'https:' + json_obj['vidInfo']['0']['dloadUrl']
        print(title, file)
        res = requests.get(file, allow_redirects=True)
        open(title + '.mp3', 'wb').write(res.content)
    except Exception as ex:
        print('download error: ' + download_url)
        f.write('error url: ' + download_url + '\n')

f.close()
os.chdir('../')
