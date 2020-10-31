import requests
from bs4 import BeautifulSoup

# URL을 읽어서 HTML를 받아오고,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://finance.naver.com/sise/lastsearch2.nhn', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')
# print(soup)

# select를 이용해서, tr들을 불러오기

# naver_rising_stocks = soup.select('.tltle')
naver_rising_stocks = soup.select('#contentarea > div.box_type_l > table > tr > td > a')
print(type(naver_rising_stocks))
print(naver_rising_stocks)

# for i in naver_rising_stocks:
#     print(i.text)

# naver_rising_stocks = soup.select('#contentarea > div.box_type_l > table')
# print(type(naver_rising_stocks))
# print(naver_rising_stocks)

# for i in naver_rising_stocks:
#     tr_tag = i.select_one('tr')
#     print(tr_tag)


# movies (tr들) 의 반복문을 돌리기
# for movie in movies:
#     # movie 안에 a 가 있으면,
#     a_tag = movie.select_one('td.title > div > a')
#     if a_tag is not None:
#         rank = movie.select_one('td:nth-child(1) > img')['alt']  # img 태그의 alt 속성값을 가져오기
#         title = a_tag.text  # a 태그 사이의 텍스트를 가져오기
#         star = movie.select_one('td.point').text  # td 태그 사이의 텍스트를 가져오기
#         print(rank, title, star)