from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import pandas as pd
from bs4 import BeautifulSoup
import html


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
    driver.find_element('id', 'su').click()
    time.sleep(1)

    html_source = driver.page_source
   # print(html_source)
    link_list = []
    target_char = "http"

    soup = BeautifulSoup(html_source, 'html.parser')
    for link in soup.find_all('a'):
        single_link = str(link.get('href'))
        sub_string = single_link[0:4]
        if sub_string == target_char:
            link_list.append(single_link)

    df = pd.DataFrame(data=link_list,columns=['link_list'])
    df.to_csv('data/result1.csv', index=False)

  #  pd.read_html(html_source)

    # browser = mechanicalsoup.StatefulBrowser()
    # browser.open("https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E5%8D%8E%E5%8D%97%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6&fenlei=256&rsv_pq=0x85c5b4d30051bdbb&rsv_t=72db3CJFOaAHVithUr8dDTdZBl%2Bd88%2FtmzGgRy7R47pqtisswgAvOHrqO2W4&rqlang=en&rsv_enter=0&rsv_dl=tb&rsv_sug3=6&rsv_btype=i&inputT=86&rsv_sug4=86")
    # browser.list_links()
    # print(browser.url)
    # print(browser.page)
    # browser.close()


if __name__ == '__main__':
    start_crawl()
