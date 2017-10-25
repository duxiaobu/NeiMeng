# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class CisdiItem(Item):
    # 项目名称
    title = Field()
    # 建设地点
    location = Field()
    # 建设单位
    construction_unit = Field()
    # 环评机构
    view_organization = Field()
    # 处理日期
    deal_date = Field()
    # 处理日期
    url = Field()

