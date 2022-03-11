from asyncio.log import logger
from calendar import firstweekday
from distutils.debug import DEBUG
from fileinput import filename
from gc import callbacks
from http.client import ResponseNotReady
from urllib import request
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

directory_name = "/shared/firmware-images/trendnet/"

class TrendnetSpider(Spider):
    handle_httpstatus_list = [404]
    name = "trendnet"
    allowed_domains = ["trendnet.com"]
    start_urls = ["http://downloads.trendnet.com/"]

    def parse(self, response):
        base_url = "http://downloads.trendnet.com/"

        for entry in response.xpath("/html/body/pre/a/@href").extract():
            yield Request(
                url=urllib.parse.urljoin(base_url, entry + "firmware"),
                callback=self.parse_products
            )
    
    def parse_products(self, response):
        for entry in response.xpath("/html/body/pre/a/@href").extract():
            file_name = entry.split("/")[-1]
            file_link = str(urllib.parse.urljoin(response.url, entry))

            if file_name not in os.listdir(directory_name):
                wget.download(file_link, directory_name + file_name)

