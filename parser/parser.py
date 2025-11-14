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

SCROLL_TIME = 1
NUMBER_OF_SCROLLS = 10000
NUMBER_OF_ARTICLES = 12 * (NUMBER_OF_SCROLLS + 1)

def get_html():
    """
    Get html text of ria news
    """
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.set_window_size(1920, 1080)
    wait = WebDriverWait(driver, 10)
    url = "https://ria.ru/economy/"
 
    # Открыли страницу и нажимаем поочередно на все кнопки, чтобы можно было начать бесконечно листать и считывать новости
    driver.get(url)
    data_param_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'За период')]")
    data_param_btn.click()        

    #data_param_btn = driver.find_element(By.XPATH, "//*[contains(text(), ) and contain(text(), )]")
    #time.sleep(1)
    #param_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'За все время')]")
    #param_btn.click()

    time.sleep(1)
    input()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    
    print("Ищем <div class='list-more ...'>...")
    show_more_div = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-more"))
    )
    driver.execute_script("arguments[0].click();", show_more_div)


    for i in range(NUMBER_OF_SCROLLS):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"Скроллов: {i} / {NUMBER_OF_SCROLLS}")
        time.sleep(random() * SCROLL_TIME)
        

    time.sleep(0.5)
    #time.sleep(10)
    #show_more_btn.click()
    time.sleep(10)
    html_content = driver.page_source

    with open("ria_news.html", 'w', encoding='utf8') as file:
        file.write(html_content)

    driver.quit()

    return html_content


def parse_html(page_source):
    """
    Parsing html, obtained in get_html
    """
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('div', class_='list-item')



html = get_html()
#df = parse_html()

"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from bs4 import BeautifulSoup

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def get_html():
    """
   # Получаем HTML страницу 
"""
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 10)

    print("Открываю сайт...")
    driver.get('https://sn.ria.ru/economy/')

    print("Ищу кнопку и нажимаю 'За период'...")
        
    button = driver.find_element(By.LINK_TEXT("За период")).click()
    period_button = driver.find_element(By.LINK_TEXT("За все время")).click()


get_html()


import time 
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


URL = 'https://ria.ru/economy/'
SCROLL_COUNT = 5
SCROLL_PAUSE_TIME = 2

def get_page_source(url, scroll_count, pause_time):

    print("Запуск...")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        print(f"Открыта страница: {url}")
        print(f"Начинаю крутить страницу. Число круток: {scroll_count}")

        load_more = driver.find_element(By.XPATH, '//button[contains(text(), '')]')
        for i in range(scroll_count):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(pause_time)
            print(f"Проктрука {i + 1}/{scroll_count}")
        
        print("Докрутили... Получаем страницу...")

        return driver.page_source
    
    finally:
        driver.quit()
        print("Закрыли браузер")

"""