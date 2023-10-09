from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.action_chains import ActionChains

import cv2
from PIL import Image
import numpy as np
import requests
import json
import pickle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import load_workbook

path = r"C:\Users\Nikol\OneDrive\Рабочий стол\боевой\chromedriver.exe"
service = Service(executable_path=path)

options = Options()
options.add_argument("--ignore-certificate-errors")
prefs = {
    "profile.default_content_setting_values.images": 1
}
options.add_experimental_option("prefs", prefs)

options.add_argument("--enable-javascript")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36")

driver = webdriver.Chrome(service=service, options=options)
driver.execute_script("return document.documentElement.setAttribute('webdriver', true)")


    

xx = 0


osn = []
for g in range(0,9):
    driver.get(f'https://novosibirsk.hh.ru/search/vacancy?text=Битрикс24&salary=&no_magic=true&ored_clusters=true&excluded_text=&area=4&page={g}')
    driver.execute_script("document.body.style.zoom='50%'")

    # Загрузка cookie из файла
    with open('cookies.pkl', 'rb') as file: # Укажите путь до ваших файлов cookies
        cookies = pickle.load(file)

    # Добавление cookie в браузер
    for cookie in cookies:
        driver.add_cookie(cookie)

    # Проверка добавленных cookie
    cookies = driver.get_cookies()
    print(cookies)

    print('Подключили куки')
    # Перезагрузка страницы
    driver.refresh()
    print('Перезагрузили')
    time.sleep(10)
    # Ожидание появления элементов
    wait = WebDriverWait(driver, 10)
    #driver.execute_script("document.body.style.zoom='50%'")
    time.sleep(20)

    # Находим все элементы с классом "serp-item"
    serp_items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "serp-item")))

    print(len(serp_items),' количество элементов')
    zz =0 
    # Перебираем найденные элементы
    for item in serp_items:
        try:
            # Проверяем наличие элемента с классом "bloko-button_collapsible"
            try:
                title = item.find_element(By.CLASS_NAME, "serp-item__title").text
            except:
                title = ''
            try:
                price = item.find_element(By.CLASS_NAME, "bloko-header-section-2").text
            except:
                price = ''
            try:
                company = item.find_element(By.CLASS_NAME, "bloko-link_kind-tertiary").text
            except:
                company = ''
            try:
                city = item.find_element(By.CLASS_NAME, "bloko-text").text
            except:
                city = ''
            if item.find_elements(By.CLASS_NAME, "bloko-button_collapsible"):
                # Если элемент найден, сохраняем его в переменную xxx
                zz += 1
                print('Нажатие ', zz)
                #xxx = item.find_elements(By.CLASS_NAME, "bloko-button_collapsible")
                driver.execute_script("arguments[0].scrollIntoView();", item)
                time.sleep(3)
                xxx = item.find_element(By.CLASS_NAME, "bloko-button_collapsible")
                xxx.click()   
                time.sleep(3)
                try:
                    fio = driver.find_element(By.CLASS_NAME, "vacancy-contacts-call-tracking__fio").text
                except:
                    fio = ''
                try:
                    tel = driver.find_element(By.CLASS_NAME, "vacancy-contacts-call-tracking__phone-number").text
                except:
                    tel = ''
                    pass
                try:
                    email = driver.find_element(By.CLASS_NAME, "vacancy-contacts-call-tracking__email").text
                except:
                    email = ''
                    pass
                try:
                    adres = driver.find_element(By.CLASS_NAME, "vacancy-contacts__address").text
                except:
                    adres = ''
                    pass
                result =[title,price,company,city,fio,tel,email,adres]
                zz +=1
                
                workbook = load_workbook('true.xlsx')
                sheet = workbook.active

                # Добавляем данные построчно
                

                #for row in result:
                sheet.append(result)

                # Сохраняем файл
                workbook.save('true.xlsx')
                
                item.find_element(By.CLASS_NAME, "vacancy-contacts-call-tracking__close").click()
                time.sleep(3)
                
        except Exception as ret:
            print(f'Ошибка {ret} ',zz)
driver.quit()
