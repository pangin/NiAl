import requests
import set_db
import db_handler
from bs4 import BeautifulSoup
site_dgu_s = "http://www.dongguk.edu/mbs/kr/jsp/board/list.jsp?boardId=3646&search=&column=&mcategoryId=0&boardType=01&listType=01&command=list&id=kr_010802000000&spage=1"
site_dgu_s_haksa = "https://www.dongguk.edu/mbs/kr/jsp/board/list.jsp?boardId=3638&search=&column=&mcategoryId=0&boardType=01&listType=01&command=list&id=kr_010801000000&spage=1"
site_dgu_s_janghak = "https://www.dongguk.edu/mbs/kr/jsp/board/list.jsp?boardId=3662&search=&column=&mcategoryId=0&boardType=01&listType=01&command=list&id=kr_010804000000&spage=1"
site_dgu_s_gookjae =  "https://www.dongguk.edu/mbs/kr/jsp/board/list.jsp?boardId=9457435&search=&column=&mcategoryId=0&boardType=01&listType=01&command=list&id=kr_010807000000&spage=1"
site_dgu_s_ippsii = "https://www.dongguk.edu/mbs/kr/jsp/board/list.jsp?boardId=3654&search=&column=&mcategoryId=0&boardType=01&listType=01&command=list&id=kr_010803000000&spage=1"
site_dgu_s_haksul = "https://www.dongguk.edu/mbs/kr/jsp/board/list.jsp?boardId=11533472&search=&column=&mcategoryId=0&boardType=01&listType=01&command=list&id=kr_010808000000&spage=1"
tag_dgu_s = 'td.title'
site_dgu_g_list = []
site_dgu_unfixed = []
site_dgu_s_list = []
site_dgu_s_unfixed = []
site_dgu_g_unfixed = []
site_dgu_s_list_haksa = []
site_dgu_s_list_ippsii = []
site_dgu_s_list_janghak = []
site_dgu_s_list_gookjae = []
site_dgu_s_list_haksul = []

a=1
fix = 1

def gethtml(site):
    raw = requests.get(site)
    html = raw.text
    return html
def parser(html,tag_info):
    soup = BeautifulSoup(html, "lxml")
    myurls = soup.select(tag_info)
    return myurls

def Textparser(parser_a):
    for i in range(len(parser_a)):
        parser_a[i] = parser_a[i].text
    return parser_a

def get_dgu_s_fixed(list):
    site_dgu_s_fixed = []
    element = 0
    lenn = int(len(list)/7)
    for count in range(lenn):
        if(len(str(list[element]))>40):
            fix = list[element+1]
            site_dgu_s_fixed.append(fix)
            element = element+7
        else:
            element = element+7
    return site_dgu_s_fixed

def mkkey(url):
    num1 = url.find('boardSeq=')
    num2 = url.find('boardId=')
    num3 = url.find('id=kr_')
    boardSeq = url[num1 + 9:num1 + 17]
    boardId = url[num2 + 8:num2 + 12]
    id_kr = url[num3 + 6:num3 + 18]
    urlnum4 = url.replace('https://www.dongguk.edu/mbs/kr/jsp/board/view.jsp?spage=', '')
    page = urlnum4.replace('&boardId='+boardId+'&boardSeq='+boardSeq+'&id=kr_'+id_kr+'&column=&search=&categoryDepth=&mcategoryId=0', '')
    return (boardSeq + boardId + id_kr + page)

def mkkey_gookjae(url):
    num1 = url.find('boardSeq=')
    num2 = url.find('boardId=')
    num3 = url.find('id=kr_')
    boardSeq = url[num1 + 9:num1 + 17]
    boardId = url[num2 + 8:num2 + 15]
    id_kr = url[num3 + 6:num3 + 18]
    urlnum4 = url.replace('https://www.dongguk.edu/mbs/kr/jsp/board/view.jsp?spage=', '')
    page = urlnum4.replace(
        '&boardId=' + boardId + '&boardSeq=' + boardSeq + '&id=kr_' + id_kr + '&column=&search=&categoryDepth=&mcategoryId=0',
        '')
    return (boardSeq + boardId + id_kr + page)

def mkkey_haksul(url):
    num1 = url.find('boardSeq=')
    num2 = url.find('boardId=')
    num3 = url.find('id=kr_')
    boardSeq = url[num1 + 9:num1 + 17]
    boardId = url[num2 + 8:num2 + 16]
    id_kr = url[num3 + 6:num3 + 18]
    urlnum4 = url.replace('https://www.dongguk.edu/mbs/kr/jsp/board/view.jsp?spage=', '')
    page = urlnum4.replace(
        '&boardId=' + boardId + '&boardSeq=' + boardSeq + '&id=kr_' + id_kr + '&column=&search=&categoryDepth=&mcategoryId=0',
        '')
    return (boardSeq + boardId + id_kr + page)


def dgu_s_url(parsered,page,i):
    z = str(parsered[i])
    num1 = z.find('boardSeq=')
    num2 = z.find('boardId=')
    num3 = z.find('id=kr_')
    boardSeq = z[num1+9:num1+17]
    boardId = z[num2+8:num2+12]
    id_kr = z[num3+6:num3+18]
    url = 'https://www.dongguk.edu/mbs/kr/jsp/board/view.jsp?spage='+str(page)+'&boardId='+boardId+'&boardSeq='+boardSeq+'&id=kr_'+id_kr+'&column=&search=&categoryDepth=&mcategoryId=0'
    return url

def dgu_s_url_gookjae(parsered,page,i):
    z = str(parsered[i])
    num1 = z.find('boardSeq=')
    num2 = z.find('boardId=')
    num3 = z.find('id=kr_')
    boardSeq = z[num1 + 9:num1 + 17]
    boardId = z[num2 + 8:num2 + 15]
    id_kr = z[num3 + 6:num3 + 18]
    url = 'https://www.dongguk.edu/mbs/kr/jsp/board/view.jsp?spage=' + str(
        page) + '&boardId=' + boardId + '&boardSeq=' + boardSeq + '&id=kr_' + id_kr + '&column=&search=&categoryDepth=&mcategoryId=0'
    return url

def dgu_s_url_haksul(parsered,page,i):
    z = str(parsered[i])
    num1 = z.find('boardSeq=')
    num2 = z.find('boardId=')
    num3 = z.find('id=kr_')
    boardSeq = z[num1 + 9:num1 + 17]
    boardId = z[num2 + 8:num2 + 16]
    id_kr = z[num3 + 6:num3 + 18]
    url = 'https://www.dongguk.edu/mbs/kr/jsp/board/view.jsp?spage=' + str(
        page) + '&boardId=' + boardId + '&boardSeq=' + boardSeq + '&id=kr_' + id_kr + '&column=&search=&categoryDepth=&mcategoryId=0'
    return url
def textparser(parsered):
    text = []
    for count in range(len(parsered)):
        text.append(parsered[count].text)
    return text

for count in range(349):
    site_dgu_s_list.append("http://www.dongguk.edu/mbs/kr/jsp/board/list.jsp?boardId=3646&search=&column=&mcategoryId=0&boardType=01&listType=01&command=list&id=kr_010802000000&spage="+str(count+1))

for count in range(109):
    site_dgu_s_list_haksa.append("https://www.dongguk.edu/mbs/kr/jsp/board/list.jsp?boardId=3638&search=&column=&mcategoryId=0&boardType=01&listType=01&command=list&id=kr_010801000000&spage="+str(count+1))

for count in range(93):
    site_dgu_s_list_janghak.append("https://www.dongguk.edu/mbs/kr/jsp/board/list.jsp?boardId=3662&search=&column=&mcategoryId=0&boardType=01&listType=01&command=list&id=kr_010804000000&spage="+str(count+1))

for count in range(91):
    site_dgu_s_list_gookjae.append("https://www.dongguk.edu/mbs/kr/jsp/board/list.jsp?boardId=9457435&search=&column=&mcategoryId=0&boardType=01&listType=01&command=list&id=kr_010807000000&spage="+str(count+1))

for count in range(9):
    site_dgu_s_list_ippsii.append('https://www.dongguk.edu/mbs/kr/jsp/board/list.jsp?boardId=3654&search=&column=&mcategoryId=0&boardType=01&listType=01&command=list&id=kr_010803000000&spage='+str(count+1))

for count in range(8):
    site_dgu_s_list_haksul.append('https://www.dongguk.edu/mbs/kr/jsp/board/list.jsp?boardId=11533472&search=&column=&mcategoryId=0&boardType=01&listType=01&command=list&id=kr_010808000000&spage='+str(count+1))
dgu_s_fix = get_dgu_s_fixed(list(parser(gethtml(site_dgu_s), 'tr>td')))
dgu_s_haksa_fix = get_dgu_s_fixed(list(parser(gethtml(site_dgu_s_haksa), 'tr>td')))
dgu_s_gookjae_fix = get_dgu_s_fixed(list(parser(gethtml(site_dgu_s_gookjae), 'tr>td')))
dgu_s_janghak_fix = get_dgu_s_fixed(list(parser(gethtml(site_dgu_s_janghak), 'tr>td')))
dgu_s_haksul_fix = list(parser(gethtml(site_dgu_s_haksul), tag_dgu_s))
dgu_s_ippsii_fix = list(parser(gethtml(site_dgu_s_ippsii), tag_dgu_s))

#요걸로 입시,학술등록함
def setdb_dgu_s(length,geturl,makekey):
    for count in range(len(length)):
        parserd = parser(gethtml(length[count]), tag_dgu_s)
        print('                 ', count + 1)
        for countt in range(len(parserd)):
            print('     ', countt + 1)
            url = geturl(parserd, count + 1, countt).strip()
            urlcraw = parser(gethtml(url), 'div>strong')
            text = parser(gethtml(url), 'thead>tr>th')[0].text.strip().replace('\n', '').replace('\t', '')
            index = parser(gethtml(url), 'td.memo')[0].text.strip()
            writer = urlcraw[1].text.strip()
            date = urlcraw[2].text.strip()
            key = makekey(url)
            #db_handler.new_noti(set_db.db, "동국대학교 서울캠퍼스", key, writer, text, url, date, index)
"""
setdb_dgu_s(site_dgu_s_list_ippsii,dgu_s_url,mkkey)
setdb_dgu_s(site_dgu_s_list_haksul,dgu_s_url_haksul,mkkey_haksul)
"""

# 요걸로 학사, 장학 등록함
def setdb_dgu_s_fix(fixedlist,geturl,makekey):
    for count in range(len(fixedlist)):
        url = geturl(fixedlist,1,count).strip()
        urlparsered = parser(gethtml(url),'div>strong')
        urlparsered = list(urlparsered)
        text = parser(gethtml(url),'thead>tr>th')[0].text.strip().replace('\n','').replace('\t','')
        index = parser(gethtml(url),'td.memo')[0].text.strip()
        writer = urlparsered[1].text.strip()
        date = urlparsered[2].text.strip()
        key = makekey(url)
        print(count+1)
        #db_handler.new_noti(set_db.db, "동국대학교 서울캠퍼스", key, writer, text, url, date, index)

def setdb_dgu_s_unfix(unfixedlist,geturl,makekey):
    for count in range(len(unfixedlist)):
        parserd = parser(gethtml(unfixedlist[count]), tag_dgu_s)
        parserd_fix = parser(gethtml(unfixedlist[count]), 'tr>td')
        dgu_s_fix = get_dgu_s_fixed(list(parserd_fix))
        dgu_s_unfix = list((set(parserd)).difference(set(dgu_s_fix)))
        print('                 ', count + 1)
        for countt in range(len(dgu_s_unfix)):
            print('     ', countt + 1)
            url = geturl(dgu_s_unfix, count + 1, countt).strip()
            urlcraw = parser(gethtml(url), 'div>strong')
            text = parser(gethtml(url), 'thead>tr>th')[0].text.strip().replace('\n','').replace('\t','')
            index = parser(gethtml(url), 'td.memo')[0].text.strip()
            writer = urlcraw[1].text.strip()
            date = urlcraw[2].text.strip()
            key = makekey(url)
            #db_handler.new_noti(set_db.db, "동국대학교 서울캠퍼스", key, writer, text, url, date, index)


def update_1page_haksul(geturl,makekey):
    parserd = parser(gethtml(site_dgu_s_haksul), tag_dgu_s)
    for countt in range(len(parserd)):
        url = geturl(parserd, 1, countt).strip()
        urlcraw = parser(gethtml(url), 'div>strong')
        text = parser(gethtml(url), 'thead>tr>th')[0].text.strip().replace('\n', '').replace('\t', '')
        index = parser(gethtml(url), 'td.memo')[0].text.strip()
        writer = urlcraw[1].text.strip()
        date = urlcraw[2].text.strip()
        key = makekey(url)
        db_handler.new_noti(set_db.db, "동국대학교 서울캠퍼스", key, writer, text, url, date, index)


def update_1page_ippsii(geturl,makekey):
    parserd = parser(gethtml(site_dgu_s_ippsii), tag_dgu_s)
    for countt in range(len(parserd)):
        url = geturl(parserd, 1, countt).strip()
        urlcraw = parser(gethtml(url), 'div>strong')
        text = parser(gethtml(url), 'thead>tr>th')[0].text.strip().replace('\n', '').replace('\t', '')
        index = parser(gethtml(url), 'td.memo')[0].text.strip()
        writer = urlcraw[1].text.strip()
        date = urlcraw[2].text.strip()
        key = makekey(url)
        db_handler.new_noti(set_db.db, "동국대학교 서울캠퍼스", key, writer, text, url, date, index)

def update_1page_janghak(geturl,makekey):
    janghak_parsered = parser(gethtml(site_dgu_s_janghak),tag_dgu_s)
    for count in range(len(janghak_parsered)):
        url = geturl(janghak_parsered,1,count).strip()
        urlparsered = parser(gethtml(url),'div>strong')
        urlparsered = list(urlparsered)
        text = parser(gethtml(url),'thead>tr>th')[0].text.strip().replace('\n','').replace('\t','')
        index = parser(gethtml(url),'td.memo')[0].text.strip()
        writer = urlparsered[1].text.strip()
        date = urlparsered[2].text.strip()
        key = makekey(url)
        print(count+1)
        db_handler.new_noti(set_db.db, "동국대학교 서울캠퍼스", key, writer, text, url, date, index)


def update_1page_haksa(geturl,makekey):
    haksa_parsered = parser(gethtml(site_dgu_s_haksa), tag_dgu_s)
    for count in range(len(haksa_parsered)):
        url = geturl(haksa_parsered,1,count).strip()
        urlparsered = parser(gethtml(url),'div>strong')
        urlparsered = list(urlparsered)
        text = parser(gethtml(url),'thead>tr>th')[0].text.strip().replace('\n','').replace('\t','')
        index = parser(gethtml(url),'td.memo')[0].text.strip()
        writer = urlparsered[1].text.strip()
        date = urlparsered[2].text.strip()
        key = makekey(url)
        db_handler.new_noti(set_db.db, "동국대학교 서울캠퍼스", key, writer, text, url, date, index)

def update_1page_gookjae(geturl, makekey):
    haksa_parsered = parser(gethtml(site_dgu_s_gookjae), tag_dgu_s)
    for count in range(len(haksa_parsered)):
        url = geturl(haksa_parsered, 1, count).strip()
        urlparsered = parser(gethtml(url), 'div>strong')
        urlparsered = list(urlparsered)
        text = parser(gethtml(url), 'thead>tr>th')[0].text.strip().replace('\n', '').replace('\t', '')
        index = parser(gethtml(url), 'td.memo')[0].text.strip()
        writer = urlparsered[1].text.strip()
        date = urlparsered[2].text.strip()
        key = makekey(url)
        db_handler.new_noti(set_db.db, "동국대학교 서울캠퍼스", key, writer, text, url, date, index)

def update_1page_illban():
    parserd = parser(gethtml(site_dgu_s), tag_dgu_s)
    for countt in range(len(parserd)):
        url = dgu_s_url(parserd, 1, count).strip()
        urlcraw = parser(gethtml(url), 'div>strong')
        text = parser(gethtml(url), 'thead>tr>th')[0].text.strip()
        index = parser(gethtml(url), 'td.memo')[0].text.strip()
        writer = urlcraw[1].text.strip()
        date = urlcraw[2].text.strip()
        key = mkkey(url)
        db_handler.new_noti(set_db.db, "동국대학교 서울캠퍼스", key, writer, text, url, date, index)

def update_firstpage():
    update_1page_illban()
    update_1page_janghak(dgu_s_url, mkkey)
    update_1page_gookjae(dgu_s_url_gookjae, mkkey_gookjae)
    update_1page_haksa(dgu_s_url, mkkey)
    update_1page_haksul(dgu_s_url_haksul, mkkey_haksul)
    update_1page_ippsii(dgu_s_url, mkkey)
def dgu_s_fist():
    illban_parserd = set(textparser(parser(gethtml(site_dgu_s), tag_dgu_s)))
    janghak_parserd = set(textparser(parser(gethtml(site_dgu_s_janghak), tag_dgu_s)))
    gookjae_parserd = set(textparser(parser(gethtml(site_dgu_s_gookjae), tag_dgu_s)))
    haksa_parserd = set(textparser(parser(gethtml(site_dgu_s_haksa), tag_dgu_s)))
    haksul_parserd = set(textparser(parser(gethtml(site_dgu_s_haksul), tag_dgu_s)))
    ippsii_parserd = set(textparser(parser(gethtml(site_dgu_s_ippsii),tag_dgu_s)))
    return illban_parserd,janghak_parserd,gookjae_parserd,haksa_parserd,haksul_parserd,ippsii_parserd
def dgu_s_getnew(parserd):
    a,b,c,d,e,f = 0,0,0,0,0,0
    parserd = list(parserd)
    new_illban_parserd = set(textparser(parser(gethtml(site_dgu_s), tag_dgu_s)))
    new_janghak_parserd = set(textparser(parser(gethtml(site_dgu_s_janghak), tag_dgu_s)))
    new_gookjae_parserd = set(textparser(parser(gethtml(site_dgu_s_gookjae), tag_dgu_s)))
    new_haksa_parserd = set(textparser(parser(gethtml(site_dgu_s_haksa), tag_dgu_s)))
    new_haksul_parserd = set(textparser(parser(gethtml(site_dgu_s_haksul), tag_dgu_s)))
    new_ippsii_parserd = set(textparser(parser(gethtml(site_dgu_s_ippsii),tag_dgu_s)))
    if (len(parserd[0].difference(new_illban_parserd)) > 0):
        a = 1
        parserd[0] = new_illban_parserd
    if (len(parserd[1].difference(new_janghak_parserd)) > 0):
        b = 1
        parserd[1] = new_janghak_parserd
    if (len(parserd[2].difference(new_gookjae_parserd)) > 0):
        c = 1
        parserd[2] = new_gookjae_parserd
    if (len(parserd[3].difference(new_haksa_parserd)) > 0):
        d = 1
        parserd[3] = new_haksa_parserd
    if (len(parserd[4].difference(new_haksul_parserd)) > 0):
        e = 1
        parserd[4] = new_haksul_parserd
    if (len(parserd[5].difference(new_ippsii_parserd)) > 0):
        f = 1
    if (a ==  1):
        print('dgu_s의 일반 게시글이 추가됩니다.')
        update_1page_illban()
    if (b == 1):
        print('dgu_s의 장학 게시글이 추가됩니다.')
        update_1page_janghak(dgu_s_url, mkkey)
    if (c == 1):
        print('dgu_s의 국제 게시글이 추가됩니다.')
        update_1page_gookjae(dgu_s_url_gookjae, mkkey_gookjae)
    if (d == 1):
        print('dgu_s의 학사 게시글이 추가됩니다.')
        update_1page_haksa(dgu_s_url,mkkey)
    if (e == 1):
        print('dgu_s의 학술 게시글이 추가됩니다.')
        update_1page_haksul(dgu_s_url_haksul,mkkey_haksul)
    if (f == 1):
        print('dgu_s의 학술 게시글이 추가됩니다.')
        update_1page_haksul(dgu_s_url,mkkey)
    return parserd

"""
setdb_dgu_s_fix(dgu_s_janghak_fix, dgu_s_url, mkkey)
setdb_dgu_s_unfix(site_dgu_s_list_janghak, dgu_s_url, mkkey)
setdb_dgu_s_fix(dgu_s_gookjae_fix, dgu_s_url_gookjae, mkkey_gookjae)
setdb_dgu_s_unfix(site_dgu_s_list_gookjae,dgu_s_url_gookjae, mkkey_gookjae)
"""


"""
#요걸로 일반 등록함
 # 일반게시글 고정계시글 등록
for count in range(len(dgu_s_fix)):
    url = dgu_s_url(dgu_s_fix,1,count).strip()
    urlparsered = parser(gethtml(url),'div>strong')
    urlparsered = list(urlparsered)
    text = parser(gethtml(url),'thead>tr>th')[0].text.strip()
    index = parser(gethtml(url),'td.memo')[0].text.strip()
    writer = urlparsered[1].text.strip()
    date = urlparsered[2].text.strip()
    key = mkkey(url)
    db_handler.new_noti(db, "동국대학교 서울캠퍼스", key, writer, text, url, date, index)




# 일반계시글 비고정계시글 등록
for count in range(len(site_dgu_s_list)):
    parserd = parser(gethtml(site_dgu_s_list[count]),tag_dgu_s)
    parserd_fix = parser(gethtml(site_dgu_s_list[count]), 'tr>td')
    dgu_s_fix = get_dgu_s_fixed(list(parserd_fix))
    dgu_s_unfix = list((set(parserd)).difference(set(dgu_s_fix)))
    print('                 ',count+1)
    for countt in range(len(dgu_s_unfix)):
        print('     ',countt+1)
        url = dgu_s_url(dgu_s_unfix,count+1,countt).strip()
        urlcraw = parser(gethtml(url), 'div>strong')
        text = parser(gethtml(url), 'thead>tr>th')[0].text.strip()
        index = parser(gethtml(url), 'td.memo')[0].text.strip()
        writer = urlcraw[1].text.strip()
        date = urlcraw[2].text.strip()
        key = mkkey(url)
        db_handler.new_noti(db, "동국대학교 서울캠퍼스", key, writer, text, url, date, index)
"""
