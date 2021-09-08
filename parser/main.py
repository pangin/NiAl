import datetime

from parser import kgu, dgu_g, hany, dgu_s

count = 1

"""
print("초기 첫 페이지 등록...")
#모든 학교의 공지사항의 첫 1페이지를 db에 등록, 프로그램을 중지하였다가 다시 실행시킬때를 위한 부분
kgu.update_firstpage()
dgu_g.update_firstpage()
hany.update_first_page()
dgu_s.update_firstpage()
"""

print('초기 값 읽어옴....') # 학교별로 현재 첫페이지에 등록되어 있는 공지사항 목록들을 저장한다
kgu_first = kgu.first_parser()
dgu_first = dgu_g.dgu_g_first_parser()
hany_first = hany.fisrt_parser()
dgu_s_first = dgu_s.dgu_s_fist()
now = datetime.datetime.now()
print('완료! 현재시각 ', now.year, '년', now.month, '월', now.day, '일', now.hour, '시', now.minute, '분', now.second, '초 부터 계시물을 최신화 합니다.')
while True:  # 학교별로 현재 첫 패이지에 등록되어 있는 공지사항을 파싱하여 새로운 개시글이 생기게 되면 db에 등록해준다. 등록하였다면 최신화된 계시글을 다시 저장한다.
    kgu_first = kgu.kgu_getnew(kgu_first)
    dgu_first = dgu_g.dgu_getnew(dgu_first)
    hany_first = hany.hany_getnew(hany_first)
    dgu_s_first = dgu_s.dgu_s_getnew(dgu_s_first)
    # print(count)
    # count = count + 1
