from scrapy_redis.spiders import RedisSpider
from scrapy import  Selector
import scrapy,re
from renrenspiderslave.items import  RenrenspiderslaveItem

class Renrenchespider(RedisSpider):
    # 爬虫名称
    name = 'renrencheslave'
    # 指定访问爬虫爬取urls队列
    redis_key = 'renrenche:start_urls'

    # 解析详情页
    def parse(self, response):
        res = Selector(response)
        items = RenrenspiderslaveItem()
        # if res.xpath('//div[@class="detail-wrapper"]/@data-encrypt-id'):
        #     items['id'] = res.xpath('//div[@class="detail-wrapper"]/@data-encrypt-id').extract()[0]
        items['id'] = response.url.split('/')[-1]
        # print(items['id'])
        # 标题
        items['title'] = res.xpath('//div[@class="title"]/h1/text()[2]').extract()
        items['title'][0] if items['title'] else 0

        # print(items['title'])
        # 客户出价
        items['price'] = res.xpath('//div[@class="list price-list"]/p/text()').extract()[0]
        items['price'] if items['price'] else 0
        if items['price'] is not '':
            items['price'] =re.findall(r"\d+\.?\d*",items['price'])[0]

        # 市场价
        items['new_car_price'] = res.xpath('//div[@class="middle-content"]/div/div[1]/span/text()').extract()
        items['new_car_price'] if items['new_car_price'] else 0
        if items['new_car_price']:
            items['new_car_price'] =re.findall(r"\d+\.?\d*",items['new_car_price'][0])[0]

        # 首付款
        items['down_payment'] = res.xpath('//div[@class="list payment-list"]/p[@class="money detail-title-right-tagP"][1]/text()').extract()
        items['down_payment'] if items['down_payment'] else 0
        if items['down_payment']:
            items['down_payment'] = re.findall(r"\d+\.?\d*", items['down_payment'][0])[0]
            # items['down_payment'] if items['down_payment'] else 0
            # print(items['down_payment'], type(items['down_payment']))

        # 月供
        items['monthly_payment'] = res.xpath('//div[@class="list payment-list"]/p[@class="money detail-title-right-tagP"][2]/text()').extract()
        items['monthly_payment'] if items['monthly_payment'] else 0
        if items['monthly_payment']:
            items['monthly_payment'] = re.findall(r"\d+\.?\d*", items['monthly_payment'][0])[0]
            # items['monthly_payment'] if items['monthly_payment'] else 0

        # print(items['price'],items['new_car_price'],items['down_payment'],items['monthly_payment'])

        # # 判断是否可以分期购买
        # if down_payment and monthly_payment:
        #     items['staging_info'] = [down_payment.extract()[0], monthly_payment.extract()[0]]
        # # 服务费
        # items['service_fee'] = res.xpath('//*[@id="js-service-wrapper"]/div[1]/p[2]/strong/text()').extract()[0]
        # # 服务项
        # if res.xpath('//div[@id="js-box-service"]/table[@class="box-service"]/tr/td/table/tr/td/text()').extract():
        #     items['service'] = res.xpath(
        #         '//div[@id="js-box-service"]/table[@class="box-service"]/tr/td/table/tr/td/text()').extract()
        # 车辆上牌时间 里程 外迁信息
        if res.xpath('//div[@class="row-fluid-wrapper"]/ul/li/div/p/strong/text()').extract():
            items['info'] = res.xpath('//div[@class="row-fluid-wrapper"]/ul/li/div/p/strong/text()').extract()
            info_list = []
            for item in items['info']:
                info_list.append(item)
            items['info'] = " # ".join(info_list)
            # print(items['info'])
        # 车辆排量
        if res.xpath('//div[@id="js-parms-table"]//tr[3]/td[@class ="bg-color"][3]/div[2]/text()').extract():
            items['displacement'] = res.xpath('//div[@id="js-parms-table"]//tr[3]/td[@class ="bg-color"][3]/div[2]/text()').extract()[0]
            # print(items['displacement'])
        # 车辆上牌城市
        items['registration_city'] = res.xpath('//div[@class="buycar-left"]//li[@class = "sym"][3]/p/strong/text()').extract()[0]
        # print(items['registration_city'])

        # 车源号
        items['options'] = res.xpath('//p[@class="detail-car-id"]/text()').extract()[0].strip().split("：")[1]
        print(items['options'])

        # 判断是都有图片
        if res.xpath('//div[@class="thumb"]//li/a/img/@src'):
            # 车辆图片
            pic_list = res.xpath('//div[@class="thumb"]//li/a/img/@src').extract()
            pic_list_1 = []
            for pic in pic_list:
                pic = "https:" + pic.strip().split("?")[0]
                pic_list_1.append(pic)
            # print(pic_list_1)

            items['car_img'] = " # ".join(pic_list_1)
            # print(items['car_img'])
        # 车辆所在城市
        items['city'] = res.xpath('//div[@class="division-city"]/a/text()').extract()[0].strip()
        # print(items['city'])

        # 车辆颜色
        items['color'] = res.xpath('//div[@class="card-table"]/table//tr/td[2]/text()').extract()
        items['color'][0] if items['color'] else ''

        if items['color']:
            items['color'] = items['color'][0]
            print(items['color'])


        yield items