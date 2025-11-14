import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from random import random
from bs4 import BeautifulSoup
import pandas as pd


"""
Парсим риа новости и потом собираем оттуда статьи 
"""

class Parser:
    def __init__(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.set_window_size(1920, 1080)    
        self.wait = WebDriverWait(self.driver, 10)
        self.NUMBER_OF_SCROLLS = 200
        self.SCROLL_TIME = 0.5
        self.NUMBER_OF_MONTHS = 17 * 6  # Одна полная страница с максимальной прокруткой вмещает в себя около 6 месяцев (порядка 6000 статей)

    def get_page_html(self):
        self.driver.get("https://ria.ru/economy/")

        input()     # Поправляем даты

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        
        print("Ищем <div class='list-more ...'>...")
        show_more_div = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-more"))
        )
        self.driver.execute_script("arguments[0].click();", show_more_div)


        for i in range(self.NUMBER_OF_SCROLLS):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"Скроллов: {i + 1} / {self.NUMBER_OF_SCROLLS}")
            time.sleep(random() * self.SCROLL_TIME)

        html_content = self.driver.page_source

        input()     # смотрим последнюю дату

        return html_content
    
    def get_htmls(self):
        for i in range(self.NUMBER_OF_MONTHS // 6):
            print(f"\n Номер прокрутки: {i+11}/{self.NUMBER_OF_MONTHS} ")
            html_content = self.get_page_html()
            with open(f"ria_news{i+11}.html", 'w', encoding='utf8') as file:
                file.write(html_content)
        
        self.driver.quit()

parser = Parser()
parser.get_htmls()

