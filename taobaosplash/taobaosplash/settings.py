# -*- coding: utf-8 -*-

# Scrapy settings for taobaosplash project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'taobaosplash'

SPIDER_MODULES = ['taobaosplash.spiders']
NEWSPIDER_MODULE = 'taobaosplash.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'taobaosplash (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1

download_timeout = 60
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'taobaosplash.middlewares.TaobaosplashSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
USER_AGENTS=[
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Opera/9.80 (Windows NT 6.1; WOW64; U; pt) Presto/2.10.229 Version/11.62",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Win64; x64; Trident/4.0)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        ]


DOWNLOADER_MIDDLEWARES = {
   'scrapy_splash.SplashCookiesMiddleware': 723,
   'scrapy_splash.SplashMiddleware': 725,
   'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'taobaosplash.pipelines.TaobaosplashPipeline': 815,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

#渲染服务的url
SPLASH_URL = 'http://192.168.99.100:8050'

# 去重过滤器
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

# 使用Splash的Http缓存
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'tbtestproducts'

COMMANDS_MODULE = 'taobaosplash.commands'

COOKIE_LISTS = []
COOKIE1= '''[
{
    "domain": ".taobao.com",
    "expirationDate": 1555751660.222826,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_cc_",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "W5iHLLyFfA%3D%3D",
    "id": 1
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "_l_g_",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "Ug%3D%3D",
    "id": 2
},
{
    "domain": ".taobao.com",
    "expirationDate": 1524819973.245012,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_m_h5_tk",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "37c8560b90b969a797337615db848163_1524217649907",
    "id": 3
},
{
    "domain": ".taobao.com",
    "expirationDate": 1524819973.245054,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_m_h5_tk_enc",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "e6a162cd51a509eade8683e4c268cc67",
    "id": 4
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "_nk_",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "t15576494927",
    "id": 5
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "_tb_token_",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "3e8e3038718e1",
    "id": 6
},
{
    "domain": ".taobao.com",
    "expirationDate": 2154580768,
    "hostOnly": false,
    "httpOnly": false,
    "name": "cna",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "2lM7E5jUDFQCAT2MRigA3BIi",
    "id": 7
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": true,
    "name": "cookie1",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "AC%2BSBsJUygU6Z2K93zMvX07frEtXak56XpXGt%2BoLic4%3D",
    "id": 8
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": true,
    "name": "cookie17",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "UojQPGipMVy6xA%3D%3D",
    "id": 9
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": true,
    "name": "cookie2",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "3172ae89e66e06da9c00eeed098675d8",
    "id": 10
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "csg",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "52d566ee",
    "id": 11
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "dnk",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "t15576494927",
    "id": 12
},
{
    "domain": ".taobao.com",
    "expirationDate": 1839571938.846491,
    "hostOnly": false,
    "httpOnly": true,
    "name": "enc",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "OPcgoObKlYT%2FO32h4dbnkEwABR0MIxKAp2gbA83TytmsP0fVxAnaInhOVp%2Fy4wwcZ9GQ3uVw6tsJ41nvRx4pCQ%3D%3D",
    "id": 13
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "existShop",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "MTUyNDIxNTcwNg%3D%3D",
    "id": 14
},
{
    "domain": ".taobao.com",
    "expirationDate": 1555751655.918702,
    "hostOnly": false,
    "httpOnly": false,
    "name": "hng",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "CA%7Czh-CN%7CCAD%7C124",
    "id": 15
},
{
    "domain": ".taobao.com",
    "expirationDate": 1539767661,
    "hostOnly": false,
    "httpOnly": false,
    "name": "isg",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "BOTkQUc-Yo7V5JYjaEHCFifvteIW1QnV9o49Fv4F8q91qYRzJo3YdxoLbQGxcUA_",
    "id": 16
},
{
    "domain": ".taobao.com",
    "expirationDate": 1526807660.222591,
    "hostOnly": false,
    "httpOnly": false,
    "name": "lgc",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "t15576494927",
    "id": 17
},
{
    "domain": ".taobao.com",
    "expirationDate": 1610615640.038624,
    "hostOnly": false,
    "httpOnly": false,
    "name": "miid",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "7651308561368876210",
    "id": 18
},
{
    "domain": ".taobao.com",
    "expirationDate": 1524820461.247027,
    "hostOnly": false,
    "httpOnly": false,
    "name": "mt",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "ci=36_1",
    "id": 19
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "sg",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "705",
    "id": 20
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": true,
    "name": "skt",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "13ed931f9c4cb491",
    "id": 21
},
{
    "domain": ".taobao.com",
    "expirationDate": 1531991660.222809,
    "hostOnly": false,
    "httpOnly": false,
    "name": "t",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "5feec0068145ace97c46d9ee91a87ee5",
    "id": 22
},
{
    "domain": ".taobao.com",
    "expirationDate": 1578215660.222845,
    "hostOnly": false,
    "httpOnly": false,
    "name": "tg",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "0",
    "id": 23
},
{
    "domain": ".taobao.com",
    "expirationDate": 1555396769.247063,
    "hostOnly": false,
    "httpOnly": false,
    "name": "thw",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "cn",
    "id": 24
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "tk_trace",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "oTRxOWSBNwn9dPy5J8INBQzvy4fzIaMzvDawskiS2V%2FQXa%2FDQpibpZXvRTMHfRMnphHJQ3wcRskPtpmT%2FtYXQU4oCbVJVwSwchPbyaIs2M11wuLJW%2FPv2dax%2F0%2FByMGuIfz6RKGyUZIxb92yZkxWzqTq%2Ff%2FLGK9nkXs2OxEy8cFtWvZCWh0tBGTHTP1GXHW9Y36Jp7PgyfTvIerI59AdfibQBavQIzKdgJCyIf14eJmW8OTtUUd3AMJFoxIX5qZG%2F28T1oxOCZdLVi6Ms0jqnYp7wi5MqAyuDlOqAh7tpmAejz%2B1CDttia6%2FNWa1ed5uTY6nJWspEJA4T0%2FozbD0kKkXIRnbqUf4HSGNmRWJGOaqpRfCf6HzT6bM132vnYJXVvtLn5Mdvz2D",
    "id": 25
},
{
    "domain": ".taobao.com",
    "expirationDate": 1555751660.222607,
    "hostOnly": false,
    "httpOnly": false,
    "name": "tracknick",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "t15576494927",
    "id": 26
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "uc1",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "cookie14=UoTeOooqBOzADQ%3D%3D&lng=zh_CN&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&existShop=false&cookie21=U%2BGCWk%2F7p4mBoUyS4E9C&tag=8&cookie15=W5iHLLyFOGW7aA%3D%3D&pas=0",
    "id": 27
},
{
    "domain": ".taobao.com",
    "expirationDate": 1526807660.222528,
    "hostOnly": false,
    "httpOnly": true,
    "name": "uc3",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "nk2=F8dByEiWo4EHzSLM&id2=UojQPGipMVy6xA%3D%3D&vt3=F8dBz4Dw9cE%2FAlvunDc%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D",
    "id": 28
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": true,
    "name": "unb",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "1945485770",
    "id": 29
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "v",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "0",
    "id": 30
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "whl",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "-1%260%260%260",
    "id": 31
},
{
    "domain": ".taobao.com",
    "expirationDate": 1555667645,
    "hostOnly": false,
    "httpOnly": false,
    "name": "x",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0",
    "id": 32
}
]'''
COOKIE2='''
            [
{
    "domain": ".taobao.com",
    "expirationDate": 1555751171.598801,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_cc_",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "UIHiLt3xSw%3D%3D",
    "id": 1
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "_l_g_",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "Ug%3D%3D",
    "id": 2
},
{
    "domain": ".taobao.com",
    "expirationDate": 1524819973.245012,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_m_h5_tk",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "37c8560b90b969a797337615db848163_1524217649907",
    "id": 3
},
{
    "domain": ".taobao.com",
    "expirationDate": 1524819973.245054,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_m_h5_tk_enc",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "e6a162cd51a509eade8683e4c268cc67",
    "id": 4
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "_nk_",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "%5Cu52D2%5Cu5E03%5Cu6717%5Cu65F6%5Cu4EE3",
    "id": 5
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "_tb_token_",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "3e8e3038718e1",
    "id": 6
},
{
    "domain": ".taobao.com",
    "expirationDate": 2154580768,
    "hostOnly": false,
    "httpOnly": false,
    "name": "cna",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "2lM7E5jUDFQCAT2MRigA3BIi",
    "id": 7
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": true,
    "name": "cookie1",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "U%2BbLm8B%2B%2F3vXJ7bnAAw32gtOz3yRcNi5Yrvz3q1bg%2BI%3D",
    "id": 8
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": true,
    "name": "cookie17",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "UoewB%2FOZO6TmVw%3D%3D",
    "id": 9
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": true,
    "name": "cookie2",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "3172ae89e66e06da9c00eeed098675d8",
    "id": 10
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "csg",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "babc6fe9",
    "id": 11
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "dnk",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "%E5%8B%92%E5%B8%83%E6%9C%97%E6%97%B6%E4%BB%A3",
    "id": 12
},
{
    "domain": ".taobao.com",
    "expirationDate": 1839571938.846491,
    "hostOnly": false,
    "httpOnly": true,
    "name": "enc",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "OPcgoObKlYT%2FO32h4dbnkEwABR0MIxKAp2gbA83TytmsP0fVxAnaInhOVp%2Fy4wwcZ9GQ3uVw6tsJ41nvRx4pCQ%3D%3D",
    "id": 13
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "existShop",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "MTUyNDIxNTIxOA%3D%3D",
    "id": 14
},
{
    "domain": ".taobao.com",
    "expirationDate": 1555751173.8838,
    "hostOnly": false,
    "httpOnly": false,
    "name": "hng",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "CA%7Czh-CN%7CCAD%7C124",
    "id": 15
},
{
    "domain": ".taobao.com",
    "expirationDate": 1539767179,
    "hostOnly": false,
    "httpOnly": false,
    "name": "isg",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "BKurcDordSuEj6key-yVkzSaOs9VaL5wBfsiyx0oh-pBvMsepZBPkkkeEvzSnBc6",
    "id": 16
},
{
    "domain": ".taobao.com",
    "expirationDate": 1526807171.598637,
    "hostOnly": false,
    "httpOnly": false,
    "name": "lgc",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "%5Cu52D2%5Cu5E03%5Cu6717%5Cu65F6%5Cu4EE3",
    "id": 17
},
{
    "domain": ".taobao.com",
    "expirationDate": 1524819973.230384,
    "hostOnly": false,
    "httpOnly": false,
    "name": "mt",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "ci=1_1",
    "id": 18
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "sg",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "%E4%BB%A395",
    "id": 19
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": true,
    "name": "skt",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "7adb783740f9410e",
    "id": 20
},
{
    "domain": ".taobao.com",
    "expirationDate": 1531991171.598784,
    "hostOnly": false,
    "httpOnly": false,
    "name": "t",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "5feec0068145ace97c46d9ee91a87ee5",
    "id": 21
},
{
    "domain": ".taobao.com",
    "expirationDate": 1578215171.598816,
    "hostOnly": false,
    "httpOnly": false,
    "name": "tg",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "0",
    "id": 22
},
{
    "domain": ".taobao.com",
    "expirationDate": 1555396769.247063,
    "hostOnly": false,
    "httpOnly": false,
    "name": "thw",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "cn",
    "id": 23
},
{
    "domain": ".taobao.com",
    "expirationDate": 1555751171.598653,
    "hostOnly": false,
    "httpOnly": false,
    "name": "tracknick",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "%5Cu52D2%5Cu5E03%5Cu6717%5Cu65F6%5Cu4EE3",
    "id": 24
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "uc1",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&cookie21=URm48syIYB3rzvI4Dim4&cookie15=URm48syIIVrSKA%3D%3D&existShop=false&pas=0&cookie14=UoTeOooqBOlZ9g%3D%3D&tag=8&lng=zh_CN",
    "id": 25
},
{
    "domain": ".taobao.com",
    "expirationDate": 1526807171.598541,
    "hostOnly": false,
    "httpOnly": true,
    "name": "uc3",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "nk2=o8hj2advLzK99Q%3D%3D&id2=UoewB%2FOZO6TmVw%3D%3D&vt3=F8dBz4Dw9cE6wW7%2Fsv0%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D",
    "id": 26
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": true,
    "name": "unb",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "1647124409",
    "id": 27
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "v",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "0",
    "id": 28
},
{
    "domain": ".taobao.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "whl",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "-1%260%260%260",
    "id": 29
},
{
    "domain": ".taobao.com",
    "expirationDate": 1555667645,
    "hostOnly": false,
    "httpOnly": false,
    "name": "x",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0",
    "id": 30
}
]
        '''
COOKIE_LISTS.append(COOKIE1)
COOKIE_LISTS.append(COOKIE2)