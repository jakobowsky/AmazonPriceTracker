import requests
import pymongo

base_link = 'https://www.amazon.de/s?k=playstation+4&i=videogames&rh=n%3A300992%2Cn%3A2583845031&dc&language=en'


class DataBaseAPI:
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client[self.db_name]


class AmazonAPI:
    def get_products_links(self, base_url):
        pass

    def get_product_info(self, product_link):
        pass

    def shorten_url(self, product_link, *args):
        """
        :param product_link:
        :param args: <-- link args to delete
        :return:
        """
        pass
