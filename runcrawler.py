from selenium import webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv
from pprint import pprint
from paddlenlp import Taskflow
import re


def extract_context(text, keyword, context_size=200):
    pattern = re.compile(re.escape(keyword))
    match = pattern.search(text)

    if not match:
        return ""

    start, end = match.span()
    start_index = max(0, start - context_size)
    end_index = min(len(text), end + context_size)

    return text[start_index:end_index]


def text_analysis(url_text):
    schema = ['姓名', '性别', '现任职务','工作单位', '毕业院校', '出生年份', '毕业年份']  # Define the schema for entity extraction
    ie = Taskflow('information_extraction', schema=schema)
    pprint(ie(url_text))
    result = ie(url_text)
    alumni_list = []

    for item in result:
        name = item.get('姓名')  # 使用get方法来避免KeyError
        sex = item.get('性别')
        job_title = item.get('现任职务')
        job_location = item.get('工作单位')
        school = item.get('毕业院校')
        birth_year = item.get('出生年份')
        graduate_year = item.get('毕业年份')

        if name is not None:  # 检查是否成功获取到'姓名'
            name_text = name[0]['text'] if name and isinstance(name, list) and name[0].get('text') else None
            if name_text is not None:
                print(name_text)
        else:
            name_text = ""
            print("当前字典中不存在'姓名'键")

        if sex is not None:
            sex_text = sex[0]['text'] if sex and isinstance(sex, list) and sex[0].get('text') else None
            if sex_text is not None:
                print(sex_text)
        else:
            sex_text = ""
            print("当前字典中不存在'性别'键")

        if job_title is not None:
            job_title_text = job_title[0]['text'] if job_title and isinstance(job_title, list) and job_title[0].get('text') else None
            if job_title_text is not None:
                print(job_title_text)
        else:
            job_title_text = ""
            print("当前字典中不存在'现任职务'键")

        if job_location is not None:
            job_location_text = job_location[0]['text'] if job_location and isinstance(job_location, list) and job_location[0].get('text') else None
            if job_location_text is not None:
                print(job_location_text)
        else:
            job_location_text = ""
            print("当前字典中不存在'工作单位'键")

        if school is not None:
            school_text = school[0]['text'] if school and isinstance(school, list) and school[0].get('text') else None
            if school_text is not None:
                print(school_text)
        else:
            school_text = ""
            print("当前字典中不存在'毕业院校'键")

        if birth_year is not None:
            birth_year_text = birth_year[0]['text'] if birth_year and isinstance(birth_year, list) and birth_year[
                0].get('text') else None
            if birth_year_text is not None:
                print(birth_year_text)
        else:
            birth_year_text = ""
            print("当前字典中不存在'出生年份'键")

        if graduate_year is not None:
            graduate_year_text = graduate_year[0]['text'] if graduate_year and isinstance(graduate_year, list) and \
                                                             graduate_year[0].get('text') else None
            if graduate_year_text is not None:
                print(graduate_year_text)
        else:
            graduate_year_text = ""
            print("当前字典中不存在'毕业年份'键")

        alumni_data = (name_text, sex_text,job_title_text,job_location_text,school_text ,birth_year_text, graduate_year_text)
        alumni_list.append(alumni_data)

    df1 = pd.DataFrame(data=alumni_list, columns=['姓名', '性别', '现任职务','工作单位', '毕业院校', '出生年份', '毕业年份'])
    df1.columns = ['姓名', '性别', '现任职务', '毕业院校', '工作单位','出生年份', '毕业年份']
    df1.to_csv("data/alumni.csv", mode="a", index=False, encoding="utf-8", header=0)


def open_url(url_path):
    r = requests.get(url_path)
    soup = BeautifulSoup(r.text, 'html.parser')
    text = soup.get_text()
    context = extract_context(text, "毕业院校")
    text_analysis(context)
    # print(context)


def read_analysis_save(data_path):
    time.sleep(3)
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        row = next(reader)
        target_row_number = 200
        while reader.line_num < target_row_number:
            for title, link in row.items():
                print(link)
                open_url(link)
            row = next(reader)


def start_crawl():
    driver = webdriver.Edge()
    driver.get('http://www.baidu.com/')
    time.sleep(1)
    driver.find_element('id', 'kw').send_keys('毕业院校：华南师范大学')
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
    # while driver.find_element('id', 'page').is_displayed():
    # demo展示前5页
    for i in range(5):
        try:
            time.sleep(2)
            link_list = []
            html_source = driver.page_source
            soup = BeautifulSoup(html_source, 'html.parser')

            for i in range(current_page, current_page + 10):
              #  print(i)
                tags = soup.find_all(id=str(i))
                for tag in tags:
                    tag_url = tag.a
                  #  print(tag_url.get('href'))
                    single_link = str(tag_url.get('href'))
                    sub_string = single_link[0:4]
                    # 特殊情况：http://map.baidu.com访问会有问题
                    if sub_string == target_char and single_link != 'http://map.baidu.com':
                        link_list.append(single_link)
                current_page = current_page + 1

            df = pd.DataFrame(data=link_list, columns=['link_list'])
            df.to_csv("data/result.csv", mode="a", index=False, encoding="utf-8", header=0)

            time.sleep(2)

            if current_page == 11:
                driver.find_element('xpath', "//*[@id='page']/div/a[10]").click()
            else:
                driver.find_element('xpath', "//*[@id='page']/div/a[11]").click()

        except:
            driver.quit()


if __name__ == '__main__':
   # start_crawl()
    read_analysis_save('data/result2.csv')
