# os-scrapy-uvicorn

[![Build Status](https://www.travis-ci.org/cfhamlet/os-scrapy-uvicorn.svg?branch=master)](https://www.travis-ci.org/cfhamlet/os-scrapy-uvicorn)
[![codecov](https://codecov.io/gh/cfhamlet/os-scrapy-uvicorn/branch/master/graph/badge.svg)](https://codecov.io/gh/cfhamlet/os-scrapy-uvicorn)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/os-scrapy-uvicorn.svg)](https://pypi.python.org/pypi/os-scrapy-uvicorn)
[![PyPI](https://img.shields.io/pypi/v/os-scrapy-uvicorn.svg)](https://pypi.python.org/pypi/os-scrapy-uvicorn)

This project provide a extension to start a ASGI http server([Uvicorn](https://www.uvicorn.org/)) along with Scrapy in the same process.

You can use the [ASGI framework](https://www.uvicorn.org/#alternative-asgi-servers)(recommend [FastAPI](https://github.com/tiangolo/fastapi)) to create app to communicate with Scrapy.

Require: Python 3.6+, Scrapy 2.0+

## Install

```
pip install os-scrapy-uvicorn
```

You can run example spider directly in the project root path

```
scrapy crawl example
```

## Settings

* [use asyncio reactor](https://docs.scrapy.org/en/latest/topics/asyncio.html)

    ```
    TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
    ```

    or you can use [os-scrapy](https://github.com/cfhamlet/os-scrapy)(installed with this project) to start crawling with ``-r`` command line option

    ```
    os-scrapy crawl -r asyncio example
    ```

* enable extension

    ```
    EXTENSIONS = {
        "os_scrapy_uvicorn.Uvicron": 1,
    }
    ```

* app path, you can use ASGI app frameworks to create your app, [FastAPI](https://github.com/tiangolo/fastapi) is recommended

    ```
    UVICORN_APP = "app_module:app"
    ```

* uvicorn server settings, [supported settings](https://www.uvicorn.org/settings/)

    ```
    UVICORN_CONFIG = {"host": "0.0.0.0", "port": 5000}
    ```

* when the server started, Scrapy crawler instance is attached to the app, it is the entrypoint to commnicate with Scrapy

## Unit Tests

```
sh scripts/test.sh
```

## License

MIT licensed.
