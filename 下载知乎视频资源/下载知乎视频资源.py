# _*_ coding:utf-8 _*_
# Author:liu

import re
import uuid
import subprocess

import requests

'''
安装ffmpeg：sudo apt install ffmpeg
'''

# 请求头信息,包含cook信息
# 对于cooki信息,打开谷歌浏览器中的抓包工具复制一份就可以
HEADERS = {
    'cookie': '',
    # TODO
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}

QUALITY = 'ld'  # 支持是 'ld' 'sd' 'hd' 分别是低清、中清、高清


def get_video_ids_from_url(url):
    """
    url地址
    """
    html = requests.get(url, headers=HEADERS).text
    # print(html)
    video_ids = re.findall(r'data-lens-id="(\d+)"', html)
    # print('11111', video_ids)
    if video_ids:
        return set([int(video_id) for video_id in video_ids])
    return []


def yield_video_m3u8_url_from_video_ids(video_ids):
	#使用生成器,目的节省内存空间
    for video_id in video_ids:
        api_video_url = 'https://lens.zhihu.com/api/videos/{}'.format(int(video_id))
        r = requests.get(api_video_url, headers=HEADERS)
        playlist = r.json()['playlist']
        m3u8_url = playlist[QUALITY]['play_url']
        yield m3u8_url


def download(url):
    video_ids = get_video_ids_from_url(url)
    m3u8_list = list(yield_video_m3u8_url_from_video_ids(video_ids))
    filename = '{}.mp4'.format(uuid.uuid4())
    for idx, m3u8_url in enumerate(m3u8_list):
        print('download {}'.format(m3u8_url))
        subprocess.call(['ffmpeg', '-i', m3u8_url, filename.format(str(idx))])


if __name__ == '__main__':
    # 要下载的url地址
    # url = 'https://www.zhihu.com/question/275611095/answer/382959285'
    url = input("请输入下载的url:")
    download(url)
