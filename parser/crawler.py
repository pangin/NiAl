import requests
from bs4 import BeautifulSoup

def gethtml(site):      #url을 인자값으로 사용하여 html을 크롤링 해주는 함수 requests 사용.
    raw = requests.get(site)
    html = raw.text
    return html
def parser(html,tag_info):      #크롤링된 html 내용과 파서할 내용인 tag_info를 인자값으로 파싱을 해주는 함수 Beautifulsoap 사용
    soup = BeautifulSoup(html, "lxml")      #html 을 soup의 2번째 인사로 사용했었지만 tag_info를 인식
    myurls = soup.select(tag_info)          #하지 못하는 경우가 있었기 때문에 lxml을 사용하였음.
    return myurls

def textparser(parser_a):       #인자값의 내용을 text화 시키는 함수
    parser_a = parser_a.text
    return parser_a


def ttextparser(parsered):      #리스트 구조의 인자의 원소들을 text화 시키는 함수
    text = []
    for count in range(len(parsered)):
        text.append(parsered[count].text)
    return text


