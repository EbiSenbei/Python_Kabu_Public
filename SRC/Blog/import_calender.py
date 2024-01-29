
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

import warnings

warnings.simplefilter('ignore')

if __name__ == '__main__':

    # /*-------------------------------------------------------------*/
    # ブラウザを開いて投稿用の画像を取得
    # SeleniumのChromeドライバーを初期化
    driver = webdriver.Chrome(executable_path=r"bin\chromedriver_win32\chromedriver.exe")

    try:
        # # 指定のURLにアクセス
        url = "https://mst.monex.co.jp/pc/servlet/ITS/report/EconomyIndexCalendar"  # 開きたいページのURLを指定してください
        driver.get(url)

        # # カレントウインドウを最大化する
        driver.maximize_window()

        # # ページが完全に読み込まれるのを待つ（必要に応じて時間を調整）
        time.sleep(10)

        # # #[★]をクリック（チェックを外す）
        # element = driver.find_element(by=By.XPATH, value='//*[@id="importance_1"]')
        # element.click()

        # #[絞り込み]をクリック
        element = driver.find_element(by=By.XPATH,
                                      value='//*[@id="gn_info-lm_economyIndexCal"]/div[7]/div/div[3]/div[1]/div[3]/a')
        element.click()

        # 経済指標カレンダーをキャプチャ - ----------------------------------------------------------
        # ## 経済指標カレンダーのデータを取得
        html_txt = driver.page_source

        # 国地域を置き換え
        bef_txt = '<img src="/pc/static/img/category/report/flag/inner_flag_jpn.gif"></td>'
        aft_txt = '日本</td>'
        html_txt = html_txt.replace(bef_txt, aft_txt)
        bef_txt = '<img src="/pc/static/img/category/report/flag/inner_flag_usa.gif"></td>'
        aft_txt = 'アメリカ</td>'
        html_txt = html_txt.replace(bef_txt, aft_txt)
        bef_txt = '<img src="/pc/static/img/category/report/flag/inner_flag_eur.gif"></td>'
        aft_txt = '欧州</td>'
        html_txt = html_txt.replace(bef_txt, aft_txt)

        # HTML情報を出力
        file_path = 'Economic_Calendar.html'
        f = open(file_path, 'w', encoding='UTF-8')
        f.write(html_txt)
        f.close()

        # ブラウザを閉じる
        driver.quit()

        # HTML情報をテーブル情報で読み込み
        data = pd.read_html(file_path, encoding="UTF-8")
        df = data[2].copy()

        print("データ件数：" + str(len(data[2])))

        data[2].to_excel('Economic_Calendar.xlsx')

    except Exception as e:
        print(e)

    # /*--FINISH----------------------------------------------------*/
