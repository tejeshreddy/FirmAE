from asyncio.log import logger
from calendar import firstweekday
from distutils.debug import DEBUG
from fileinput import filename
from gc import callbacks
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

base_folder = "/shared/firmware-images/tenda/"
# base_folder = "downloads/"

class TendaScraper(Spider):
    name = "tenda"
    # allowed_domains = ["tendacn.com"]
    start_urls = [
        "https://www.tendacn.com/download/list-3.html"
        ]

    def parse(self, response):
        for entry in response.xpath("/html/body/div/div/div/div/div/div/a/@href").extract():
            response_url = "https://" + entry[2:]

            if "detail" in response_url.split("/")[-1]:
                yield Request(
                    url=urllib.parse.urljoin("http:/", response_url),
                    callback=self.download_helper
                )
            else:
                continue

    def download_helper(self, response):
        for entry in response.xpath("/html/body/div[5]/div/div[2]/div/div/a/@href").extract():
            download_url = "https://" + entry[2:]
            file_name = download_url.split("/")[-1]
            wget.download(download_url, base_folder + file_name)

