import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from kakaobank.items import Article
import requests
import json
import re


class kakaobankSpider(scrapy.Spider):
    name = 'kakaobank'
    start_urls = ['https://www.kakaobank.com/']

    def parse(self, response):
        json_response = json.loads(requests.get('https://www.kakaobank.com/api/v1/boards/NOTICE/posts?size=100000&page=0').text)
        articles = json_response["result"]['content']
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()

            title = article["title"]
            date = article["reg_date"][:10]
            p = re.compile(r'<.*?>')
            content = p.sub('', article["content"])

            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('content', content)

            yield item.load_item()