import json
import scrapy

from typing import Any, AsyncIterator, Generator, AsyncGenerator

from scrapy import Request
from scrapy.http.response.text import TextResponse
from scrapy.crawler import AsyncCrawlerProcess
from urllib.parse import quote


class AccuWeatherScraper(scrapy.Spider):
    def __init__(self, location: str = None, **kwargs: Any):
        super().__init__(**kwargs)
        self.location = location

    name = 'accu_weather'
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "ROBOTSTXT_OBEY": False,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 5,
        "AUTOTHROTTLE_MAX_DELAY": 60,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 1.0,
        "AUTOTHROTTLE_DEBUG": False
    }

    async def start(self) -> AsyncGenerator[Request, None]:
        curr_location = quote(self.location)  # Para sa mga spaces; turned to its ascii equivalent or dunno code
        api_url = f"https://www.accuweather.com/web-api/autocomplete?query={curr_location}&language=en-us"
        yield scrapy.Request(url=api_url, callback=self.parse_suggestions)

    def parse_suggestions(self, response: TextResponse):
        search_results = json.loads(response.text)
        if search_results:
            first_match = search_results[0]
            loc_key = first_match.get('key')
            path = f"/web-api/three-day-redirect?key={loc_key}"
            yield response.follow(url=path, callback=self.parse_homepage)

    def parse_homepage(self, response: TextResponse):
        yield {"img": response.css("img.weather-icon").attrib['src'],
               "temp": response.css("div.temp::text").get().strip()}


if __name__ == "__main__":
    _location = "Libon, PH"
    process = AsyncCrawlerProcess()
    process.crawl(AccuWeatherScraper, location=_location)
    process.start()
