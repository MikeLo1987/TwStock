# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 14:14:09 2024

@author: thewh
"""

import os
import pandas as pd
from datetime import datetime
from datetime import date
import matplotlib.pyplot as plt

path1 = 'D:/Python爬蟲程式與資料視覺化開發-專題/price/'
# 提示使用者輸入查詢之起訖日，並將輸入結果轉換為 datetime 物件。
symbol = input("請輸入股票代號:")
date_start = input("請輸入開始查詢之日期，格式為YYYY-mm-dd:")
date_start = date.fromisoformat(date_start)
date_end = input("請輸入結束查詢之日期，格式為YYYY-mm-dd:")
date_end = date.fromisoformat(date_end)

def stock(symbol):
    x = []
    for i in range(int(str(date_start).replace('-','')), int(str(date_end).replace('-',''))+1):
        x.append(i)
    
    dfs = []
    y = []
    for date in x:
        filename = f'{date}.csv' # 將date轉換為字串
        # 將path1與filename組合在一起
        filepath = os.path.join(path1, filename)
        # 檢查檔案是否存在
        if os.path.isfile(filepath):
            df = pd.read_csv(filepath)
            dfs.append(df)
            # 將交易日儲存至y
            y.append(str(date))
    
    for i in range(len(dfs)):
        # 整理DataFrame，只留下需要的欄位
        dfs[i] = dfs[i][['symbol', '開盤價', '最高價', '最低價', '收盤價']]
        dfs[i] = dfs[i][dfs[i]['symbol'].isin([int(symbol)])]
        # 建立日期物件
        date_obj = datetime.strptime(y[i], '%Y%m%d')
        # 將日期物件轉換為字串
        date_str = date_obj.strftime('%Y/%m/%d')
        # 新增日期欄位
        dfs[i]['日期'] = [date_str]
    # 將每一天的數據合併成一個表格
    target = pd.concat(dfs)
    target = target.reset_index(drop=True)
    return target

path2 = 'D:/Python爬蟲程式與資料視覺化開發-專題/'

df = stock(symbol)
df.to_csv(path2 + symbol + '.csv')
print('已儲存CSV檔')

plt.rc("font", family="Microsoft JhengHei")
for i in range(len(df)):
    date = df.loc[i, '日期']
    open_price = df.loc[i, '開盤價']
    close_price = df.loc[i, '收盤價']
    highest = df.loc[i, '最高價']
    lowest = df.loc[i, '最低價']
    #決定陰線(下跌)或陽線(上漲)
    color = 'red'
    if open_price > close_price:
        color = 'green'
    #畫陰陽線
    plt.bar(date,
            abs(open_price - close_price),
            bottom=min(open_price, close_price),
            color=color, width=0.5)
    #畫影線
    plt.bar(date,
            highest - lowest,
            bottom=lowest, color=color, width=0.1)
    
plt.title(symbol + " K線圖", fontsize = 20)
plt.xlabel("日期", fontsize = 16)
plt.ylabel("價格", fontsize = 16)
plt.xticks(rotation=15)
plt.show()