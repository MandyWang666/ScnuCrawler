from selenium import webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv
from pprint import pprint
from paddlenlp import Taskflow
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import html
import threading


def text_analysis(url_text):
    schema = ['姓名', '毕业院校']  # Define the schema for entity extraction
    ie = Taskflow('information_extraction', schema=schema)
    pprint(ie(url_text))


def open_url(url_path):
    r = requests.get(url_path)
    soup = BeautifulSoup(r.text, 'html.parser')
    text = soup.get_text()
    text_analysis(text)
    # print(text)


def read_csv(data_path):
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        row = next(reader)
        target_row_number = 50
        while reader.line_num < target_row_number:
            for title, link in row.items():
                print(link)
                open_url(link)
            row = next(reader)


def start_crawl():
    driver = webdriver.Edge()
    driver.get('http://www.baidu.com/')
    time.sleep(1)
    driver.find_element('id', 'kw').send_keys('毕业于华南师范大学')
    time.sleep(1)
    driver.find_element('id', 'su').click()
    time.sleep(2)
    driver.find_element('xpath', "//*[@id='tsn_inner']/div[2]/div/i").click()
    time.sleep(1)
    driver.find_element('xpath', "//*[@id='tsn_inner']/div[1]/span[4]/span").click()
    time.sleep(1)
    driver.find_element('xpath', "//*[@id='container']/div[2]/div/div[2]/div/input").send_keys('baike.baidu.com')
    time.sleep(1)
    driver.find_element('xpath', "//*[@id='container']/div[2]/div/div[2]/div/button").click()
    time.sleep(1)

    target_char = "http"
    current_page = 1
    while driver.find_element('id', 'page').is_displayed():
        try:
            time.sleep(2)
            link_list = []
            html_source = driver.page_source
            soup = BeautifulSoup(html_source, 'html.parser')

            for i in range(current_page, current_page + 10):
                print(i)
                tags = soup.find_all(id=str(i))
                for tag in tags:
                    tag_url = tag.a
                    print(tag_url.get('href'))
                    single_link = str(tag_url.get('href'))
                    sub_string = single_link[0:4]
                    # 特殊情况：http://map.baidu.com访问会有问题
                    if sub_string == target_char and single_link != 'http://map.baidu.com':
                        link_list.append(single_link)
                current_page = current_page + 1

            df = pd.DataFrame(data=link_list, columns=['link_list'])
            df.to_csv("data/result2.csv", mode="a", index=False, encoding="utf-8", header=0)

            time.sleep(2)

            if current_page == 11:
                driver.find_element('xpath', "//*[@id='page']/div/a[10]").click()
            else:
                driver.find_element('xpath', "//*[@id='page']/div/a[11]").click()

        except:
            driver.quit()


if __name__ == '__main__':
    # start_crawl()
    read_csv('data/result2.csv')
