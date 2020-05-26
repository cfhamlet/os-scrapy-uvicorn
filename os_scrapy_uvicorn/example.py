# FastAPI example
# pip install fastapi
import json

from fastapi import FastAPI
from scrapy.utils.serialize import ScrapyJSONEncoder

app = FastAPI()


@app.get("/")
async def index():
    encoder = ScrapyJSONEncoder()
    return json.loads(encoder.encode(app.crawler.stats.get_stats()))
