# https://scrapfly.io/blog/how-to-scrape-instagram/

# standard web scraping code
import httpx
from parsel import Selector

response = httpx.get("some instagram.com URL")
selector = Selector(response.text)

# in ScrapFly becomes this 👇
from dataScrapers.Instagram.scrapfly import ScrapeConfig, ScrapflyClient

# replaces your HTTP client (httpx in this case)
scrapfly = ScrapflyClient(key="Your ScrapFly API key")

response = scrapfly.scrape(ScrapeConfig(
    url="website URL",
    asp=True, # enable the anti scraping protection to bypass blocking
    country="US", # set the proxy location to a specfic country
    render_js=True # enable rendering JavaScript (like headless browsers) to scrape dynamic content if needed
))

# use the built in Parsel selector
selector = response.selector
# access the HTML content
html = response.scrape_result['content']