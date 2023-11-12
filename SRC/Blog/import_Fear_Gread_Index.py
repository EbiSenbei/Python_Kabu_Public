# Fear&Greed Index(恐怖と強欲指数)を取得
import requests, csv, json, urllib
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib 
# %matplotlib inline
import yfinance as yf
from dateutil.relativedelta import relativedelta
from fake_useragent import UserAgent
from datetime import datetime
import warnings
warnings.simplefilter('ignore')

if __name__ == '__main__':
    print("/*--START-----------------------------------------------------*/")

    # データ設定----------------------------------------------------------------
    ticker01 = '^GSPC'
    date_start = '2023-01-01'
    # date_start = '2020-08-01' #MEMO：Fear & Greed Indexを取得できる最も古いデータがこの日付です
    # date_start = (pd.datetime.today() - relativedelta(weeks= 1)).strftime('%Y-%m-%d') #1週間前
    # date_start = (pd.datetime.today() - relativedelta(years=1)).strftime('%Y-%m-%d')  #1年前
    date_end = pd.datetime.today().strftime('%Y-%m-%d')

    # データ取得----------------------------------------------------------------
    # S&P 500の株価データを取得
    df_day01 = yf.download(ticker01, start=date_start, end=date_end)
    
    # Fear & Greed Indexのデータ取得
    BASE_URL = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata/"
    END_DATE = pd.datetime.today().strftime('%Y-%m-%d')
    ua = UserAgent()

    headers = {
        'User-Agent': ua.random,
    }
    URL = BASE_URL + date_start
    r = requests.get(URL, headers=headers)
    data = r.json()
   
    # DataFrame型へ変換＋データ整備---------------------------------------------------
    df_day02 = pd.DataFrame()
    idx = 0
    for row in data['fear_and_greed_historical']['data']:
        idx += 1
        # row['x'] = datetime.fromtimestamp(row['x'] / 1000).strftime('%Y-%m-%d')
        # print(row)
        target_date = datetime.fromtimestamp(row['x'] / 1000)
        close_price: float = float(row['y'])
        rating: str = row['rating']
        df_day02 = df_day02.append({
            'target_dt': target_date,
            'Close': close_price,
            'rating': rating,
        }, ignore_index=True)

        
    # チャートを描画 ------------------------------------------------------------------
    plt.figure(figsize=(12, 6))
    ax1 = plt.subplot(1, 1, 1)

    strbuf = "Fear&Greadの説明" + "\n"
    strbuf += "extreme fear \t 0〜25" + "\n"
    strbuf += "fear \t\t 26〜45" + "\n"
    strbuf += "neutral \t 46〜55" + "\n"
    strbuf += "greed \t\t 56〜75" + "\n"
    strbuf += "extreme greed \t 76〜100" + "\n"
    print(strbuf)

    # 強欲指数の状態ごとに色付け
    # ax1.axvspan(300, 400, color="coral")
    bef_status = df_day02['rating'][0]
    bef_TARGET_DT = df_day02['target_dt'][0]
    bef_idx = 0
    # print(bef_status)
    for idx,sr in df_day02.iterrows():
        if not(bef_status == sr['rating']):

            # 判定処理
            if bef_status == "extreme greed":
                ax1.axvspan(bef_TARGET_DT, sr['target_dt'], color="limegreen")
            elif bef_status == "greed":
                ax1.axvspan(bef_TARGET_DT, sr['target_dt'], color="palegreen")
            elif bef_status == "neutral":
                pass
            elif bef_status == "fear":
                ax1.axvspan(bef_TARGET_DT, sr['target_dt'], color="lightsalmon")
            elif bef_status == "extreme fear":
                ax1.axvspan(bef_TARGET_DT, sr['target_dt'], color="tomato")
            else:
                pass

            # 切替情報をセット
            bef_status = sr['rating']
            bef_TARGET_DT = sr['target_dt']
            bef_idx = idx

    # S&P 500株価指数のチャート
    ax1.plot(df_day01.index, df_day01['Close'], label='S&P 500', color='black')
    ax1.set_xlabel('日付')
    ax1.set_ylabel('S&P 500株価', color='black')
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.grid(True)
    # plt.title('S&P 500株価指数')
    
    # # Fear&Gread Indexのチャート
    # ax2 = ax1.twinx()
    # ax2.plot(df_day02['target_dt'], df_day02['Close'], label='Fear&Gread', color='gray')
    # ax2.set_xlabel('日付')
    # ax2.set_ylabel('Fear&Gread', color='black')
    # ax2.tick_params(axis='y', labelcolor='black')
    # ax2.grid(True)
    
    plt.title('Fear&Gread Indexの期間とS&P 500株価指数の推移')
    
    # チャートを表示
    file_name = "20231112_04_S&P500株価指数とFear&Greed_Indexの比較.png"
    plt.savefig(file_name) #グラフを保存
    plt.show()

    print("/*--FINISH-----------------------------------------------------*/")
    