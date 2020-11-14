from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://search.naver.com/search.naver?where=news&query=삼성전자', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

news_page_bulk = soup.select('#main_pack > section > div > div.group_news > ul')
news_page_text = str(news_page_bulk[0])
news_page_list_raw = news_page_text.split('<')
news_page_list_adjust = []

for i in news_page_list_raw :
    if "dsc_thumb" in i:
        # print(i)
        end = i.find('onclick')
        # print(i[26:end-2])
        news_indi = i[26:end - 2]
        news_page_list_adjust.append(news_indi)

# print(news_page_list_adjust)
news_list = []

for i in news_page_list_adjust:
    temp_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(i, headers=headers)

    # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
    soup = BeautifulSoup(data.text, 'html.parser')
    try:
        og_image = soup.select_one('meta[property="og:image"]')['content']
        og_title = soup.select_one('meta[property="og:title"]')['content']
        og_description = soup.select_one('meta[property="og:description"]')['content']
        temp_list.append(og_image)
        temp_list.append(og_title)
        temp_list.append(og_description)
    except:
        temp_list=[0,0,0]
    print(temp_list)

print(news_list)
