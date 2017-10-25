# -*- coding: utf-8 -*-

from scrapy.cmdline import execute
import sys
import os

# 指向的路径 E:\PycharmProjects\CISDI
CISDI_path = os.path.dirname(os.path.abspath(__file__))
# 设置工程目录，在这个目录下执行scrapy命令才会生效。
sys.path.append(CISDI_path)
execute(["scrapy", "crawl", "neimeng"])
