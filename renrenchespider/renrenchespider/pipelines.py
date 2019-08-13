# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import redis

class RenrenchespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MasterPipeline(object):
    def __init__(self):
        # 初始化连接数据的变量
        self.REDIS_HOST = settings['REDIS_HOST']
        self.REDIS_PORT = settings['REDIS_PORT']
        # 链接redis
        self.r = redis.Redis(host=self.REDIS_HOST, port=self.REDIS_PORT,db=2)

    def process_item(self, item, spider):
        # 向redis中插入需要爬取的链接地址
        self.r.lpush('renrenche:start_urls', item['url'])

        return item

