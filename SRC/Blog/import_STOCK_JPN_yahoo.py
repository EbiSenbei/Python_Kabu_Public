import datetime
from dateutil.relativedelta import relativedelta
import yfinance as yf
import pandas as pd
import urllib.request
import pandas_datareader as web

from Common.common import Common
from Common.log import Log
from Dao import T_KBN_Dao, M_BRAND_Dao,M_BRAND_US_Dao, L_STOCK_DAY_Dao
from Entity import L_STOCK_DAY_Entity

FILE_NAME:str = "import_STOCK_JPN_yahoo"
log: Log = Log(FILE_NAME)
if __name__ == '__main__':
    # try:
    print("/*--START-----------------------------------------------------*/")

    # df: pd.core.frame.DataFrame
    # df = get_nasdaq_symbols()
    # df.to_csv('nasdaq_symbols.csv')
    # print(len(df))

    # ------------------------------------------------------------------
    # 各クラスのコンストラクタ(DB接続)を実行
    tKbnDao: T_KBN_Dao = T_KBN_Dao.T_KBN_Dao()
    mBrandDao: M_BRAND_Dao = M_BRAND_Dao.M_BRAND_Dao()
    mBrandUsDao: M_BRAND_US_Dao = M_BRAND_US_Dao.M_BRAND_US_Dao()
    lStockDayDao: L_STOCK_DAY_Dao = L_STOCK_DAY_Dao.L_STOCK_DAY_Dao()

    # 初期値の設定
    brandCode: str = "0000"
    start = pd.datetime.today() - relativedelta(months=1)   # 取得したい開始期間
    # start = "2020/01/01"  # 取得したい開始期間
    end = pd.datetime.today()  # 取得したい終了期間(システム日付)

    # 全銘柄情報取得
    # 銘柄データ(data_j.xls)を一覧表から取得
    inputDf: pd.core.frame.DataFrame
    # 日本取引所グループから、東証上場銘柄一覧をダウンロード
    url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    save_name = "data_j.xls"
    urllib.request.urlretrieve(url, save_name)

    inputDf: pd.core.frame.DataFrame
    inputDf = pd.read_excel('data_j.xls')

    # inputDf: pd.core.frame.DataFrame
    # inputDf = pd.DataFrame({"コード":["2558"]})
    df: pd.core.frame.DataFrame
    error_symbols = []

    for idx in range(len(inputDf)):
        if 0 <= idx :
            try:
                brandCode = str(inputDf.loc[idx, "コード"])
                # df = web.DataReader(inputDf.loc[idx, "BRAND_CD"], "yahoo", start.strftime("%Y/%m/%d"))
                df = yf.download(brandCode+'.T', start=start, end=end)
                # df = web.DataReader(brandCode+'.jp', data_source='stooq', start=start, end=end)
                # df = web.DataReader(brandCode + '.jp', data_source='stooq')
                df = df.sort_index(ascending=True)

            except Exception as e:
                log.error_print(e)

            # # CSV出力
            # df.to_csv(str(inputDf.loc[idx, "Symbol"]) + '.csv')

            # システム日付を取得
            sysDateTime: str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # 銘柄データを整形
            strBuf: str = ""
            strBuf = " \t (" + str(idx + 1) + "/" + str(len(inputDf)) + ") " + str('{:.2f}'.format(((idx + 1) * 100 / (len(inputDf))))) + '%'
            strBuf = strBuf + "\t銘柄コード：" + str(brandCode)
            strBuf = strBuf + " \t件数：" + str(len(df)) + "\t" + sysDateTime
            log.print(strBuf)

            for i in range(len(df)):
                try:
                    # 初期化
                    stockEn: L_STOCK_DAY_Entity = L_STOCK_DAY_Entity.L_STOCK_DAY_Entity()
                    # 値を設定
                    stockEn.strBRAND_CD = brandCode
                    # 始値
                    if Common.isfloat(str(df.loc[df.index[i], "Open"])):
                        stockEn.fltOPEN_PRICE = float(df.loc[df.index[i], "Open"])
                    else:
                        stockEn.fltOPEN_PRICE = 0.00
                    # 高値
                    if Common.isfloat(str(df.loc[df.index[i], "High"])):
                        stockEn.fltHIGH_PRICE = float(df.loc[df.index[i], "High"])
                    else:
                        stockEn.fltHIGH_PRICE = 0.00
                    # 安値
                    if Common.isfloat(str(df.loc[df.index[i], "Low"])):
                        stockEn.fltLOW_PRICE = float(df.loc[df.index[i], "Low"])
                    else:
                        stockEn.fltLOW_PRICE = 0.00
                    # 終値
                    if Common.isfloat(str(df.loc[df.index[i], "Close"])):
                        stockEn.fltCLOSE_PRICE = float(df.loc[df.index[i], "Close"])
                    else:
                        stockEn.fltCLOSE_PRICE = 0.00
                    # 修正後終値
                    if Common.isfloat(str(df.loc[df.index[i], "Adj Close"])):
                        stockEn.fltADJ_CLOSE_PRICE = float(df.loc[df.index[i], "Adj Close"])
                    else:
                        stockEn.fltADJ_CLOSE_PRICE = 0.00
                    # 売買高
                    if Common.isfloat(str(df.loc[df.index[i], "Volume"])):
                        stockEn.fltVOLUME_SU = float(df.loc[df.index[i], "Volume"])
                    else:
                        stockEn.fltVOLUME_SU = 0.00

                    # 前日差額（修正後終値 - 始値）
                    stockEn.fltDIFF_PRICE = stockEn.fltCLOSE_PRICE - stockEn.fltOPEN_PRICE

                    # 前日増減比率((修正後終値 - 始値)＊100/始値)
                    if stockEn.fltOPEN_PRICE == 0:
                        stockEn.fltDIFF_RATE = 0
                    else:
                        stockEn.fltDIFF_RATE = round(
                            ((stockEn.fltCLOSE_PRICE - stockEn.fltOPEN_PRICE) * 100 / stockEn.fltOPEN_PRICE), 4)

                    # 対象日付をセット（システム年＋取得月日）
                    stockEn.dateTARGET_DT = datetime.datetime.strptime(str(df.index[i]), '%Y-%m-%d 00:00:00')

                    # stockEn.print()
                    # 取得した値をDBに登録
                    lStockDayDao.pushL_STOCK_DAY(stockEn, sysDateTime)
                except KeyError:
                    pass
                except ValueError:
                    pass
                except Exception as e:
                    log.error_print(e)
                    break


    print("/*--FINISH-----------------------------------------------------*/")