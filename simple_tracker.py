import time
from selenium.webdriver.common.keys import Keys
from web_driver_conf import get_web_driver_options
from web_driver_conf import get_chrome_web_driver
from web_driver_conf import set_ignore_certificate_error
from web_driver_conf import set_browser_as_incognito
from web_driver_conf import set_automation_as_head_less
from utils import convert_price_toNumber
from selenium.common.exceptions import NoSuchElementException


class AmazonAPI:
    def __init__(self, search_term):
        self.base_url = "http://www.amazon.de/"
        self.search_term = search_term
        options = get_web_driver_options()
        set_automation_as_head_less(options)
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)
        self.currency = '€'
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
        product_short_url = self.shorten_url(asin)
        title = self.get_title()
        seller = self.get_seller()
        price = self.get_price()
        if title and seller and price:
            product_info = {
                'asin': asin,
                'url': product_short_url,
                'title': title,
                'seller': seller,
                'price': price
            }
            return product_info
        return None

    def get_title(self):
        try:
            return self.driver.find_element_by_id('productTitle').text
        except Exception as e:
            print(e)
            print(f"Can't get title of a product - {self.driver.current_url}")
            return None

    def get_seller(self):
        try:
            return self.driver.find_element_by_id('bylineInfo').text
        except Exception as e:
            print(e)
            print(f"Can't get seller of a product - {self.driver.current_url}")
            return None

    def get_price(self):
        price = None
        try:
            price = self.driver.find_element_by_id('priceblock_ourprice').text
            price = convert_price_toNumber(price, self.currency)
        except NoSuchElementException:
            availability = self.driver.find_element_by_id('availability').text
            if 'Available' in availability:
                price = self.driver.find_element_by_class_name('olp-padding-right').text
                price = price[price.find(self.currency):]
                price = convert_price_toNumber(price, self.currency)
        except Exception as e:
            print(e)
            print(f"Can't get price of a product - {self.driver.current_url}")
            return None
        return price

    @staticmethod
    def get_asin(product_link):
        return product_link[product_link.find('/dp/') + 4:product_link.find('/ref')]

    def shorten_url(self, asin):
        return self.base_url + 'dp/' + asin


if __name__ == '__main__':
    am = AmazonAPI('PS4')
    info = am.get_single_product_info(
        'https://www.amazon.de/-/en/9408574/dp/B07KMV94JF/ref=sr_1_5?dchild=1&keywords=ps4&qid=1587255153&sr=8-5')
    print(info)
