import glob
import pandas as pd
import re
import os
import sqlite3
import numpy as np
import csv

daumNews_dir = glob.glob('../daum_news_dataset/*.csv')


def preprocessing_articles(data):
    contents_new = []
    for content in data['content']:
        # content = content.fillna("")
        content = str(content).split('\n')
        content = list(filter(lambda s: len(s) > 3, content))

        # 글 마지막에 항상 기자의 메일 주소가 추가되어 있다. 그 이후로 나오는 글은 불필요하므로 삭제함
        for i in range(1, len(content)):
            if '@' in content[-i]:
                break
        if i == len(content) - 1:
            i = 1
        content_prep = content[:-i]

            # 너무 짧거나, 광고, copyright, 사진설명, 메일 등 불필요한 단어가 포함되어 있을 경우 불필요한 문장으로 판단하고 삭제 처리
        content_prep = list(filter(lambda s: len(s) > 30 and \
                                             '▶' not in s and \
                                             '©' not in s and \
                                             '▲' not in s and \
                                             '사진=' not in s and \
                                             '사진제공=' not in s and \
                                             '@' not in s and \
                                             not re.findall("기자 *$", s) and \
                                             not re.findall("제공 *$", s) and \
                                             not re.findall("이하", s) and \
                                             not re.findall("무단전재", s) and \
                                             not re.findall("기자 *= *", s), content_prep))

        # 언론사명이 들어간 prefix 삭제
        content_prep = list(map(lambda s: re.sub("\[.*\]", "", s), content_prep))  # [스포츠서울]
        content_prep = list(map(lambda s: re.sub("\(.*\=.*\)", "", s), content_prep))  # (서울=뉴시스)
        content_prep = list(map(lambda s: re.sub("\【.*\=.*\】", "", s), content_prep))  # 【파이낸셜뉴스 포천=강근주 기자】
        # content_prep = list(map(lambda s: re.sub('[^A-Za-z가-힣]',' ', s), content_prep)) # 한글 제외 영문, 한자, 숫자, 특수문자 모두 제거
        content_prep = list(map(lambda s: re.sub('[^가-힣]', ' ', s), content_prep))  # 한글 제외 영문, 한자, 숫자, 특수문자 모두 제거

        contents_new.append('\n'.join(content_prep))
        # print('for 안',len(contents_new))
    # cnt =+ 1
    # print(cnt, contents_new)
    # print('for 밖',len(contents_new))
    data['news_content'] = contents_new
    return data


if __name__ == "__main__":
    con = sqlite3.connect("scrapping.db")   # 데이터베이스 이름
    c = con.cursor()
    c.execute('DROP TABLE IF EXISTS `news_dummy`;')
    c.execute('''
            CREATE TABLE `news_dummy` (
                `news_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                `news_name` TEXT NOT NULL,
                `pubdate` TEXT NOT NULL,
                `url` TEXT NOT NULL,
                `news_content` TEXT NOT NULL
            );

    ''')
    full_dataset = pd.DataFrame()
    for daumNews in daumNews_dir:
        df = pd.read_csv(daumNews, names=['order', 'news_name', 'pubdate', 'url', 'content'])  # 컬럼이름 지정
        df = df.drop(['order'], axis=1)
        # print(df)
        data_prep = preprocessing_articles(df)
        full_dataset = pd.concat([full_dataset, data_prep], axis=0)
        # full_dataset.to_csv('test.csv', encoding='utf-8-sig')
        
        # print(data_prep)
        # full_dataset['news_content'] = full_dataset['news_content'].str.replace(' ', '')
        full_dataset['news_content'] = full_dataset['news_content'].str.replace('\n',' ')
        full_dataset['news_content'] = full_dataset['news_content'].str.strip()
        full_dataset['news_content'] = full_dataset['news_content'].replace('', np.nan)    # 빈셀이 있는 행을 삭제하기 위해 NaN으로 변경
        data_prep_drop = full_dataset.dropna(axis=0)
        data_prep_drop_dup = data_prep_drop.drop_duplicates(['news_content'], keep='first', inplace=False, ignore_index=True)   # 중복값 제거
        result = data_prep_drop_dup[['news_name', 'pubdate', 'url', 'news_content']]  # 비교를 위해 content(원본데이터) 추가, news_content가 전처리된 데이터
        # result.to_csv('test.csv', encoding='utf-8-sig')
    result.to_sql('news_dummy', con, if_exists='append', index=False)         # DB에 news_dummy 라는 테이블 이름으로 저장

    con.commit()
    con.close()