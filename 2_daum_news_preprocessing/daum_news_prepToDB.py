import glob
import pandas as pd
import re
import os
import sqlite3
import numpy as np

daumNews_dir = glob.glob('daum_news_dataset/*.csv')


def preprocessing_articles(data):
    contents_new = []
    for content in data['content']:
        content = str(content).split('\n')
        content = list(filter(lambda s: len(s) > 3, content))
        content_prep = content[:-1]
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

        content_prep = list(map(lambda s: re.sub("\[.*\]", "", s), content_prep))  # [스포츠서울]
        content_prep = list(map(lambda s: re.sub("\(.*\=.*\)", "", s), content_prep))  # (서울=뉴시스)
        content_prep = list(map(lambda s: re.sub("\【.*\=.*\】", "", s), content_prep))  # 【파이낸셜뉴스 포천=강근주 기자】
        content_prep = list(map(lambda s: re.sub('[^가-힣]', ' ', s), content_prep))  # 한글 제외 영문, 한자, 숫자, 특수문자 모두 제거

        contents_new.append(''.join(content_prep))

    data['news_content'] = contents_new

    return data


if __name__ == "__main__":
    con = sqlite3.connect("kr_scrapping.db")
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
    result_csv = pd.DataFrame()
    cnt = 0
    for daumNews in daumNews_dir:
        cnt += 1
        print(round(len(daumNews_dir)/cnt,1),'%', daumNews)
        data_prep = pd.DataFrame()
        df = pd.read_csv(daumNews, names=['order', 'news_name', 'pubdate', 'url', 'content'])
        df = df.drop(['order'], axis=1)
        data_prep = preprocessing_articles(df)
        data_prep['news_content'] = data_prep['news_content'].str.strip()
        data_prep['news_content'] = data_prep['news_content'].replace('', np.nan)
        data_prep_drop = data_prep.dropna(axis=0)
        data_prep_drop_dup = data_prep_drop.drop_duplicates(['news_content'], keep='first', inplace=False,
                                                            ignore_index=True)
        result = data_prep_drop_dup[['news_name', 'pubdate', 'url', 'news_content']]
        # result_csv = pd.concat([result_csv, result], axis=0)
        result.to_sql('news_dummy', con, if_exists='append', index=False)
    # result_csv.to_csv('test.csv', encoding='utf-8-sig')
    con.commit()
    con.close()