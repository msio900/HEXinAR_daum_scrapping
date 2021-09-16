import csv
from socket import MSG_MCAST
from urllib.parse import quote, quote_plus
import requests
from bs4 import BeautifulSoup
import pandas as pd


strDate = '20200807'
endDate = '20200807'
dt_index = pd.date_range(start=strDate, end=endDate)
dt_list = dt_index.strftime("%Y%m%d").tolist()

cnt = 0
max_page = 10000 # 뉴스 페이지 탭 수 지정
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"}

def 


if __name__ == '__main__':
    filename = f"daum_news_{strDate}-{endDate}.csv"
    f = open(filename, "w", encoding="utf-8-sig", newline="")
    writer = csv.writer(f)

    for i in dt_list:
        print(i)
        for j in range(1534, max_page):
            # print(j, j+1)
            main_url = f"https://news.daum.net/breakingnews/?page={j}&regDate={i}" # url 입력
            res = requests.get(main_url, headers=headers)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "lxml") # soup으로 저장
            main = soup.find("ul", attrs={"class":"list_news2 list_allnews"})

            val_url = f"https://news.daum.net/breakingnews/?page={j+1}&regDate={i}"
            val = requests.get(val_url, headers=headers)
            val.raise_for_status()
            val_soup = BeautifulSoup(val.text, "lxml")
            val_main = val_soup.find("ul", attrs={"class":"list_news2 list_allnews"})
            

            if main != val_main:
                news = main.find_all("strong", attrs={"class":"tit_thumb"})
                for new in news:
                    urls = new.select_one("a")["href"]# 페이지에 나와있는 뉴스 URL 변수 입력
                    # print(urls)

                    result = requests.get(urls)         # request 로 다시 개별 뉴스 접속
                    result.raise_for_status()
                    news_soup = BeautifulSoup(result.text, "lxml")
                    # 뉴스 제목, 발행시간, 기사본문 저장
                    title = news_soup.find("h3", attrs={"tit_view"}).get_text().strip()
                    pubdate = news_soup.find("span", attrs={"num_date"}).get_text().strip()
                    text = news_soup.find("div", attrs={"news_view"}).get_text().strip()
                    cnt += 1
                    print(cnt)
                    writer.writerow([cnt, title, pubdate, urls, text])

            else:
                news = main.find_all("strong", attrs={"class":"tit_thumb"})
                for new in news:
                    urls = new.select_one("a")["href"]# 페이지에 나와있는 뉴스 URL 변수 입력
                    # print(urls)

                    result = requests.get(urls)         # request 로 다시 개별 뉴스 접속
                    result.raise_for_status()
                    news_soup = BeautifulSoup(result.text, "lxml")
                    # 뉴스 제목, 발행시간, 기사본문 저장
                    title = news_soup.find("h3", attrs={"tit_view"}).get_text().strip()
                    pubdate = news_soup.find("span", attrs={"num_date"}).get_text().strip()
                    text = news_soup.find("div", attrs={"news_view"}).get_text().strip()
                    cnt += 1
                    print(cnt, title, pubdate, urls)
                    writer.writerow([cnt, title, pubdate, urls, text])

                break