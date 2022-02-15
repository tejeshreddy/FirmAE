from asyncio.log import logger
from calendar import firstweekday
from distutils.debug import DEBUG
from gc import callbacks
from scrapy import Spider
from scrapy.http import Request

from firmware.items import FirmwareImage
from firmware.loader import FirmwareLoader
import os
import json
import urllib.parse
import wget
import logging
from scrapy.utils.log import configure_logging 

metadata = []

class TPLink(Spider):

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='spider_log.log',
        filemode='a',
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    name = "tp-link"
    vendor = "tp-link"
    allowed_domains = ["tp-link.com"]

    start_urls = ["https://www.tp-link.com/en/support/download/"]

    def parse(self, response):
        for entry in response.xpath("//*[@id='list']/div/div/span/a/@href").extract():
            # self.logger.info(entry)
            url = urllib.parse.urljoin(response.url, entry)
            # self.logger.info(url)

            yield Request(
                url=urllib.parse.urljoin(response.url, entry),
                callback=self.parse_device
            )
    
    def parse_device(self, response):
        # model = response.xpath('//*[@id="model-version-name"]//text()').get()
        # self.logger.info(response.xpath('//*[@id="model-version-name"]//text()').get())

        versions = response.xpath("/html/body/div/div/div/div/div/div/div/div/div/dl/dd/ul/li/a/@href").extract()
        if versions:
            for version_link in versions:
                yield Request(
                    url=urllib.parse.urljoin(version_link, "#Firmware/"),
                    callback=self.parse_version_page
                )
        else:
            yield Request(
                    url=urllib.parse.urljoin(response.url, "#Firmware/"),
                    callback=self.parse_version_page
                )
    
    def parse_version_page(self, response):
        firmware_image_names, firmware_image_download_links = [], []
        firmware_image_names = response.xpath("//*[@id='content_Firmware']/table/tbody/tr[@class='basic-info']/th/p//text()").extract()
        firmware_image_download_links = response.xpath("//*[@id='content_Firmware']/table/tbody/tr[@class='basic-info']/th/a/@href").extract()

        dir_name = "/shared/firmware-images/tplink/"
        # dir_name = "../../tplink/"
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        
        for image_link in firmware_image_download_links:
            wget.download(image_link, dir_name + image_link.split("/")[-1])

        # with open("metadata.txt", "a") as fp:
        #     fp.write(
        #         json.dumps({
        #             "url": response.url,
        #             "names": firmware_image_names,
        #             "download_links": firmware_image_download_links       
        #         })
        #     )
        #     fp.write("\n")

        # for entry in response.xpath("").extract():


            