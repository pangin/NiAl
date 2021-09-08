import crawler
import db_handler
import set_db
hany_tag_writer = 'div.notice-writer'
hany_tag_date = 'div.notice-date'
hany_tag_title = 'p.title'
site_hany_hakksa = 'https://www.hanyang.ac.kr/web/www/notice_all?p_p_id=viewNotice_WAR_noticeportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_viewNotice_WAR_noticeportlet_sCategoryId=1&_viewNotice_WAR_noticeportlet_sCurPage=1&_viewNotice_WAR_noticeportlet_action=view'

def get_site_list(categoryId,count):
    url_list = []
    for count in range(count):
        url = 'https://www.hanyang.ac.kr/web/www/notice_all?p_p_id=viewNotice_WAR_noticeportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_viewNotice_WAR_noticeportlet_sCategoryId='+str(categoryId)+'&_viewNotice_WAR_noticeportlet_sCurPage='+str(count+1)+'&_viewNotice_WAR_noticeportlet_action=view'
        url_list.append(url)
    return url_list

def get_site_url(categoryId):

    url = 'https://www.hanyang.ac.kr/web/www/notice_all?p_p_id=viewNotice_WAR_noticeportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_viewNotice_WAR_noticeportlet_sCategoryId='+str(categoryId)+'&_viewNotice_WAR_noticeportlet_sCurPage=1&_viewNotice_WAR_noticeportlet_action=view'
    return url


def kgu_url(parsered,page,i):
    z = str(parsered[i])
    num1 = z.find('amp;id=')
    num2 = z.find('pid=')
    urlnum = z[num1+7:num1+13]
    urlnum2 = z[num2+4:num2+9]
    url = 'http://www.kyonggi.ac.kr/boardView.kgu?bcode=B0039&id='+urlnum+'&pid='+urlnum2+'&pF='+str(page)+'&lgF=1&mzcode=K00M0403&orgCd=G'
    return url
def get_hany_url(url,page,categoryId):
    url = str(url)
    num1 = url.find('message(')
    urlnum1 = url[num1+8:num1+14].replace(')','')
    urlnum1 = urlnum1.replace(';','')
    url = 'https://www.hanyang.ac.kr/web/www/notice_all?p_p_id=viewNotice_WAR_noticeportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_viewNotice_WAR_noticeportlet_sCategoryId='+str(categoryId)+'&_viewNotice_WAR_noticeportlet_sCurPage='+str(page)+'&_viewNotice_WAR_noticeportlet_sUserId=0&_viewNotice_WAR_noticeportlet_action=view_message&_viewNotice_WAR_noticeportlet_messageId='+str(urlnum1)
    return url

def makky(url,categoryId,page):
    url = str(url)
    num1 = url.find('CategoryId=')
    num2 = url.find('messageId=')
    categoryId = str(categoryId)
    messageId = url[num2+10:num2+16].replace(')','')
    messageId = messageId.replace(';','')
    page = url.replace('https://www.hanyang.ac.kr/web/www/notice_all?p_p_id=viewNotice_WAR_noticeportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_viewNotice_WAR_noticeportlet_sCategoryId='+categoryId+'&_viewNotice_WAR_noticeportlet_sCurPage=','')
    page = page.replace('&_viewNotice_WAR_noticeportlet_sUserId=0&_viewNotice_WAR_noticeportlet_action=view_message&_viewNotice_WAR_noticeportlet_messageId='+messageId,'')
    return (categoryId+messageId+page)

def totpage(url):
    totpage = str(crawler.parser(crawler.gethtml(url), 'div>div>div>div>span')[3]).strip()
    totpage = totpage.replace('전체', '')
    totpage = totpage.replace('건', '')
    totpage = totpage.replace('<span>','')
    totpage = totpage.replace('</span>','').strip()
    totpage = int(totpage)
    if (totpage % 10 == 0):
        totpage = totpage/10
    else:
        totpage = int(totpage/10) + 1

    return totpage


"""
학사 1, 3856p
입학 2, 343p
모집 3, 1044
사회봉사 4, 116
일반 5, 2945
산학 6, 303
행사 7, 551
장학 8, 403
학회 9, 17
"""
def setdb_hany(categoryId):
    page_url = get_site_url(categoryId)
    print(page_url)
    page = totpage(page_url)
    page = int(page)
    site_hany_list = get_site_list(categoryId,page)
    for count in range(len(site_hany_list)):
        parserd = crawler.parser(crawler.gethtml(site_hany_list[count]), hany_tag_title)
        writer = crawler.parser(crawler.gethtml(site_hany_list[count]), hany_tag_writer)
        date = crawler.parser(crawler.gethtml(site_hany_list[count]), hany_tag_date)
        parserd = list(parserd)
        print('             ', count + 1)
        for countt in range(len(parserd)):
            print(' ', countt + 1)
            url = get_hany_url(parserd[countt], count + 1,categoryId).strip()
            text = parserd[countt].text.strip().replace('\n','').replace('\t','')
            indexx = crawler.parser(crawler.gethtml(url), 'tbody')
            if(len(indexx) == 0):
                index = ''
            else:
                index = indexx[0].text.strip()
            writerr = writer[countt].text.strip()
            datee = date[countt].text.strip()
            key = makky(url,categoryId,count)
            db_handler.new_noti(set_db.db, "한양대학교", key, writerr, text, url, datee, index)




def update_1page(categoryId):
    site_hany_list = get_site_list(categoryId, 1)
    parserd = crawler.parser(crawler.gethtml(site_hany_list[0]), hany_tag_title)
    writer = crawler.parser(crawler.gethtml(site_hany_list[0]), hany_tag_writer)
    date = crawler.parser(crawler.gethtml(site_hany_list[0]), hany_tag_date)
    parserd = list(parserd)
    for countt in range(len(parserd)):
        url = get_hany_url(parserd[countt], 1, categoryId).strip()
        text = parserd[countt].text.strip().replace('\n', '').replace('\t', '')
        indexx = crawler.parser(crawler.gethtml(url), 'tbody')
        if (len(indexx) == 0):
            index = ''
        else:
            index = indexx[0].text.strip()
        writerr = writer[countt].text.strip()
        datee = date[countt].text.strip()
        key = makky(url, categoryId, 1)
        print(countt+1)
        db_handler.new_noti(set_db.db, "한양대학교", key, writerr, text, url, datee, index)


def update_first_page():
    for i in range(9):
        update_1page(int(i+1))

def fisrt_parser():
    a = []
    for i in range(9):
        a.append(set(crawler.ttextparser(crawler.parser(crawler.gethtml(get_site_url(int(i + 1))), hany_tag_title))))
    return a
def hany_getneww(categoryId,parserd):
    new_parserd = set(crawler.ttextparser(crawler.parser(crawler.gethtml(get_site_url(categoryId)), hany_tag_title)))
    diffrence = parserd.difference(new_parserd)
    if (len(diffrence) > 0):
        a = 1
        return a,new_parserd
    else:
        a = 0
    return a,parserd
def hany_getnew(a):
    value = []
    value2 = []
    for i in range(9):
        result = list(hany_getneww(i + 1, a[i]))
        value.append(result[0])
        value2.append(result[1])
    for i in range(9):
        if (value[i] == 1):
            update_1page(int(i+1))
    return value2