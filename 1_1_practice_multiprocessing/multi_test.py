from bs4 import BeautifulSoup
import requests
import time
from multiprocessing import Pool, Manager, freeze_support
search_word = "삼성" #검색어 지정
end = 300 #마지막 뉴스 지정
 
#list를 공유 하기 위해
manager = Manager()
title_list = manager.list()
 
def title_to_list(start):
    global title_list
    #url making
    url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}&start={}'.format(search_word,start)
    req = requests.get(url)
 
    #정상적인 request 확인
    if req.ok:
        html = req.text
        soup = BeautifulSoup(html,'html.parser')
    
        #뉴스제목 뽑아오기
        titles = soup.select(
            'div > a.news_tit'
        )
 
        #list에 넣어준다
        for title in titles:
            title_list.append(title['title'])

if __name__ == '__main__':
    freeze_support()
    
    start_time = time.time()
    pool = Pool(processes=4) #4개의 프로세스 동시에 작동
    pool.map(title_to_list,range(1,end,10)) #title_to_list라는 함수에 1 ~ end까지 10씩늘려가며 인자로 적용
    print(title_list)
    print("실행 시간 : %s초" % (time.time() - start_time))
