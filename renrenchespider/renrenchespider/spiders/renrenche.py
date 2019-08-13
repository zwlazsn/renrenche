# -*- coding: utf-8 -*-
import scrapy
import re
# from scrapy_redis.spiders import RedisSpider
# from scrapy_redis.spiders import  RedisSpider
# from scrapy_redis.spiders import RedisSpider
from scrapy import Selector, Request
from renrenchespider.items import RenrenchespiderItem

class RenrencheSpider(scrapy.Spider):
    name = 'renrenche'
    allowed_domains = ['renrenche.com']
    start_urls = ['https://www.renrenche.com/']


    # 解析所有城市
    def parse(self, response):
        res = Selector(response)
        city_url_list = res.xpath('//div[@class="area-city-letter"]/div/a[@class="province-item "]/@href')
        for city_url in city_url_list:
            city = city_url.extract()
            city = 'https://www.renrenche.com' + city
            # print(city,type(city))
            yield Request(url=city, callback=self.parse_brand)

    # 解析所有的品牌
    def parse_brand(self, response):
        res = Selector(response)
        brand_url_list = res.xpath('//div[@id="brand_more_content"]/div/p/span/a')
        for a in brand_url_list:
            band_url = a.xpath('./@href').extract()[0]
            band_url = 'https://www.renrenche.com' + band_url

            # print(band_url,type(band_url))
            yield Request(url=band_url, callback=self.parse_page_url)

    # 解析某个品牌下面的具体某辆车的页面
    def parse_page_url(self, response):
        # 实例化管道
        item = RenrenchespiderItem()
        res = Selector(response)
        # 获取到页面的所有li的信息 用于下面的页码的判断
        li_list = res.xpath('//ul[@class="row-fluid list-row js-car-list"]/li')
        # 判断页面
        # 判断页面是否有li标签
        if li_list:
            for c in li_list:
                # 获取页面的每个车的url 并且过滤掉有广告的那个a标签
                one_car_url = c.xpath('./a[@class="thumbnail"]/@href').extract()
                # print(one_car_url,type(one_car_url))
                # 判断是否有这个url
                if one_car_url:
                    # print(one_car_url, type(one_car_url))
                    one_car_url = self.start_urls[0] + one_car_url[0]
                    item['url'] = one_car_url
                    # print(one_car_url, type(one_car_url))
                    yield item

            # 下一页信息
            page = response.meta.get('page', 2)
            #
            url = response.url
            # 替换掉上面的结果出现../p1/p2/这样的结果我们只需要一个页面参数
            url = re.sub(r'p\d+', '', url)
            # 产生新的页面url
            car_info_url = url + 'p{page}/'
            # 回调 获取下一页
            yield Request(car_info_url.format(page=page), meta={'page': page + 1}, callback=self.parse_page_url)