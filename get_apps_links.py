import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

url = 'https://apps.microsoft.com/store/category/Business'
service_path = Service(r'chrome_driver\chromedriver.exe')


def get_page_down(body) -> None:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(3)


# We scroll page down and finally get 200 links in the file
def get_app_links() -> None:
    with webdriver.Chrome(service=service_path) as browser:
        browser.get(url)
        time.sleep(1)

        body = browser.find_element(By.CSS_SELECTOR, 'body')
        [get_page_down(body) for _ in range(20)]

        title_list = browser.find_elements(By.CSS_SELECTOR, '.product_card_title.title')
        
        results = [x.get_attribute('href') for x in title_list[:200]]

        with open('app_links.txt', mode='w', encoding='utf-8') as file:
            file.write('\n'.join(results))
