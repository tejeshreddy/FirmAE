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

count = 0
base_url = "https://www.netgear.com/support/product/"
directory_name = "/shared/firmware-images/netgear/"

class NetgearSpider(Spider):
    name = "netgear"
    allowed_domains = ["netgear.com"]
    start_urls = ["https://www.netgdear.com/support/"]
    primary_set = []


    def parse(self, response):
        for entry in response.xpath("//*[@id='scrolltohere-category']/div/div/a/@href").extract():
            if entry != "javascript:;":
                yield Request(
                url=urllib.parse.urljoin(response.url, "/support/product/" + entry.split("/")[-1]),
                callback=self.parse_page
            )
            else:
                continue

        for entry in response.xpath("/html/body/div/main/section[4]/div/div/div/div/@onclick").extract():
            link = entry.split("=")[1].replace("'", "")
            yield Request(
                url=urllib.parse.urljoin(response.url, link, "#download"),
                callback=self.parse_products
            )


    def parse_page(self, response):
        for device in response.xpath("//*[@id='supportproduct']/section/div/section/section/section/a/@href").extract():
            yield Request(
                url=urllib.parse.urljoin(base_url, device.split("/")[-1] + "#download"),
                callback=self.parse_products
            )

    def parse_products(self, response):
        global primary_set
        product_names = response.xpath("//*[@id='topicsdownload']/div/div/div/div/section/div/div/a/h1//text()").extract()
        product_names = [name.rstrip() for name in product_names]

        product_links = response.xpath("//*[@id='topicsdownload']/div/div/div/div/section/div/div/div/div/a/@href").extract()
        product_links = [link.rstrip() for link in product_links]

        product_json = dict(zip(product_names, product_links))

        # with open("netgear-metadata.txt", "a") as fp:
        #     for k, v in product_json.items():
        #         fp.write(json.dumps({k: v}))
        #         fp.write("\n")

        for link in product_links:
            file_name = link.rsplit("/", 1)[1]
            if (file_name.split(".")[-1] in ["zip"]) and (file_name not in os.listdir(directory_name)):
                print(link, directory_name + file_name)
                # wget.download(link, directory_name + file_name)


