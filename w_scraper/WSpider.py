from typing import AsyncIterator, Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import scrapy
from scrapy.crawler import AsyncCrawlerProcess
from scrapy.http import Response

"""
Responsible for Scraping the https://www.panahon.gov.ph/ for real-time weather data
"""
class WSpider(scrapy.Spider):
    name = 'w_spider'
    start_urls = ["https://www.panahon.gov.ph/"]

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)


    def parse(self, response: Response, **kwargs: Any) -> Any:
        self.driver.get(response.url)


process = AsyncCrawlerProcess()
process.crawl(WSpider)
process.start()
