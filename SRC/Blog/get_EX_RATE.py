
# ▼参考サイト
# https://support.yahoo-net.jp/PccFinance/s/article/H000006607
# https://note.nkmk.me/python-pandas-dataframe-rename/

from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

import yfinance as yf
import sys

import warnings

warnings.simplefilter('ignore')
sys.path.append('../')

# 抽出対象を設定
## 通貨を指定
brandCode = "USDJPY=X" #ドル/日本円
# brandCode = "CNYJPY=X"　#中国元/日本円
# brandCode = "CNYUSD=X"　#中国元/ドル

## 抽出期間を指定
start_date = (pd.datetime.today() - relativedelta(months=6)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')
print(start_date)
print(end_date)

# Yahooファイナンスより通貨情報を取得（抽出期間指定あり）
df = yf.download(tickers=brandCode,
                 start=start_date,
                 end=end_date)

# Yahooファイナンスより通貨情報を取得（抽出期間指定なしの場合、1996年ころから取得）
# df = yf.download(tickers=brandCode)

df['code'] = brandCode
# df.head()

# 前日増減額と前日増減比を算出
# データフレームに前日増減額と前日増減比の枠を追加
df['diff_close'] = 0.00
df['diff_close_rate'] = 0.00

# 値の宣言と初期値をセット
close_price_before: float = 0
diff_close_price: float = 0
diff_close_rate: float = 0
count: int = 0
for idx, row in df.iterrows():
    count = count + 1

    # データの端数を丸める
    df.at[idx, 'Open'] = round(row['Open'], 3)
    df.at[idx, 'High'] = round(row['High'], 3)
    df.at[idx, 'Low'] = round(row['Low'], 3)
    df.at[idx, 'Close'] = round(row['Close'], 3)

    # 前日増減額と前日増減比を算出
    if count == 1:
        df.at[idx, 'diff_close'] = 0.00
        df.at[idx, 'diff_close_rate'] = 0.00
    else:
        df.at[idx, 'diff_close'] = round(row['Close'] - close_price_before, 3)
        df.at[idx, 'diff_close_rate'] = round((row['Close'] - close_price_before) * 100 / close_price_before, 3)

    # 前日の値をセット
    close_price_before = row['Close']
# df.tail()

## 項目を日本語に再設定とExcel出力
df_jp = df.copy()

# 項目の並べ替え
df_jp = df_jp.reindex(columns=['code', 'Open', 'High', 'Low', 'Close', 'diff_close', 'diff_close_rate'])
# 項目名を日本語に再設定
df_jp = df_jp.rename(columns={'Open': '始値', 'High': '高値', 'Low': '安値', 'Close': '終値'})
df_jp = df_jp.rename(columns={'code': 'コード', 'diff_close': '前日増減額', 'diff_close_rate': '前日増減比'})
# df_jp.tail()

filename = df_jp.at[df_jp.index[0], 'コード'].replace('=X', '') + "_" + datetime.now().strftime("%Y%m%d") + ".xlsx"
df_jp.to_excel(filename)



