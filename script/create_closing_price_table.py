# coincheckの取扱い仮想通貨の終値一覧ページからヒストリカルデータを一日単位で取得

import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import time
from datetime import datetime

import pandas as pd
import os

## ユーザー設定
OUTPUT_PATH = '..\\csv'
TARGET_URL = 'https://coincheck.com/ja/exchange/closing_prices'

def main():
    driver = webdriver.Chrome()
    driver.get(TARGET_URL)

    # 待機時間の設定
    driver.implicitly_wait(10)

    # select要素の取得
    year_select = Select(driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div[1]/div/div[1]/div[1]/select[1]')) 
    month_select = Select(driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div[1]/div/div[1]/div[1]/select[2]')) 

    closing_price_df_list = []
    for year_i in range(len(year_select.options)):
        for month_i in range(len(month_select.options)):
            # select要素を選択   
            year_select.select_by_index(year_i)
            year_str = year_select.options[year_i].text
            month_select.select_by_index(month_i)
            month_str = month_select.options[month_i].text
            print(year_str + '/' + month_str)
            time.sleep(2)

            # bs4によるテーブルの取得
            html = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')

            # 通貨一覧取得
            column_list = [col.text for col in soup.find('thead').find_all('th')]
            column_list[0] = 'date' # 最初に空欄があるためそこをdateのカラムにする

            # 価格取得
            table_row_list = soup.find('tbody').find_all('tr')
            
            # DF作成
            for row in table_row_list:
                date_str = year_str+ '/' + row.find('th').text
                value_list = [date_str] + [(float(val.text.replace(',', '')) if val.text != '' else None) for val in row.find_all('td')]

                closing_price_df_list.append(pd.DataFrame(dict(zip(column_list, value_list)), index=['i',]))

    # DFにまとめる
    closing_price_df = pd.concat(closing_price_df_list)
    closing_price_df = closing_price_df.reset_index()
    closing_price_df = closing_price_df.drop('index', axis=1)

    # 出力
    output_file_name = 'closing_price_' + datetime.now().strftime('%Y%m%d') + '.csv'
    closing_price_df.to_csv(os.path.join(OUTPUT_PATH, output_file_name), index=False)

    print('終了')

    driver.close()

if __name__ == '__main__':
    main()