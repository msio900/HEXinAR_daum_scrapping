import glob
import pandas as pd
import re
import os
import sqlite3
import numpy as np

daumNews_dir = glob.glob('./glob_test/*.csv')

for daumNews in daumNews_dir:
    csv_df = pd.read_csv(daumNews, names=['order', 'news_name', 'pubdate', 'url', 'content'])  # 컬럼이름 지정

    for i in csv_df['news_name']:
        print(i)