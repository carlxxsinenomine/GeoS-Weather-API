from typing import AsyncIterator, Any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

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
        # chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)


    def parse(self, response: Response, **kwargs: Any) -> Any:
        self.driver.get(response.url)

        WebDriverWait(self.driver, 80).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'device-detected'))
        )
        search_box = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'js-search-input'))
        )
        search_box.clear()
        search_box.send_keys('Legazpi')


process = AsyncCrawlerProcess()
process.crawl(WSpider)
process.start()
