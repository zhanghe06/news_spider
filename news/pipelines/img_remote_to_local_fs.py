# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import re
from urlparse import urljoin

from news.items import FetchResultItem

from libs.weed_fs import WeedFSClient
from config import current_config

WEED_FS_URL = current_config.WEED_FS_URL

weed_fs_client = WeedFSClient(WEED_FS_URL)


def remote_to_local(remote_file_path):
    """
    保存远程图片文件
    :param remote_file_path:
    :return:
    """
    remote_file_save_result = weed_fs_client.save_file(remote_file_path=remote_file_path)
    local_file_url = weed_fs_client.get_file_url(remote_file_save_result['fid'], '/')
    return local_file_url


def add_src(html_body, base=u''):
    """
    添加图片文件链接（1、添加真实链接；2、替换本地链接）
    :param html_body:
    :param base:
    :return:
    """
    rule = ur'data-src="(.*?)"'
    img_data_src_list = re.compile(rule, re.I).findall(html_body)
    for img_src in img_data_src_list:
        # 处理相对链接
        if base:
            new_img_src = urljoin(base, img_src)
        if new_img_src.startswith(u'/'):
            continue
        # 远程转本地
        local_img_src = remote_to_local(new_img_src)
        img_dict = {
            'img_src': img_src,
            'local_img_src': local_img_src
        }
        html_body = html_body.replace(img_src, '%(img_src)s" src="%(local_img_src)s' % img_dict)
    return html_body


def replace_src(html_body, base=u''):
    """
    替换图片文件链接（替换本地链接）
    :param html_body:
    :param base:
    :return:
    """
    rule = ur'src="(.*?)"'
    img_data_src_list = re.compile(rule, re.I).findall(html_body)
    for img_src in img_data_src_list:
        # 处理相对链接
        if base:
            new_img_src = urljoin(base, img_src)
        if new_img_src.startswith(u'/'):
            continue
        # 远程转本地
        local_img_src = remote_to_local(new_img_src)
        img_dict = {
            'img_src': img_src,
            'local_img_src': local_img_src
        }
        html_body = html_body.replace(img_src, '%(local_img_src)s" data-src="%(img_src)s' % img_dict)
    return html_body


class ImgRemoteToLocalFSPipeline(object):
    """
    图片 远程链接 转 本地文件系统链接
    注意:
        1、置于数据存储 pipeline 之前
    """

    def process_item(self, item, spider):

        spider_name = spider.name
        # 读取抓取内容
        if isinstance(item, FetchResultItem):
            if spider_name == 'weixin':
                html_body = item['article_content']
                base = item['article_url']
                item['article_content'] = add_src(html_body, base)
            if spider_name == 'weibo':
                html_body = item['article_content']
                base = item['article_url']
                item['article_content'] = replace_src(html_body, base)
        return item
