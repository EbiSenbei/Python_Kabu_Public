import pandas as pd
from pandas_datareader.nasdaq_trader import get_nasdaq_symbols

import datetime

# from Common.common import Common
# from Dao import T_KBN_Dao
# from Dao import M_BRAND_Dao
# from Entity import L_STOCK_DAY_Entity
# from Dao import L_STOCK_DAY_Dao



if __name__ == '__main__':
    # try:
    print("/*--START-----------------------------------------------------*/")

    # 初期値の設定
    symbolCode: str = "0000"
    startYear = 2010    # 取得したい開始期間
    endYear = int(pd.datetime.today().strftime('%Y'))   # 取得したい終了期間(システム日付)

    # 米国株の銘柄コード(ティッカーシンボル)一覧をナスダックより取得
    symbolsDf: pd.core.frame.DataFrame
    symbolsDf = get_nasdaq_symbols()
    # symbolsDf.to_csv('nasdaq_symbols.csv')    # 銘柄一覧をCSVファイルで出力

    # 取得した銘柄コード一覧から、株価情報を取得する。
    for codeIdx in range(len(symbolsDf)):
        if codeIdx >= 0:
            # 対象の銘柄コードを設定。
            symbolCode = str(symbolsDf.index[codeIdx])

            # システム日付を取得
            sysDateTime: str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # 進捗
            strBuf: str = ""
            strBuf = strBuf + "   (" + str(codeIdx+1) + "/" + str(len(symbolsDf)) + ") " + str('{:.2f}'.format(((codeIdx+1) * 100 / len(symbolsDf)))) + '%\t'
            strBuf = strBuf + "\t銘柄コード：" + str(symbolCode) + "\t日付：" + sysDateTime
            print(strBuf)

            # 指定期間の日別株価を取得
            for yearIdx in range(endYear - startYear):    
                try:
                    strURL = 'https://kabuoji3.com/stock/' + str(symbolCode) + '/' + str(startYear + yearIdx) + '/'
                    df = pd.read_html(strURL)[0]
                except ValueError as err:
                    print("ValueError:" + str(err))
                    continue

                # 銘柄データを整形
                strBuf: str = ""
                strBuf = " \t (" + str(yearIdx) + "/" + str(endYear - startYear) + ") " + str('{:.2f}'.format((yearIdx * 100 / (endYear - startYear)))) + '%'
                strBuf = strBuf + " \t件数：" + str(len(df))
                print(strBuf)

                for i in range(len(df)):
                    try:
                        # 初期化
                        stockEn: L_STOCK_DAY_Entity = L_STOCK_DAY_Entity.L_STOCK_DAY_Entity()
                        # 値を設定
                        stockEn.strBRAND_CD = symbolCode
                        # 始値
                        if Common.isfloat(str(df.loc[df.index[i], "始値"])):
                            stockEn.fltOPEN_PRICE = float(df.loc[df.index[i], "始値"])
                        else:
                            stockEn.fltOPEN_PRICE = 0.00
                        # 高値
                        if Common.isfloat(str(df.loc[df.index[i], "高値"])):
                            stockEn.fltHIGH_PRICE = float(df.loc[df.index[i], "高値"])
                        else:
                            stockEn.fltHIGH_PRICE = 0.00
                        # 安値
                        if Common.isfloat(str(df.loc[df.index[i], "安値"])):
                            stockEn.fltLOW_PRICE = float(df.loc[df.index[i], "安値"])
                        else:
                            stockEn.fltLOW_PRICE = 0.00
                        # 終値
                        if Common.isfloat(str(df.loc[df.index[i], "終値"])):
                            stockEn.fltCLOSE_PRICE = float(df.loc[df.index[i], "終値"])
                        else:
                            stockEn.fltCLOSE_PRICE = 0.00
                        # 修正後終値
                        if Common.isfloat(str(df.loc[df.index[i], "終値調整"])):
                            stockEn.fltADJ_CLOSE_PRICE = float(df.loc[df.index[i], "終値調整"])
                        else:
                            stockEn.fltADJ_CLOSE_PRICE = 0.00
                        # 売買高
                        if str(df.loc[df.index[i], "出来高"]).isnumeric():
                            stockEn.fltVOLUME_SU = float(df.loc[df.index[i], "出来高"])
                        else:
                            stockEn.fltVOLUME_SU = 0.00

                        # 前日差額（修正後終値 - 始値）
                        stockEn.fltDIFF_PRICE = stockEn.fltCLOSE_PRICE - stockEn.fltOPEN_PRICE

                        # 前日増減比率((修正後終値 - 始値)＊100/始値)
                        if stockEn.fltOPEN_PRICE == 0:
                            stockEn.fltDIFF_RATE = 0
                        else:
                            stockEn.fltDIFF_RATE = round(((stockEn.fltCLOSE_PRICE - stockEn.fltOPEN_PRICE) * 100 / stockEn.fltOPEN_PRICE),4)

                        # 対象日付をセット（システム年＋取得月日）
                        stockEn.dateTARGET_DT = datetime.datetime.strptime(str(df.loc[df.index[i], "日付"]), '%Y-%m-%d')

                        # stockEn.print()
                        # 取得した値をDBに登録
                        lStockDayDao.pushL_STOCK_DAY(stockEn, sysDateTime)
                    except KeyError as err:
                        print("KeyError:" + str(err))
                        pass
                    except ValueError as err:
                        print("ValueError:" + str(err))
                        pass
                    except Exception as err:
                        print("Error:" + str(err))
                        break
            # except Exception as e:
            #     print("Error:" + str(e))

    print("/*--FINISH-----------------------------------------------------*/")
