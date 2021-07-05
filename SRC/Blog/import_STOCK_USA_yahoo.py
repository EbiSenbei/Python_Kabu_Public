import pandas as pd
from pandas_datareader.nasdaq_trader import get_nasdaq_symbols
import datetime
import os
import fix_yahoo_finance as yf

# float型への変換チェック
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
    print("/*--米国株の株価取得プログラム*/")
    # 初期値の設定
    symbolCode: str = "0000"
    start = datetime.datetime(2010, 1, 1)  # 取得したい開始期間
    end = pd.datetime.today()  # 取得したい終了期間(システム日付)

    # 米国株の銘柄コード(ティッカーシンボル)一覧をナスダックより取得
    symbolsDf: pd.core.frame.DataFrame
    symbolsDf = get_nasdaq_symbols()              # 米国全銘柄を取得したい場合はこちら
    # symbolsDf = pd.DataFrame(index=["VTI","VOO"])   # 銘柄指定で取得したい場合はこちら
    # symbolsDf.to_csv('nasdaq_symbols.csv')    # 銘柄一覧をCSVファイルで出力

    # データ出力フォルダを作成
    new_path = "data"  # フォルダ名
    if not os.path.exists(new_path):  # ディレクトリがなかったら
        os.mkdir(new_path)  # 作成したいフォルダ名を作成
    outputDf: pd.core.frame.DataFrame
    outputDf = pd.DataFrame(columns=["銘柄","日付", "始値","高値", "安値", "終値", "終値調整", "売買高", "前日増減額", "前日増減率"])

    # 取得した銘柄コード一覧から、株価情報を取得する。
    for codeIdx in range(len(symbolsDf)):
        if codeIdx >= 0:
            # 対象の銘柄コードを設定。
            symbolCode = str(symbolsDf.index[codeIdx])

            # システム日付を取得
            sysDateTime: str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # 進捗
            strBuf: str = ""
            strBuf = strBuf + "   (" + str(codeIdx + 1) + "/" + str(len(symbolsDf)) + ") " + str(
                '{:.2f}'.format(((codeIdx + 1) * 100 / len(symbolsDf)))) + '%\t'
            strBuf = strBuf + "\t銘柄コード：" + str(symbolCode) + "\t日付：" + sysDateTime
            print(strBuf)

            # 日別株価を取得
            try:
                df = yf.download(symbolCode, start=start, end=end)
            except ValueError as err:
                continue
            except Exception as err:
                print("Error:" + str(err))
                break

            for i in range(len(df)):
                try:
                    # 初期化
                    if i == 0:
                        fltADJ_CLOSE_PRICE = 0

                    # 値を設定
                    strBRAND_CD = symbolCode
                    # 始値
                    if isfloat(str(df.loc[df.index[i], "Open"])):
                        fltOPEN_PRICE = float(df.loc[df.index[i], "Open"])
                    else:
                        fltOPEN_PRICE = 0.00
                    # 高値
                    if isfloat(str(df.loc[df.index[i], "High"])):
                        fltHIGH_PRICE = float(df.loc[df.index[i], "High"])
                    else:
                        fltHIGH_PRICE = 0.00
                    # 安値
                    if isfloat(str(df.loc[df.index[i], "Low"])):
                        fltLOW_PRICE = float(df.loc[df.index[i], "Low"])
                    else:
                        fltLOW_PRICE = 0.00
                    # 終値
                    if isfloat(str(df.loc[df.index[i], "Close"])):
                        fltCLOSE_PRICE = float(df.loc[df.index[i], "Close"])
                    else:
                        fltCLOSE_PRICE = 0.00
                    # 修正後終値
                    if isfloat(str(df.loc[df.index[i], "Adj Close"])):
                        fltADJ_CLOSE_PRICE_before = fltADJ_CLOSE_PRICE
                        fltADJ_CLOSE_PRICE = float(df.loc[df.index[i], "Adj Close"])
                    else:
                        fltADJ_CLOSE_PRICE = 0.00
                    # 売買高
                    if str(df.loc[df.index[i], "Volume"]).isnumeric():
                        fltVOLUME_SU = float(df.loc[df.index[i], "Volume"])
                    else:
                        fltVOLUME_SU = 0.00

                    # 前日差額（修正後終値 - 始値）
                    fltDIFF_PRICE = fltCLOSE_PRICE - fltADJ_CLOSE_PRICE_before

                    # 前日増減比率((修正後終値(当日) - 修正後終値(前日))＊100/修正後終値(前日))
                    if fltADJ_CLOSE_PRICE_before == 0:
                        fltDIFF_RATE = 0
                    else:
                        fltDIFF_RATE = round(
                            ((fltADJ_CLOSE_PRICE - fltADJ_CLOSE_PRICE_before) * 100 / fltADJ_CLOSE_PRICE_before), 4)

                    # 対象日付をセット
                    dateTARGET_DT = datetime.datetime.strptime(str(df.index[i]), '%Y-%m-%d 00:00:00')

                    # 取得した値をDataframeにセット
                    outputDf = outputDf.append({
                        '銘柄': strBRAND_CD
                        , '日付': dateTARGET_DT
                        , '始値': fltOPEN_PRICE
                        , '高値': fltHIGH_PRICE
                        , '安値': fltLOW_PRICE
                        , '終値': fltCLOSE_PRICE
                        , '終値調整': fltADJ_CLOSE_PRICE
                        , '売買高': fltVOLUME_SU
                        , '前日増減額': fltDIFF_PRICE
                        , '前日増減率': fltDIFF_RATE
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
            if len(outputDf) > 0:
                outputDf.to_csv("data/StockData_" + strBRAND_CD + ".csv",encoding="utf_8_sig")
                outputDf = outputDf.drop(outputDf.index[0:])

    print("/*--FINISH-----------------------------------------------------*/")
