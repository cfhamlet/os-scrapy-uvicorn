# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy

from os_scrapy_uvicorn.items import ExampleItem


class ExampleSpider(scrapy.Spider):
    """ ExampleSpider
    Auto generated by os-scrapy-cookiecuter

    Run:
        scrapy crawl example
    """

    name = "example"

    start_urls = ["http://example.com/"]

    def parse(self, response):
        request = response.request
        yield ExampleItem(
            request={
                "url": request.url,
                "method": request.method,
                "headers": request.headers,
                "body": request.body,
            },
            response={
                "status": response.status,
                "headers": response.headers,
                "body": response.body,
            },
        )