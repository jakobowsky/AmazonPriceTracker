import requests
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from web_driver_conf import get_web_driver_options
from web_driver_conf import get_chrome_web_driver
from web_driver_conf import set_ignore_certificate_error
from web_driver_conf import set_browser_as_incognito
from web_driver_conf import set_automation_as_head_less


class AmazonAPI:
    def __init__(self, search_term):
        self.base_url = "http://www.amazon.de/"
        self.search_term = search_term
        options = get_web_driver_options()
        # set_automation_as_head_less(options)
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)
        price = "&rh=p_36%3A20000-50000"

    def run(self):
        print("Starting Script...")
        print(f"Looking for {self.search_term} products...")
        links = self.get_products_links()
        if not links:
            print("Stopped script.")
            return
        print(f"Got {len(links)} links to products...")
        print("Getting info about products...")

    def get_products_links(self):
        self.driver.get(self.base_url)
        element = self.driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
        element.send_keys(self.search_term)
        element.send_keys(Keys.ENTER)
        time.sleep(3)  # wait to load page
        result_list = self.driver.find_elements_by_class_name('s-result-list')
        links = []
        try:
            results = result_list[0].find_elements_by_xpath(
                "//div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a")
            links = [link.get_attribute('href') for link in results]
            return links
        except Exception as e:
            print("Didn't get any products...")
            print(e)
            return links

    def get_products_info(self, links):
        products = []
        for link in links:
            product = self.get_single_product_info(link)
        return products

    def get_single_product_info(self, product_link):
        self.driver.get(product_link)
        asin = self.get_asin(product_link)
        print("ASIN: ", asin)
        product_short_url = self.shorten_url(asin)
        print("Short URL: ", product_short_url)
        print("debug")
        title = self.driver.find_element_by_id('productTitle').text
        by = self.driver.find_element_by_id('bylineInfo').text
        price = self.driver.find_element_by_id('priceblock_ourprice').text
        # if not price:
        # self.driver.find_element_by_id('availability').text <- check if ava
        # if ava:
        # self.driver.find_element_by_class_name('olp-padding-right').text

        print("Testing this page now")

    @staticmethod
    def get_asin(product_link):
        return product_link[product_link.find('/dp/') + 4:product_link.find('/ref')]

    def shorten_url(self, asin):
        return self.base_url + '/dp/' + asin


if __name__ == '__main__':
    am = AmazonAPI('PS4')
    am.get_single_product_info(
        'https://www.amazon.de/-/en/dp/B07WHSY2WT/ref=sr_1_2?dchild=1&keywords=ps4&qid=1587251983&sr=8-2')
