import logging

from scrapy import signals
from scrapy.exceptions import DontCloseSpider, NotConfigured
from scrapy.utils.defer import deferred_from_coro
from scrapy.utils.reactor import is_asyncio_reactor_installed
from uvicorn.config import Config
from uvicorn.main import Server as BaseServer

logger = logging.getLogger(__name__)


class Server(BaseServer):
    def __init__(self, config, crawler):
        super(Server, self).__init__(config)
        self.crawler = crawler

    def install_signal_handlers(self):
        pass

    async def serve(self, sockets=None):
        config = self.config
        if not config.loaded:
            config.load()
        app = config.loaded_app
        while hasattr(app, "app"):
            app = getattr(app, "app")
        app.crawler = self.crawler
        return await super(Server, self).serve(sockets)


class Uvicorn(object):
    def __init__(self, crawler, server: BaseServer):
        self.crawler = crawler
        crawler.signals.connect(self.dont_close_spider, signal=signals.spider_idle)
        crawler.signals.connect(self.start, signal=signals.spider_opened)
        crawler.signals.connect(self.stop, signal=signals.spider_closed)
        self.server = server
        self.serv_deferred = None

    def start(self):
        self.serv_deferred = deferred_from_coro(self.server.serve())

    def stop(self):
        if self.serv_deferred:
            self.server.handle_exit(None, None)
            return self.serv_deferred

    def dont_close_spider(self):
        raise DontCloseSpider

    @classmethod
    def from_crawler(cls, crawler):
        if not is_asyncio_reactor_installed():
            raise NotConfigured("asyncio reactor not installed")

        settings = crawler.settings
        app = settings.get("UVICORN_APP")
        if not app:
            raise NotConfigured("no app configured")
        config = settings.getdict("UVICORN_CONFIG")
        if "log_config" not in config:
            config["log_config"] = None
        config = Config(app, **config)
        server = Server(config, crawler)

        return cls(crawler, server)
