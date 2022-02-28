# -*- coding: utf-8 -*

from http.client import ResponseNotReady
from importlib.util import resolve_name
from scrapy import Spider
from scrapy.http import Request

from firmware.items import FirmwareImage
from firmware.loader import FirmwareLoader

import urllib.parse
import logging
from scrapy.utils.log import configure_logging 


class TPLinkZHSpider(Spider):

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='spider_log.log',
        filemode='a',
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    name = "tp-link_zh"
    vendor = "tp-link_zh"
    allowed_domains = ["tp-link.com.cn", "service.tp-link.com.cn", "tp-link.com"]
    start_urls = ["https://service.tp-link.com.cn/m/list_download_software_1_0.html"]

    def parse(self, response):
        # print(response.body)
        # self.logger.debug("This is href")
        for entry in response.xpath("/html/body/div/section/section/div/div/table/tbody/tr/th/a/@href").extract():
            self.logger.debug("In this")
            # self.logger.degub(entry)

            # self.logger.debug(entry)
        #     self.logger.info("In the loop")
        #     self.logger.info(response.xpath("/html/body/div[3]/section/section/div/div/table/tbody/tr/th/a/@href").extract())
        #     exit(0)
        #     self.logger.info(urllib.parse.urljoin(response.url.rsplit("/", 1)[0], product))
        #     self.logger.info("XXXXXXXXXXXXXXXXX")
        #     yield Request(
        #         url=urllib.parse.urljoin(response.url.rsplit("/", 1)[0], product),
        #         headers={"Referer": response.url},
        #         callback=self.parse_product)

        # for page in response.xpath("/html/body/div/section/section/div/div/button").extract():
        #     yield Request(
        #         url=urllib.parse.urljoin(response.url, page),
        #         headers={"Referer": response.url},
        #         callback=self.parse)

    # def parse_product(self, response):
    #     print(response)
    #     text = response.xpath("//div[@class='download']/table[1]//tr[1]/td[2]//text()").extract()[
    #         0].encode("ascii", errors="ignore")
    #     date = response.xpath(
    #         "//div[@class='download']/table[1]//tr[4]/td[2]//text()").extract()
    #     href = response.xpath(
    #         "//div[@class='download']/table[1]//tr[5]/td[2]/a/@href").extract()[0]
    #     desc = response.xpath(
    #         "//div[@class='download']/table[1]//tr[1]/td[2]//text()").extract()[0].encode("utf-8")

    #     build = None
    #     product = None
    #     if "_" in text:
    #         build = text.split("_")[1]
    #         product = text.split("_")[0]
    #     elif " " in text:
    #         product = text.split(" ")[0]

    #     item = FirmwareLoader(item=FirmwareImage(),
    #                           response=response, date_fmt=["%Y/%m/%d"])
    #     item.add_value("url", href.encode("utf-8"))
    #     item.add_value("date", item.find_date(date))
    #     item.add_value("description", desc)
    #     item.add_value("build", build)
    #     item.add_value("product", product)
    #     item.add_value("vendor", self.vendor)
    #     yield item.load_item()
