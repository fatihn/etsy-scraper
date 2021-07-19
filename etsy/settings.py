BOT_NAME = 'etsy'

SPIDER_MODULES = ['etsy.spiders']
NEWSPIDER_MODULE = 'etsy.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 20

DOWNLOAD_DELAY = 0
RANDOMIZE_DOWNLOAD_DELAY = True

COOKIES_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'etsy.middlewares.too_many_requests_retry_middleware.TooManyRequestsRetryMiddleware': 543,
}

RETRY_HTTP_CODES = [429]