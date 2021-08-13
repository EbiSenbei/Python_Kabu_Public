import pandas as pd
import datetime
import os
import urllib.request


def isfloat(obj: any):
    if not obj.isdecimal():
        try:
            float(obj)
            return True
        except ValueError:
            return False
    else:
        return True


if __name__ == '__main__':
    # try:
    print("/*--START-----------------------------------------------------*/")

    # 初期値の設定
    symbolCode: str = "0000"
    startYear = 2010  # 取得したい開始期間
    endYear = int(pd.datetime.today().strftime('%Y'))  # 取得したい終了期間(システム日付)

     # データ出力フォルダを作成
    new_path = "data"  # フォルダ名
    if not os.path.exists(new_path):  # ディレクトリがなかったら
        os.mkdir(new_path)  # 作成したいフォルダ名を作成
    outputDf: pd.core.frame.DataFrame

    outputDf: pd.core.frame.DataFrame
    outputDf = pd.DataFrame(columns=["銘柄", "日付", "始値", "高値", "安値", "終値", "終値調整", "売買高", "前日増減額", "前日増減率"])

    # 日本取引所グループから、東証上場銘柄一覧をダウンロード
    url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    save_name = "data/data_j.xls"
    urllib.request.urlretrieve(url, save_name)

    symbolsDf: pd.core.frame.DataFrame
    symbolsDf = pd.read_excel('data/data_j.xls')

    # 取得した銘柄コード一覧から、株価情報を取得する。
    for codeIdx in range(len(symbolsDf)):
        if codeIdx >= 0:
            # 対象の銘柄コードを設定。
            symbolCode = str(symbolsDf.loc[codeIdx, "コード"])

            # システム日付を取得
            sysDateTime: str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # 進捗
            strBuf: str = ""
            strBuf = strBuf + "   (" + str(codeIdx + 1) + "/" + str(len(symbolsDf)) + ") " + str(
                '{:.2f}'.format(((codeIdx + 1) * 100 / len(symbolsDf)))) + '%\t'
            strBuf = strBuf + "\t銘柄コード：" + str(symbolCode) + "\t日付：" + sysDateTime
            print(strBuf)

            # 指定期間の日別株価を取得
            for yearIdx in range(endYear - startYear):
                try:
                    strURL = 'https://kabuoji3.com/stock/' + str(symbolCode) + '/' + str(startYear + yearIdx) + '/'
                    df = pd.read_html(strURL)[0]
                except ValueError as err:
                    # print("ValueError:" + str(err))
                    continue
                except Exception as err:
                    print("Error:" + str(err))
                    break

                for i in range(len(df)):
                    try:
                        # # 初期化
                        fltADJ_CLOSE_PRICE = 0.00  # 終値調整
                        fltADJ_CLOSE_PRICE_before = 0.00  # 終値調整(前日)

                        # 値を設定
                        strBRAND_CD = symbolCode
                        # 始値
                        if isfloat(str(df.loc[df.index[i], "始値"])):
                            fltOPEN_PRICE = float(df.loc[df.index[i], "始値"])
                        else:
                            fltOPEN_PRICE = 0.00
                        # 高値
                        if isfloat(str(df.loc[df.index[i], "高値"])):
                            fltHIGH_PRICE = float(df.loc[df.index[i], "高値"])
                        else:
                            fltHIGH_PRICE = 0.00
                        # 安値
                        if isfloat(str(df.loc[df.index[i], "安値"])):
                            fltLOW_PRICE = float(df.loc[df.index[i], "安値"])
                        else:
                            fltLOW_PRICE = 0.00
                        # 終値
                        if isfloat(str(df.loc[df.index[i], "終値"])):
                            fltCLOSE_PRICE = float(df.loc[df.index[i], "終値"])
                        else:
                            fltCLOSE_PRICE = 0.00
                        # 修正後終値
                        if isfloat(str(df.loc[df.index[i], "終値調整"])):
                            fltADJ_CLOSE_PRICE_before = fltADJ_CLOSE_PRICE
                            fltADJ_CLOSE_PRICE = float(df.loc[df.index[i], "終値調整"])
                        else:
                            fltADJ_CLOSE_PRICE = 0.00
                        # 売買高
                        if str(df.loc[df.index[i], "出来高"]).isnumeric():
                            fltVOLUME_SU = float(df.loc[df.index[i], "出来高"])
                        else:
                            fltVOLUME_SU = 0.00

                        # 前日差額（修正後終値 - 始値）
                        fltDIFF_PRICE = fltCLOSE_PRICE - fltOPEN_PRICE

                        # 前日増減比率((修正後終値(当日) - 修正後終値(前日))＊100/修正後終値(前日))
                        if fltADJ_CLOSE_PRICE_before == 0:
                            fltDIFF_RATE = 0
                        else:
                            fltDIFF_RATE = round(
                                ((fltADJ_CLOSE_PRICE - fltADJ_CLOSE_PRICE_before) * 100 / fltADJ_CLOSE_PRICE_before), 4)

                        # 対象日付をセット
                        dateTARGET_DT = datetime.datetime.strptime(str(df.loc[df.index[i], "日付"]), '%Y-%m-%d')

                        # 取得した値をDataframeにセット
                        outputDf = outputDf.append({
                             '銘柄': strBRAND_CD
                            ,'日付': dateTARGET_DT
                            , '始値': fltOPEN_PRICE
                            , '高値': fltHIGH_PRICE
                            , '安値': fltLOW_PRICE
                            , '終値': fltCLOSE_PRICE
                            , '終値調整': fltADJ_CLOSE_PRICE
                            , '売買高': fltVOLUME_SU
                            , '前日増減額': fltDIFF_PRICE
                            , '前日増減率': fltDIFF_PRICE
                        }, ignore_index=True)

                    except KeyError as err:
                        print("KeyError:" + str(err))
                        pass
                    except ValueError as err:
                        print("ValueError:" + str(err))
                        pass
                    except Exception as err:
                        print("Error:" + str(err))
                        break

            # 取得した株価データをExcelデータに出力
            if "outputDf" in globals():
                outputDf.to_csv("data/StockData_"+strBRAND_CD+".csv")

    print("/*--FINISH-----------------------------------------------------*/")
