from selenium.webdriver.common.keys import Keys
from product import Product
from utils import convert_price_toNumber
from web_driver_conf import get_web_driver_options
from web_driver_conf import get_chrome_web_driver
from web_driver_conf import set_ignore_certificate_error
from web_driver_conf import set_browser_as_incognito
from web_driver_conf import set_automation_as_head_less
import json
import time

URL = "http://www.amazon.de/"
search_term = 'PS4'

options = get_web_driver_options()
set_automation_as_head_less(options)
set_ignore_certificate_error(options)
set_browser_as_incognito(options)
driver = get_chrome_web_driver(options)

driver.get(URL)

element = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
element.send_keys(search_term)
element.send_keys(Keys.ENTER)
time.sleep(3) # wait to load page
# x = driver.find_elements_by_xpath('//*[@id="search"]/div[1]/div[1]/div/span[4]/div[1]')
x = driver.find_elements_by_class_name('s-result-list')
l = x[0].find_elements_by_xpath("//div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a")
links = [link.get_attribute('href') for link in l]
print(links)


# /html/body/div[1]/div[2]/div[1]/div[1]/div/span[4]/div[1]/div[1]/div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a
# //*[@id="search"]/div[1]/div[1]/div/span[4]/div[1]/div[1]/div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a
# a-link-normal a-text-normal
# search > div.s-desktop-width-max.s-desktop-content.s-opposite-dir.sg-row > div.sg-col-20-of-24.s-matching-dir.sg-col-28-of-32.sg-col-16-of-20.sg-col.sg-col-32-of-36.sg-col-8-of-12.sg-col-12-of-16.sg-col-24-of-28 > div > span:nth-child(5) > div:nth-child(1) > div:nth-child(1)
# //*[@id="search"]/div[1]/div[1]/div/span[4]/div[1]/div[1]
# //*[@id="search"]/div[1]/div[1]/div/span[4]/div[1]/div[1]/div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a
# //*[@id="search"]/div[1]/div[1]/div/span[4]/div[1]/div[2]

#de
# //*[@id="search"]/div[1]/div[2]/div/span[4]/div[1]/div[2]/div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a