from scrapy import Spider
from scrapy.http import Request
from firmware.items import FirmwareImage
from firmware.loader import FirmwareLoader
import json
import urllib.parse
import os
import urllib.request
import wget


class DLinkSpider(Spider):
    name = "dlink"
    allowed_domains = ["dlink.com"]
    start_urls = ["http://support.dlink.com/AllPro.aspx"]

    custom_settings = {"CONCURRENT_REQUESTS": 3}

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'ServiceTypecookies': "ServiceType=2&ServiceTypeshow=1"}, dont_filter=True)

    def parse(self, response):
        for entry in response.xpath("//tr/td[1]/a/@alt").extract():
            url=urllib.parse.urljoin(
                    response.url, "ProductInfo.aspx?m=%s" % entry)
            yield Request(
                url=urllib.parse.urljoin(
                    response.url, "ProductInfo.aspx?m=%s" % entry),
                headers={"Referer": response.url},
                meta={"product": entry},
                callback=self.parse_product)

    def parse_product(self, response):
        for entry in response.xpath("//select[@id='ddlHardWare']/option"):
            rev = entry.xpath(".//text()").extract()[0]
            val = entry.xpath("./@value").extract()[0]
            # print(rev, val)
            if val:
                yield Request(
                    url=urllib.parse.urljoin(
                        response.url, "/ajax/ajax.ashx?action=productfile&ver=%s" % val),
                    headers={"Referer": response.url,
                             "X-Requested-With": "XMLHttpRequest"},
                    meta={"product": response.meta[
                        "product"], "revision": rev},
                    callback=self.parse_json)


    def parse_json(self, response):
        mib = None
        json_response = json.loads(response.body_as_unicode())
 
        dir_name = "../../../images/dlink/"
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        for entry in reversed(json_response["item"]):
            for file in reversed(entry["file"]):
                if file["filetypename"].lower() == "firmware" or file["isFirmF"] == "1":
                    wget.download(file["url"], dir_name + file["name"] + ".zip")
