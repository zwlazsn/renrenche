# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RenrenspiderslaveItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    '''定义车辆信息的item'''

    # 定义表名称
    collection = 'car_info'
    # 定义字段名称
    id = scrapy.Field() #网页编号
    title = scrapy.Field() #标题
    price = scrapy.Field()  #客户出价
    new_car_price = scrapy.Field() #市场价
    down_payment = scrapy.Field() #首付款
    monthly_payment = scrapy.Field() #月供
    # staging_info = scrapy.Field() #判断是否可以分期购买
    # service_fee = scrapy.Field() # 服务费
    # service = scrapy.Field() # 服务项
    info = scrapy.Field()  # 车辆上牌时间 里程 外迁信息
    displacement = scrapy.Field() # 车辆排量
    registration_city = scrapy.Field() # 车辆上牌城市
    options = scrapy.Field() # 车源号
    car_img = scrapy.Field() # 车辆图片
    city = scrapy.Field() # 车辆所在城市
    color = scrapy.Field() # 车辆颜色
