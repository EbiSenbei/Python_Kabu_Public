
import datetime
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.request

import warnings
warnings.simplefilter('ignore')

FOLDER_PATH = 'data'

if __name__ == '__main__':
    print("/*--START-----------------------------------------------------*/")

    # 全銘柄情報取得
    # 銘柄データ(data_j.xls)を一覧表から取得
    inputDf: pd.core.frame.DataFrame
    # 日本取引所グループから、東証上場銘柄一覧をダウンロード
    url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    save_name = "data_j.xls"
    urllib.request.urlretrieve(url, save_name)

    inputDf: pd.core.frame.DataFrame
    inputDf = pd.read_excel('data_j.xls')


    # フォルダの存在チェック(フォルダがなかったら作成する)
    if not os.path.exists(FOLDER_PATH):
        os.mkdir(FOLDER_PATH)

    outputDf = pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
    for idx,sr in inputDf.iterrows():

        # if idx > 20:
        #     break

        ticker_code = str(inputDf.loc[idx, "コード"])
        ticker_name = str(inputDf.loc[idx, "銘柄名"])

        # ブルームバーグより、企業の情報を取得する。-----------------------------------------------------------
        # https: // finance.yahoo.co.jp / quote / 8031.T
        url = "https://www.bloomberg.co.jp/quote/" + ticker_code + ":JP"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # システム日付を取得
        sysDateTime: str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        #進捗確認
        strBuf: str = ""
        strBuf = " \t (" + str(idx + 1) + "/" + str(len(inputDf)) + ") " + str(
            '{:.2f}'.format(((idx + 1) * 100 / (len(inputDf))))) + '%'
        strBuf = strBuf + "\t銘柄コード：" + str(ticker_code) + "\t銘柄名：" + str(ticker_name)
        strBuf = strBuf + "\t" + sysDateTime
        print(strBuf)

        # 更新日時(対象日付)
        try:

            elem_biz_txt = soup.find_all('div', attrs={'class': 'profile__description'})[0].text
            elem_biz_txt = elem_biz_txt.replace("　","") #全角の空白を除去
            if idx in range(10):
                elem_biz_txt = elem_biz_txt.replace("  ", "")#半角の空白2連続を除去
            # print(elem_biz_txt)

            # 取得した値をDataframeにセット
            outputDf = outputDf.append({
                '銘柄': ticker_code
                , '銘柄名': ticker_name
                , '銘柄説明': elem_biz_txt
            }, ignore_index=True)

        except Exception as e:
            print(e)
            continue

    # 取得した株価データをExcelデータに出力
    if len(outputDf) > 0:
        outputDf.to_excel("data/tickerList"+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+".xlsx")

    print("/*--FINISH-----------------------------------------------------*/")