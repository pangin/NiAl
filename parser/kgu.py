import crawler
import db_handler
import set_db
site_kgu = 'http://www.kyonggi.ac.kr/boardList.kgu?bcode=B0039&mzcode=K00M0403&orgCd=G&pF=1&lgF=1&yyyy='
tag_kgu = 'td.subject'
site_kgu_list = []


for count in range(1860):
    site_kgu_list.append('http://www.kyonggi.ac.kr/boardList.kgu?bcode=B0039&mzcode=K00M0403&orgCd=G&pF='+str(count+1)+'&lgF=1&yyyy=')

def kgu_url(parsered,page,i):
    z = str(parsered[i])
    num1 = z.find('amp;id=')
    num2 = z.find('pid=')
    urlnum = z[num1+7:num1+13]
    urlnum2 = z[num2+4:num2+9]
    url = 'http://www.kyonggi.ac.kr/boardView.kgu?bcode=B0039&id='+urlnum+'&pid='+urlnum2+'&pF='+str(page)+'&lgF=1&mzcode=K00M0403&orgCd=G'
    return url


def mkkey(url):
    num1 = url.find('B0039&id=')
    num2 = url.find('pid=')
    urlnum = url[num1 + 9:num1 + 15]
    urlnum2 = url[num2 + 4:num2 + 9]
    urll = url.replace('http://www.kyonggi.ac.kr/boardView.kgu?bcode=B0039&id='+urlnum+'&pid='+urlnum2+'&pF=', '')
    urll = urll.replace('&lgF=1&mzcode=K00M0403&orgCd=G', '')
    return (urlnum+urlnum2+urll)



"""
for count in range(1860):
    parsered = crolling.parser(crolling.gethtml(site_kgu_list[count]), tag_kgu)
    print(count+1)
    parsered = list(parsered)
    for countt in range(len(parsered)):
        secret_text = str(parsered[countt])
        secret = secret_text.find('비밀글')
        if (secret != -1):
            continue
        print('     ', countt+1)
        urll = kgu_url(parsered, count + 1, countt).strip()
        url = str(urll)
        url_craw = crolling.parser(crolling.gethtml(urll), 'tr>td')
        index = str(crolling.parser(crolling.gethtml(urll), 'td.substance')[0].text.strip())
        text = str((url_craw[0].text.strip()))
        date = str(url_craw[3].text.strip())
        writer = str(url_craw[1].text.strip())
        key = mkkey(url)
        db_handler.new_noti(set_db.db, "경기대학교", key, writer, text, url, date, index)
"""

def update_1page():
    parserd = crawler.parser(crawler.gethtml(site_kgu), tag_kgu)
    for count in range(len(parserd)):
        secret_text = str(parserd[count])
        secret = secret_text.find('비밀글')
        if (secret != -1):
            continue
        urll = kgu_url(parserd,1, count)
        url = str(urll)
        url_craw = crawler.parser(crawler.gethtml(urll), 'tr>td')
        index = str(crawler.parser(crawler.gethtml(urll), 'td.substance')[0].text.strip())
        text = str((url_craw[0].text.strip()))
        date = str(url_craw[3].text.strip())
        writer = str(url_craw[1].text.strip())
        key = mkkey(url)
        print('  ',count+1)
        db_handler.new_noti(set_db.db, "경기대학교", key, writer, text, url, date, index)

def update_firstpage():
    update_1page()

def first_parser():
    parserd = set(crawler.ttextparser(crawler.parser(crawler.gethtml(site_kgu), tag_kgu)))
    return parserd

def kgu_getnew(parserd):
    new_parserd = set(crawler.ttextparser(crawler.parser(crawler.gethtml(site_kgu), tag_kgu)))
    diffrence = parserd.difference(new_parserd)
    if(len(diffrence) > 0):
        print('kgu 의 게시글이 추가됩니다.')
        update_1page()
        return new_parserd
    else:
        return parserd
