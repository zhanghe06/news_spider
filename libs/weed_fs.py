#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: weed_fs.py
@time: 2018-02-10 15:25
"""

import csv
from urlparse import urlparse

import requests

from config import current_config


REQUESTS_TIME_OUT = current_config.REQUESTS_TIME_OUT


class WeedFSClient(object):
    request_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0'
    }

    def __init__(self, weed_fs_url):
        self.weed_fs_url = weed_fs_url

    def _get_assign(self):
        """
        获取分配的资源（url fid）
        接口消息 - 正确:
            {"fid":"1,014e123ade","url":"127.0.0.1:8080","publicUrl":"127.0.0.1:8080","count":1}
        接口消息 - 错误:
            {"error":"No free volumes left!"}
        """
        url = '%s/dir/assign' % self.weed_fs_url
        res = requests.get(url, timeout=REQUESTS_TIME_OUT).json()
        if 'error' in res:
            raise Exception(res['error'])
        return res

    def _get_locations(self, fid):
        """
        获取文件服务器列表
        {"volumeId":"1","locations":[{"url":"127.0.0.1:8080","publicUrl":"127.0.0.1:8080"}]}
        """
        volume_id = fid.split(',')[0]
        url = '%s/dir/lookup?volumeId=%s' % (self.weed_fs_url, volume_id)
        return requests.get(url, timeout=REQUESTS_TIME_OUT).json()

    def save_file(self, local_file_path=None, remote_file_path=None, file_obj=None):
        """
        保存本地文件至weed_fs文件系统
        {"name":"test.csv","size":425429}
        """
        assign = self._get_assign()
        url = 'http://%s/%s' % (assign['url'], assign['fid'])

        if local_file_path:
            file_obj = open(local_file_path, 'rb')
        elif remote_file_path:
            headers = {'Host': urlparse(remote_file_path).netloc}  # 防反爬, 指定图片 Host
            headers.update(self.request_headers)
            res = requests.get(remote_file_path, headers=headers, timeout=REQUESTS_TIME_OUT)
            if res.status_code == 200:
                file_obj = res.content
            else:
                raise Exception('File does not exist')
        elif not file_obj:
            raise Exception('File does not exist')

        res = requests.post(url, files={'file': file_obj}, timeout=REQUESTS_TIME_OUT)
        return dict(res.json(), **assign)

    def get_file_url(self, fid, separator=None):
        """
        获取文件链接
        """
        locations = self._get_locations(fid)
        public_url = locations['locations'][0]['publicUrl']
        return 'http://%s/%s' % (public_url, fid.replace(',', separator) if separator else fid)

    def read_csv(self, fid, encoding=None):
        """
        逐行读取远程csv文件
        :param fid:
        :param encoding: 'gbk'/'utf-8'
        :return:
        """
        file_url = self.get_file_url(fid)
        download = requests.get(file_url, timeout=REQUESTS_TIME_OUT)
        csv_rows = csv.reader(download.iter_lines(), delimiter=',', quotechar='"')
        for csv_row in csv_rows:
            line = [item.decode(encoding, 'ignore') if encoding else item for item in csv_row]
            yield line
