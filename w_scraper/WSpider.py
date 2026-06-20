import time
from typing import AsyncIterator, Any

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import scrapy
from scrapy.crawler import AsyncCrawlerProcess
from scrapy.http import Response

"""
Responsible for Scraping the https://www.panahon.gov.ph/ for real-time weather data.

So, unfortunately, panahon uses a canvas element so we can't extract some of the data using scrapy and selenium.
What I'm gonna do now is, same as before, I'm going to manually search for the place using selenium and check if there
are any advisories on that place.

Or even better, I'm thinking of creating a list of cities and check for advisories for each cities then extract the data using
Scrapy. 

This is going to be just a worker server that runs every hour to check for advisories.
"""
list_of_regions = [
    'Metro Manila',
    'Baguio City',
    'San Fernando City, La Union',
    'Tuguegarao City, Cagayan',
    'City of San Fernando, Pampanga',
    'Calamba City, Laguna',
    'Calapan City, Oriental Mindoro',
    'Legazpi City, Albay',
    'Iloilo City',
    'Cebu City',
    'Tacloban City, Leyte',
    'Bacolod City, Negros Occidental',
    'Pagadian City, Zamboanga del Sur',
    'Cagayan de Oro City',
    'Davao City',
    'Koronadal City, South Cotabato',
    'Butuan City, Agusan del Norte',
    'Cotabato City'
]


class WSpider(scrapy.Spider):
    name = 'panahon_spider'
    start_urls = ["https://www.panahon.gov.ph/"]

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()

    def parse(self, response: Response, **kwargs: Any) -> Any:
        self.driver.get(response.url)
        wait = WebDriverWait(self.driver, 80)

        wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'device-detected'))
        )
        search_box = wait.until(
            EC.visibility_of_element_located((By.ID, 'js-search-input'))
        )
        search_box.clear()
        search_box.send_keys('Legazpi')
        search_box.send_keys(Keys.ENTER)

        data = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'picker-content'))
        ).text
        data = data.split("\n")
        PRECIPIRATION = ecipitation = data[0]
        TIME = data[1]


        yield {
            "precipitation": PRECIPIRATION,
            "time": TIME
        }


process = AsyncCrawlerProcess()
process.crawl(WSpider)
process.start()
