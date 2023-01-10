import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from typing import List, Tuple


service_path = Service(r'chrome_driver\chromedriver.exe')

options = webdriver.ChromeOptions()
options.add_argument("--lang=en-US")
options.add_argument('User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
options.add_argument('Accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')


# Reading full list of 200 links from our file
def read_apps_from_file() -> List:
    with open('app_links.txt', mode='r', encoding='utf-8') as file:
        app_list = []
        for line in file:
            app_list.append(line.strip())
    return app_list


# We get number of last string in final data file to continue parsing (in case we did not receive data from the application page)
def get_last_app() -> int:
    with open('full_data.txt', mode='r', encoding='utf-8') as file:
        for line in file:
            pass

        return int(line.split(';')[0]) if line else 0


# Adding data from aplication page to final data file
def add_data_to_file(position: int, data: tuple):
    with open('full_data.txt', mode='a', encoding='utf-8') as file:
        file.write('\n' + str(position) + ';' + ';'.join(data))


# Main parser. Getting data from application page. Release year and email may not be provided
def get_data_from_app_link(link: str) -> Tuple:
    with webdriver.Chrome(service=service_path, options=options) as browser:
        browser.get(link)
        time.sleep(1)

        page_source = browser.page_source

        soup = BeautifulSoup(page_source, features="lxml")

        title_div = soup.find('div', class_='c017')

        app_name = title_div.find(class_='c0139 c0143 c0131 c0135 c0120').text
        company_name = title_div.find(class_='c0127 c0149 underline-on-hover').text

        year_info = browser.find_element(By.CSS_SELECTOR, 'div > div > div > span > div > span')
        release_year = year_info.text.split(': ')[1]

        email = None
        try:
            contact_button = browser.find_element(By.ID, 'contactInfoButton_desktop')
            if contact_button:
                browser.execute_script('arguments[0].click();', contact_button)
                browser.maximize_window()
                time.sleep(1)

                email = browser.find_element(By.CSS_SELECTOR, 'div > div > div > div > p > a').text

        except Exception as ex:
            pass

        return app_name, company_name, release_year if release_year else 0, email if email else 'No email'


start = -1


while start < 199:
    start = get_last_app() + 1
    print(start)

    try:
        for i, app_link in enumerate(read_apps_from_file()[start:], start=start):
            print(i, app_link)
            add_data_to_file(i, get_data_from_app_link(app_link))
    except Exception:
        pass
