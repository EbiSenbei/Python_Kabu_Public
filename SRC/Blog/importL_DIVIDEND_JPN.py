import datetime
import os

from pandas_datareader.nasdaq_trader import get_nasdaq_symbols
import pandas as pd
from dateutil.relativedelta import relativedelta
import urllib.request

import yfinance as yf

if __name__ == '__main__':

    print("/*--START-----------------------------------------------------*/")
    try:

        # 初期値の設定
        brandCode: str = ""
        start = pd.datetime.today() - relativedelta(years=20)  # 取得したい開始期間
        # start = datetime.datetime(2000, 1, 1)  # 取得したい開始期間
        end = pd.datetime.today()  # 取得したい終了期間(システム日付)

        print('# 対象期間')
        print("\t start = " + start.strftime('%Y-%m-%d %H:%M:%S'))
        print("\t end   = " + end.strftime('%Y-%m-%d %H:%M:%S'))

        # 全銘柄情報取得
        # 銘柄データ(data_j.xls)を一覧表から取得
        inputDf: pd.core.frame.DataFrame
        # 日本取引所グループから、東証上場銘柄一覧をダウンロード
        url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
        save_name = "data_j.xls"
        urllib.request.urlretrieve(url, save_name)

        symbolsDf: pd.core.frame.DataFrame
        symbolsDf = pd.read_excel('data_j.xls')

        # データ出力フォルダを作成
        new_path = "data"  # フォルダ名
        if not os.path.exists(new_path):  # ディレクトリがなかったら
            os.mkdir(new_path)  # 作成したいフォルダ名を作成

        print('# 対象の銘柄画面を検索・表示')

        strBrandCode:str = ""
        strBrandName:str = ""
        for idx in range(len(symbolsDf)):
            if 0 <= idx :
                try:
                    # システム日付を取得
                    sysDateTime: str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # 銘柄コードを取得
                    strBrandCode = str(symbolsDf.loc[idx, "コード"])+".T"

                    # 進捗
                    strBuf: str = ""
                    strBuf = " \t (" + str(idx + 1) + "/" + str(len(symbolsDf)) + ") " + str(
                        '{:.2f}'.format(((idx + 1) * 100 / (len(symbolsDf))))) + '%'
                    strBuf = strBuf + " \t銘柄コード：" + strBrandCode + "\t銘柄名：" + strBrandName + '\t' + sysDateTime
                    print(strBuf)

                    # 配当情報を取得
                    # print(strBrandCode)
                    t = yf.Ticker(strBrandCode)
                    # if not(start == "") and not(end == ""):
                    df = t.history(start=start, end=end, interval="1d")

                    # 取得件数0件の場合は、次の銘柄に移動
                    if len(df) == 0:
                        continue
                    else:
                        df = df.query("not(Dividends == 0.00)")
                        if len(df) == 0:
                            continue
                        else:
                            ## 項目を日本語に再設定とExcel出力
                            df_jp = df.copy()
                            strBrandCode = strBrandCode.replace(".T","")
                            df_jp["code"] = strBrandCode
                            df_jp = df_jp.drop('Stock Splits', axis=1)

                            # 項目の並べ替え
                            df_jp = df_jp.reindex(
                                columns=['code', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends'])

                            # 項目名を日本語に再設定
                            df_jp = df_jp.rename(columns={'Open': '始値', 'High': '高値', 'Low': '安値', 'Close': '終値'})
                            df_jp = df_jp.rename(
                                columns={'Date': '日付','code': 'コード', 'Volume': '出来高', 'Dividends': '配当額'})

                            # 配当金データがあった場合はデータ加工してExcel出力する
                            df_jp.to_excel("data\\DividendData_" + strBrandCode + "_" + datetime.datetime.now().strftime("%Y%m%d") + ".xlsx")
                            pass

                except Exception as e:
                    print(text = "idx=" + str(idx) + " brandCode=" + strBrandCode+ "Error:" + str(e).split('\n')[0]+ '\t' + sysDateTime)
                    pass

    except Exception as e:
        print("Error:" + str(e))
    finally:
        pass
    print("/*--FINISH-----------------------------------------------------*/")
    exit()

