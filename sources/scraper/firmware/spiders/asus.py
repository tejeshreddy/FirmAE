from asyncio.log import logger
from calendar import firstweekday
from distutils.debug import DEBUG
from fileinput import filename
from gc import callbacks
from itertools import product
from math import prod
from subprocess import call
from scrapy import Spider
from scrapy.http import Request
import time
from firmware.items import FirmwareImage
from firmware.loader import FirmwareLoader
import os
import json
import urllib.parse
import wget
import logging
from scrapy.utils.log import configure_logging
import pprint

count = 0
directory_name = "/shared/firmware-images/asus/"

class ASUSSpider(Spider):
    name = "asus"
    region = "en"
    allowed_domains = ["asus.com"]
    start_urls = ["https://odinapi.asus.com/apiv2/SearchSuggestion?SystemCode=*&WebsiteCode=us&SearchKey=RTN&SearchType=ProductsAll&RowLimit=5000"]


    def parse(self, response):
        query_response = json.loads(response.text)
        print(type(query_response))
        for object in query_response["Result"][0]["Content"]:
            url = "https://www.asus.com/support/api/product.asmx/GetPDBIOS?website=us&model=" + object["Url"].split("/")[-3]
            print(url)
            yield Request(
                url=url,
                callback=self.parse_product
            )


    def parse_product(self, response):
        product_response = json.loads(response.text)
        with open("asus-metadata-1.txt", "a") as fp:
            if product_response["Status"] == "SUCCESS":
                print(type(product_response["Result"]["Obj"][0]["Files"]))
                for product in product_response["Result"]["Obj"][0]["Files"]:
                    if ".exe" not in product["DownloadUrl"]["Global"]:
                        # wget.download(product["DownloadUrl"]["Global"], directory_name + product["DownloadUrl"]["Global"].split("/")[-1])
                        fp.write(json.dumps({ product["DownloadUrl"]["Global"].split("/")[-1]: product["DownloadUrl"]["Global"]}))
                        fp.write("\n")
                        # print(product["DownloadUrl"]["Global"], product["DownloadUrl"]["Global"].split("/")[-1])
