# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class CSVPipeline(object):

    def __init__(self):
        # 加上newline=''可以避免，每条数据后面出现空行
        self.file = open(r'C:\Users\acer\Desktop\内蒙古自治区环评数据.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.file, delimiter=',')
        self.csv_writer.writerow(['项目名称', '建设地点', '建设单位', '环境影响评价机构', '受理日期', 'url'])

    def process_item(self, item, spider):
        rows = [item['title'], item['location'], item['construction_unit'], item['view_organization'], item['deal_date'], item['url']]
        self.csv_writer.writerow(rows)
        return item

    def close_spider(self, spider):
        self.file.close()
