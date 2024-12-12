# Scrapy settings for first_teste project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "first_teste"

SPIDER_MODULES = ["first_teste.spiders"]
NEWSPIDER_MODULE = "first_teste.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "first_teste (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "first_teste.middlewares.FirstTesteSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "first_teste.middlewares.FirstTesteDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "first_teste.pipelines.FirstTestePipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True

# The initial download delay
AUTOTHROTTLE_START_DELAY = 5

# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60

# O número médio de requisições que o Scrapy deve enviar em paralelo para
# cada servidor remoto

AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Habilitar a exibição de estatísticas de controle de taxa para cada resposta recebida:
AUTOTHROTTLE_DEBUG = False

# Habilitar e configurar o cache HTTP (desativado por padrão)
# Veja https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
# Definir configurações cujo valor padrão está obsoleto para um valor à prova de futuro
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
# settings.py

# Número máximo de requisições simultâneas (padrão: 16)
#CONCURRENT_REQUESTS = 32

# Atraso entre requisições para o mesmo site (padrão: 0)
#DOWNLOAD_DELAY = 3

# Habilitar o AutoThrottle (controle automático de taxa de requisições)
AUTOTHROTTLE_ENABLED = True
# Atraso inicial de download
AUTOTHROTTLE_START_DELAY = 5
# Atraso máximo de download em caso de alta latência
AUTOTHROTTLE_MAX_DELAY = 60
# Número médio de requisições que o Scrapy deve enviar em paralelo para cada servidor remoto
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Habilitar a exibição de estatísticas de controle de taxa para cada resposta recebida
AUTOTHROTTLE_DEBUG = False

# Limite de páginas a serem raspadas
#CLOSESPIDER_PAGECOUNT = 100

# Limite de itens a serem raspados
#CLOSESPIDER_ITEMCOUNT = 1000

# Habilitar e configurar o cache HTTP (desativado por padrão)
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"
