# -*- coding: utf-8 -*-

# Scrapy settings for wggesucht project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'wggesucht'

SPIDER_MODULES = ['wggesucht.spiders']
NEWSPIDER_MODULE = 'wggesucht.spiders'

RETRY_HTTP_CODES = [s for s in range(300,600) if s != 303]
RETRY_TIMES = 20
DOWNLOAD_TIMEOUT = 5
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Mobile; rv:26.0) Gecko/26.0 Firefox/26.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False
COOKIES_DEBUG = True
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'wggesucht.middlewares.WggesuchtSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'wggesucht.middlewares.WggesuchtDownloaderMiddleware': 543,
#}
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
	# 'scrapy_proxies.RandomProxy': 100,
	'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
	# 'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'wggesucht.RedirectHandler.RedirectHandler': 109,
}
PROXY_LIST = 'proxy_list'
PROXY_MODE = 0
# USER_AGENT_LIST = "user_agents.txt"
# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'wggesucht.FailLogger.FailLogger': 599,
}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'wggesucht.LoggerPipeline.LoggerPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# WG-Gesucht specific settings
INFO = {
      "RENT_TYPE": 0,
      "MAX_RENT": 600,
      "AGE": 22,
      "FIRST_NAME": "foo",
      "LAST_NAME": "bar",
      "EMAIL": "foo@bar.baz",
      "PHONE": "12345",
      "LETTER": "Some long texts you want to tell the landlords...",
      "GENDER": 0 # 0 or 1 or 2, where 0 is doesn't matter, 1 is female and 2 is male
      # The following dates should be of format "DD.MM.YYYY"
      "MOVE_IN_DATE_EARLIEST": "1.10.2017",
      "MOVE_IN_DATE_LATEST": "10.10.2017",
      "MOVE_OUT_DATE_EARLIEST": "30.11.2017",
      "MOVE_OUT_DATE_LATEST": "1.12.2017",
      # Should send the letters to the landlord after a new ad is seen?
      # Sometimes you may not want to do this, particularly when you want to test your new codes.
      "DONT_SEND": True,
}
