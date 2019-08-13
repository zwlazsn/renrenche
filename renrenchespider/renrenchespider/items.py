# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RenrenchespiderItem(scrapy.Item):
    # def __init__(self):
    count = 1
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    print(count,url)
    count+=1

