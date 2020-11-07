from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

##########################################mongodb##################################
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.project_joopago    # 'dbsparta'라는 이름의 db를 사용합니다. 'dbsparta' db가 없다면 새로 만듭니다.

##############################################################검색순위DB만들기################################
# URL을 읽어서 HTML를 받아오고,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://finance.naver.com/sise/lastsearch2.nhn', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')
# print(soup)
# select를 이용해서, tr들을 불러오기
# head 뽑아오기
naver_rising_stocks_info_list = []
naver_rising_stocks_head_list = []

naver_rising_stocks_head = soup.select_one('#contentarea > div.box_type_l > table > tr')
naver_rising_stocks_head_adjust = naver_rising_stocks_head.select('th')

for i in naver_rising_stocks_head_adjust:
    # print(i.text)
    naver_rising_stocks_head_list.append(i.text)

# 검색주식 순위의 자료 모으기
naver_rising_stocks_info = soup.select('#contentarea > div.box_type_l > table > tr')
for i in naver_rising_stocks_info:
    infos = i.select('td')
    # print(infos)
    temp_stock_list = []
    temp_dic = {}
    for info in infos:
        info_adjust = info.text.strip()
        # print(info_adjust)
        temp_stock_list.append(info_adjust)
    # print(temp_stock_list)

    if len(temp_stock_list) == len(naver_rising_stocks_head_list):
        count = 0
        while count < len(naver_rising_stocks_head_list):
            temp_dic[naver_rising_stocks_head_list[count]] = temp_stock_list[count]
            count += 1
        naver_rising_stocks_info_list.append(temp_dic)
print(naver_rising_stocks_info_list)
for i in naver_rising_stocks_info_list:
    # print(i)
    db.naver_rising_stocks.insert_one(i)
print("네이버 검색어 주식 DB 저장 완료")

####################################################################급등주 DB만들기##############################
# URL을 읽어서 HTML를 받아오고,
data = requests.get('https://finance.naver.com/sise/sise_low_up.nhn', headers=headers)
# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

naver_fast_rising_stocks_head_adjust_list = []
naver_fast_rising_stocks_info_adjust_list = []

naver_fast_rising_stocks_head = soup.select_one('#contentarea > div.box_type_l > table > tr')
naver_fast_rising_stocks_head_adjust = naver_fast_rising_stocks_head.select('th')
for i in naver_fast_rising_stocks_head_adjust:
    # print(i.text)
    naver_fast_rising_stocks_head_adjust_list.append(i.text)
# print(naver_fast_rising_stocks_head_adjust_list)

naver_fast_rising_stocks_info = soup.select('#contentarea > div.box_type_l > table > tr')
# print(naver_fast_rising_stocks_info)
for i in naver_fast_rising_stocks_info:
    infos = i.select('td')
    # print(infos)
    temp_stock_list = []
    temp_dic = {}
    for info in infos:
        info_adjust = info.text.strip()
        # print(info_adjust)
        temp_stock_list.append(info_adjust)
    if len(temp_stock_list) == len(naver_fast_rising_stocks_head_adjust_list):
        count = 0
        while count < len(naver_fast_rising_stocks_head_adjust_list):
            temp_dic[naver_fast_rising_stocks_head_adjust_list[count]] = temp_stock_list[count]
            count += 1
        naver_fast_rising_stocks_info_adjust_list.append(temp_dic)
print(naver_fast_rising_stocks_info_adjust_list)
for i in naver_fast_rising_stocks_info_adjust_list:
    # print(i)
    db.naver_fast_rising_stocks.insert_one(i)
print("네이버 급등 주식 DB 저장 완료")

####################################################################주식차트가져오기##############################
# URL을 읽어서 HTML를 받아오고,
data = requests.get('', headers=headers)
# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')



##############################flask##############################################
app = Flask(__name__)

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/rising_stocks', methods=['GET'])
def rising_stock_get():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
    result = list(db.naver_rising_stocks.find({}, {'_id': 0}))
    # 2. articles라는 키 값으로 article 정보 보내주기
    return jsonify({'result': 'success', 'rising_stocks': result})

@app.route('/fast_rising_stocks', methods=['GET'])
def fast_rising_stock_get():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
    result = list(db.naver_fast_rising_stocks.find({}, {'_id': 0}))
    # 2. articles라는 키 값으로 article 정보 보내주기
    return jsonify({'result': 'success', 'fast_rising_stocks': result})

@app.route('/test', methods=['POST'])
def test_post():
    title_receive = request.form['title_give']
    print(title_receive)
    return jsonify({'result': 'success', 'msg': '이 요청은 POST!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

