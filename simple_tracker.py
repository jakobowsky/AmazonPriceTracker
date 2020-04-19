import time
from selenium.webdriver.common.keys import Keys
from web_driver_conf import get_web_driver_options
from web_driver_conf import get_chrome_web_driver
from web_driver_conf import set_ignore_certificate_error
from web_driver_conf import set_browser_as_incognito
from web_driver_conf import set_automation_as_head_less
from utils import convert_price_toNumber
from selenium.common.exceptions import NoSuchElementException
import json
from datetime import datetime


# TODO implement price filters while searching
# TODO save to json
# TODO Generate report from json


class GenerateReport:
    def __init__(self, file_name, data, filters, base_link):
        self.data = data
        self.file_name = file_name
        self.filters = filters
        self.base_link = base_link
        report = {
            'title': self.file_name,
            'date': self.get_now(),
            'best_item': self.get_best_item(),
            'filters': self.filters,
            'base_link': self.base_link,
            'products': self.data
        }
        with open(f'{file_name}.json', 'w') as f:
            json.dump(report, f)

    @staticmethod
    def get_now():
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")

    def get_best_item(self):
        try:
            return sorted(self.data, key=lambda k: k['price'])[0]
        except Exception as e:
            print(e)
            print("Problem with sorting items")
            return None


class AmazonAPI:
    def __init__(self, search_term, min, max, base_url):
        self.base_url = base_url
        self.search_term = search_term
        options = get_web_driver_options()
        # set_automation_as_head_less(options)
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)
        self.currency = '€'
        self.price_filter = f"&rh=p_36%3A{min}00-{max}00"

    def run(self):
        print("Starting Script...")
        print(f"Looking for {self.search_term} products...")
        links = self.get_products_links()
        if not links:
            print("Stopped script.")
            return
        print(f"Got {len(links)} links to products...")
        print("Getting info about products...")
        products = self.get_products_info(links)
        self.driver.quit()
        return products

    def get_products_links(self):
        self.driver.get(self.base_url)
        element = self.driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
        element.send_keys(self.search_term)
        element.send_keys(Keys.ENTER)
        time.sleep(2)  # wait to load page
        self.driver.get(f'{self.driver.current_url}{self.price_filter}')
        time.sleep(2)  # wait to load page
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
        asins = self.get_asins(links)
        products = []
        for asin in asins:
            product = self.get_single_product_info(asin)
            products.append(product)
        return products

    def get_asins(self, links):
        return [self.get_asin(link) for link in links]

    def get_single_product_info(self, asin):
        product_short_url = self.shorten_url(asin)
        self.driver.get(f'{product_short_url}?language=en_GB')
        time.sleep(2)
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
            try:
                availability = self.driver.find_element_by_id('availability').text
                if 'Available' in availability:
                    price = self.driver.find_element_by_class_name('olp-padding-right').text
                    price = price[price.find(self.currency):]
                    price = convert_price_toNumber(price, self.currency)
            except Exception as e:
                print(e)
                print(f"Can't get price of a product - {self.driver.current_url}")
                return None
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
    name = "PS4"
    min_price = '250'
    max_price = '450'
    filters = {'min': min_price, 'max': max_price}
    base_url = "http://www.amazon.de/"

    # am = AmazonAPI('PS4', 250, 450)
    # info = am.run()
    # print(info)

    test_data = [{'asin': 'B07WHSY2WT', 'url': 'http://www.amazon.de/dp/B07WHSY2WT',
                  'title': 'PlayStation 4 Slim - Konsole (1 TB, schwarz) inkl. FIFA 20 + 2 DualShock Controller',
                  'seller': 'Sony Interactive Entertainment', 'price': 379.0},
                 {'asin': 'B085PB4B6J', 'url': 'http://www.amazon.de/dp/B085PB4B6J',
                  'title': 'PlayStation 4 Pro - Konsole (1 TB, schwarz) PS Hits Naughty Dog Bundle',
                  'seller': 'Sony Interactive Entertainment', 'price': 399.99},
                 {'asin': 'B07HHPX4N1', 'url': 'http://www.amazon.de/dp/B07HHPX4N1',
                  'title': 'PlayStation 4 - Konsole (500 GB, schwarz, slim, F-Chassis) inkl. 2 DualShock 4 Controller',
                  'seller': 'Sony Interactive Entertainment', 'price': 299.99},
                 {'asin': 'B07HSJW7HK', 'url': 'http://www.amazon.de/dp/B07HSJW7HK',
                  'title': 'PlayStation 4 Pro - Konsole (1 TB, schwarz, Pro, Modell: CUH-7216B)',
                  'seller': 'Sony Interactive Entertainment', 'price': 408.0},
                 {'asin': 'B07KMV94JF', 'url': 'http://www.amazon.de/dp/B07KMV94JF',
                  'title': 'PlayStation 4 Slim - Konsole (1TB, schwarz)', 'seller': 'Sony Interactive Entertainment',
                  'price': 359.0}, {'asin': 'B07HNR4ZZD', 'url': 'http://www.amazon.de/dp/B07HNR4ZZD',
                                    'title': 'PlayStation4 - Konsole (500GB, schwarz, slim)', 'seller': 'Sony',
                                    'price': 317.0}, {'asin': 'B07V7NT6ZC', 'url': 'http://www.amazon.de/dp/B07V7NT6ZC',
                                                      'title': 'PlayStation 4 Pro (1TB, black): Fortnite Neo Versa Bundle',
                                                      'seller': 'Sony', 'price': 409.98},
                 {'asin': 'B07V282WBB', 'url': 'http://www.amazon.de/dp/B07V282WBB',
                  'title': 'PlayStation 4 Slim - Konsole (500GB, Jet Black) + 2 Controller: Fortnite Neo Versa Bundle',
                  'seller': 'Sony', 'price': 369.0}, {'asin': 'B07YGJGFZC', 'url': 'http://www.amazon.de/dp/B07YGJGFZC',
                                                      'title': 'PlayStation 4 Virtual Reality Megapack - Edition 2 (inkl. Skyrim, Astro Bot Rescue Mission, VR Worlds, Resident Evil: Biohazard, Everybody´s Golf)',
                                                      'seller': 'Sony Interactive Entertainment', 'price': 379.0},
                 {'asin': 'B07K2PT733', 'url': 'http://www.amazon.de/dp/B07K2PT733', 'title': 'PlayStation VR',
                  'seller': 'Sony Interactive Entertainment', 'price': 289.0},
                 {'asin': 'B07Z7438CY', 'url': 'http://www.amazon.de/dp/B07Z7438CY',
                  'title': 'Spongebob SquarePants: Battle for Bikini Bottom - Rehydrated - F.U.N. Edition [Playstation 4]',
                  'seller': 'THQ Nordic', 'price': 299.99},
                 {'asin': 'B07DNM3MT9', 'url': 'http://www.amazon.de/dp/B07DNM3MT9',
                  'title': 'PlayStation 4 Pro - Konsole Schwarz, A Chassis, 1TB, (Generalüberholt)',
                  'seller': 'Sony Interactive Entertainment', 'price': 349.99},
                 {'asin': 'B07WDKT7DP', 'url': 'http://www.amazon.de/dp/B07WDKT7DP',
                  'title': 'PlayStation 4 Pro - Konsole (1TB) inkl. FIFA 20',
                  'seller': 'Sony Interactive Entertainment', 'price': 419.0},
                 {'asin': 'B07YSX4DLW', 'url': 'http://www.amazon.de/dp/B07YSX4DLW',
                  'title': 'PlayStation 4 Slim inkl. 2 Controller und Call of Duty: Modern Warfare - Konsolenbundle (1TB, schwarz, Slim)',
                  'seller': 'Sony', 'price': 444.0}, {'asin': 'B07S7RGRFC', 'url': 'http://www.amazon.de/dp/B07S7RGRFC',
                                                      'title': 'Playstation 4 Slim 1TB - Limited Edition Days of Play 2019',
                                                      'seller': 'Sony', 'price': 359.0},
                 {'asin': 'B07TTB3SR2', 'url': 'http://www.amazon.de/dp/B07TTB3SR2',
                  'title': 'ASTRO Gaming A50 Wireless Headset and Base Station', 'seller': 'ASTRO Gaming',
                  'price': 249.99}]

    GenerateReport(name, test_data, filters, base_url)
