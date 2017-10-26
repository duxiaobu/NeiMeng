# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from urllib import parse
from CISDI.items import CisdiItem
from scrapy.loader import ItemLoader


class NeimengSpider(Spider):
    name = 'neimeng'
    allowed_domains = ['www.nmgepb.gov.cn']
    start_urls = ['http://www.nmgepb.gov.cn/']
    # 页面循环变量
    page = 1

    def start_requests(self):
        # 起始url
        yield Request(url='http://www.nmgepb.gov.cn/ywgl/hjpj/xmslqk/index.html', callback=self.time_fiter)

    def time_fiter(self, response):
        # 过滤出时间在2015/1/1之前的链接
        url_list = response.xpath("//span[@class='font_hei15_1']/a/@href").extract()
        datetime_list = response.xpath("//span[@class='font_hei15_1']/text()").extract()
        for number, item in enumerate(datetime_list):
            if item >= "2015-01-01":
                url = parse.urljoin(response.url, url_list[number])
                print(url)
                yield Request(url=url, callback=self.parse_detail)
        # 如果最后一条数据的日期比2015-01-01大，就递归自己访问下一页
        if datetime_list[-1] >= "2015-01-01":
            yield Request(url='http://www.nmgepb.gov.cn/ywgl/hjpj/xmslqk/index_{}.html'.format(self.page), callback=self.time_fiter)
        self.page += 1

    def parse_detail(self, response):
        # 解析出具体的字段，因为页面的数据规则，但是构造不规则，所以分类了三种方法解析数据
        cisdi_item = CisdiItem()
        # 规则一，如果这种标签存在，就以它后面的规则提取内容
        if response.xpath('//div[@class="TRS_Editor"]/table').extract():
            title = response.xpath('//div[@class="TRS_Editor"]//table//tr[2]/td[2]//text()').extract()
            title = "".join([item.strip() for item in title if item not in ["\xa0", "\n"]]).split('.')[0]

            location = response.xpath('//div[@class="TRS_Editor"]/table/tbody/tr[2]/td[3]/p//text()').extract()[0]

            construction_unit =  response.xpath('//div[@class="TRS_Editor"]/table/tbody/tr[2]/td[4]/p//text()').extract()
            construction_unit = [item for item in construction_unit if item != "\xa0"][0]

            view_organization = response.xpath('//div[@class="TRS_Editor"]/table/tbody/tr[2]/td[5]/p//text()').extract()
            view_organization = [item for item in view_organization if item != "\xa0"][0]

            deal_date = response.xpath('//div[@class="TRS_Editor"]/table/tbody/tr[2]/td[6]/p//text()').extract()
            deal_date = "".join([item for item in deal_date if item != '\xa0'])

        # 规则二
        elif response.xpath('//div[@class="TRS_Editor"]/p/text()|//div[@id="zoomfont"]/p/text()'):
            results = response.xpath('//div[@class="TRS_Editor"]/p/text()|//div[@id="zoomfont"]/p/text()').extract()
            results = [item for item in results if item not in ["\n", "\xa0"]]
            title = results[4]
            location = results[5]
            construction_unit = results[6]
            view_organization = results[7]
            deal_date = results[8]

        # 规则三
        else:
            try:
                title = "".join(response.xpath("//table/tbody/tr[last()]/td[2]//text()").extract()).strip()
                location = "".join(response.xpath("//table/tbody/tr[last()]/td[3]//text()").extract()).strip()
                construction_unit = "".join(response.xpath("//table/tbody/tr[last()]/td[4]//text()").extract()).strip()
                view_organization = "".join(response.xpath("//table/tbody/tr[last()]/td[5]//text()").extract()).strip()
                deal_date = "".join(response.xpath("//table/tbody/tr[last()]/td[6]//text()").extract()).strip()
            except Exception as e:
                print(e)
                print("出现了新的页面构造，请及时更新解析规则")

        cisdi_item['title'] = title
        cisdi_item['location'] = location
        cisdi_item['construction_unit'] = construction_unit
        cisdi_item['view_organization'] = view_organization
        cisdi_item['deal_date'] = deal_date
        cisdi_item['url'] = response.url

        yield cisdi_item