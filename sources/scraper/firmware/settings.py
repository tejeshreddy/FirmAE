BOT_NAME = "firmware"

SPIDER_MODULES = ["firmware.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

ITEM_PIPELINES = {
    "firmware.pipelines.FirmwarePipeline" : 1,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None
}

FILES_STORE = "./output/"

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0
AUTOTHROTTLE_MAX_DELAY = 15
CONCURRENT_REQUESTS = 8

DOWNLOAD_TIMEOUT = 1200
DOWNLOAD_MAXSIZE = 0
DOWNLOAD_WARNSIZE = 0

HTTPCACHE_ENABLED=False
ROBOTSTXT_OBEY = False
USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'

# USER_AGENT = "FirmwareBot/1.0 (+https://github.com/firmadyne/scraper)"
#SQL_SERVER = "127.0.0.1"
