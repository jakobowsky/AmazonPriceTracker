import requests
import time
from bs4 import BeautifulSoup


class APILogger:
    def print_log(self, msg):
        print(f"[AmazonAPI] {msg}")


class AmazonAPI:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.11 (KHTML, like Gecko) '
                          'Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        self.number_of_requests = 0
        self.logger = APILogger()

    def __request_url(self, link):
        for attempt in range(10):
            try:
                if self.number_of_requests == 50:
                    self.logger.print_log(f'Did 50 requests, going to sleep for 15 secs...')
                    time.sleep(15)
                    self.number_of_requests = 0
                response = requests.get(
                    link,
                    timeout=4,
                    headers=self.headers,
                )
                self.number_of_requests += 1
            except requests.HTTPError:
                self.logger.print_log(f'HTTP error.')
            except requests.RequestException:
                self.logger.print_log(f'RequestException.')
            except Exception as e:
                self.logger.print_log(f'__request_url error: {e}')
            else:
                return response
        self.logger.print_log(f'ERROR! Max attempts. Raising error')
        raise

    def get_products_links(self, base_url):
        pass

    def get_product_info(self, product_link):
        details = {"name": "", "price": 0, "deal": True, "url": ""}
        _url = self.shorten_url(product_link)
        if _url == "":
            details = None
        else:
            page = self.__request_url(_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            print('ELO')
            price = soup.find('span', attrs={'class': 'a-offscreen'})
            title = soup.find(id="productTitle")
            price = soup.find(id="priceblock_dealprice")
            if price is None:
                price = soup.find(id="priceblock_ourprice")
                details["deal"] = False
            if title is not None and price is not None:
                details["name"] = title.get_text().strip()
                details["url"] = _url
            else:
                return None
        return details

    def shorten_url(self, product_link, *args):
        """
        :param product_link:
        :param args: <-- link args to delete
        :return:
        """
        return product_link


if __name__ == '__main__':
    base_link = 'https://www.amazon.de/s?k=playstation+4&i=videogames&rh=n%3A300992%2Cn%3A2583845031&dc&language=en'
    am = AmazonAPI()
    x = am.get_product_info('https://www.amazon.de/-/en/dp/B07WHSY2WT/ref=sr_1_1?dchild=1&keywords=playstation+4&qid=1587235149&s=videogames&sr=1-1')
    print(x)