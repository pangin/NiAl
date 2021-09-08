from lib import db_handler
from parser import crawler, set_db

site_dgu_g = "https://web.dongguk.ac.kr/mbs/kr/jsp/board/list_all.jsp?boardId=0&search=&column=&categoryDepth=&categoryId=0&mcategoryId=&boardType=01&listType=01&command=list&id=kr_070101000000&spage=1"
tag_dgu_g = 'td.subject'
tag_dgu_fix = 'td.subject.new'
site_dgu_g_list = []


def lastpage_dgu_g():
    z = str((crawler.parser(crawler.gethtml(site_dgu_g), 'li.last')))
    page = z.find('spage')
    return int(z[page+6:page+9])


def find_new(parsered):
    a = []
    for count in range(int(len(parsered) / 6)):
        if (len(str(parsered[6 * count])) > 9):
            a.append(int(parsered[6 * count].text))
    return max(a)


def dgu_g_url(parsered,page,i):
    z = str(parsered[i])
    num1 = z.find('boardSeq=')
    num2 = z.find('boardId=')
    num3 = z.find('id=kr_')
    urlnum = z[num1+9:num1+15]
    urlnum2 = z[num2+8:num2+11]
    urlnum3 = z[num3+6:num3+18]
    url = 'https://web.dongguk.ac.kr/mbs/kr/jsp/board/view.jsp?spage='+str(page)+'&boardId='+str(urlnum2)+'&boardSeq='+str(urlnum)+'&id=kr_'+str(urlnum3)+'&noticeType=all'
    return url


def boardseq(parserd):
    z = str(parserd)
    num1 = z.find('boardSeq=')
    urlnum = z[num1 + 9:num1 + 15]
    return urlnum


def mkkey(url):
    num1 = url.find('boardSeq=')
    num2 = url.find('boardId=')
    num3 = url.find('id=kr_')
    urlnum = url[num1 + 9:num1 + 15]
    urlnum2 = url[num2 + 8:num2 + 11]
    urlnum3 = url[num3 + 6:num3 + 18]
    urlnum4 = url.replace('https://web.dongguk.ac.kr/mbs/kr/jsp/board/view.jsp?spage=', '')
    urlnum4 = urlnum4.replace('&boardId=' + urlnum2 + '&boardSeq=' + urlnum + '&id=kr_' + urlnum3 + '&noticeType=all', '')
    return urlnum + urlnum2 + urlnum3 + urlnum4


for count in range(lastpage_dgu_g()):
    site_dgu_g_list.append("https://web.dongguk.ac.kr/mbs/kr/jsp/board/list_all.jsp?boardId=0&search=&column=&categoryDepth=&categoryId=0&mcategoryId=&boardType=01&listType=01&command=list&id=kr_070101000000&spage="+str(count+1))
    count = count + 1

dgu_fixed = crawler.parser(crawler.gethtml(site_dgu_g), tag_dgu_fix)

"""
for count in range(len(dgu_fixed)):
    urll = dgu_g_url(dgu_fixed, 1, count)
    url = str(urll)
    url_craw = crolling.parser(crolling.gethtml(urll), 'tr>td')
    index = crolling.parser(crolling.gethtml(urll), 'div.editor')[0].text.strip()
    text = crolling.parser(crolling.gethtml(urll),'th.subject')[0].text.strip().strip('0').strip().strip('0').strip()
    date = url_craw[1].text.strip()
    writer = url_craw[0].text.strip()
    key = mkkey(url)
    db_handler.new_noti(db, "동국대학교 경주캠퍼스", key, writer, text, url, date, index)
    print(count)

print(len(site_dgu_g_list))


for count in range(len(site_dgu_g_list)):
    parsered = set(crolling.parser(crolling.gethtml(site_dgu_g_list[count]),tag_dgu_g)).difference(set(crolling.parser(crolling.gethtml(site_dgu_g_list[count]),tag_dgu_fix)))

    print(count+1)
    parsered = list(parsered)
    for countt in range(len(parsered)):
        print('     ',countt+1)
        urll = dgu_g_url(parsered, count + 1, countt).strip()
        url = str(urll)
        url_craw = crolling.parser(crolling.gethtml(urll), 'tr>td')
        index = str(crolling.parser(crolling.gethtml(urll), 'div.editor')[0].text.strip())
        text = str(crolling.parser(crolling.gethtml(urll),'th.subject')[0].text.strip().strip('0').strip().strip('0').strip())
        date = str(url_craw[1].text.strip())
        writer = str(url_craw[0].text.strip())
        key = mkkey(url)
        db_handler.new_noti(db,"동국대학교 경주캠퍼스", key, writer, text, url, date, index)
"""


def update_1page():
    dgu_url = 'https://web.dongguk.ac.kr/mbs/kr/jsp/board/list_all.jsp?boardId=0&search=&column=&categoryDepth=&categoryId=0&mcategoryId=&boardType=01&listType=01&command=list&id=kr_070101000000&spage=1'
    parserd = crawler.parser(crawler.gethtml(dgu_url), tag_dgu_g)
    for count in range(len(parserd)):
        urll = dgu_g_url(parserd, 1, count)
        url = str(urll)
        url_craw = crawler.parser(crawler.gethtml(urll), 'tr>td')
        index = crawler.parser(crawler.gethtml(urll), 'div.editor')[0].text.strip()
        text = crawler.parser(crawler.gethtml(urll), 'th.subject')[0].text.strip().strip('0').strip().strip('0').strip()
        date = url_craw[1].text.strip()
        writer = url_craw[0].text.strip()
        key = mkkey(url)
        #print(url, '\n', index, '\n', date, '\n', text, '\n', writer, '\n', key)
        print('     ', count+1)
        db_handler.new_noti(set_db.db, "동국대학교 경주캠퍼스", key, writer, text, url, date, index)


def update_firstpage():
    update_1page()


def dgu_g_first_parser():
    par = crawler.parser(crawler.gethtml(site_dgu_g), 'tr>td')
    value = find_new(par)
    return value


def dgu_getnew(input):
    new_parserd = crawler.parser(crawler.gethtml(site_dgu_g), 'tr>td')
    new = find_new(new_parserd)
    if new > input:
        print('dgu 의 게시글이 추가됩니다.')
        update_1page()
    return new
