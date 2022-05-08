# 作成したCSVから指定通貨のチャートを作成

import pandas as pd
import matplotlib.pyplot as plt
import os

## ユーザー設定
TARGET_PATH = '..\\csv'
TARGET_FILE = 'closing_price_20220509.csv'
CURRENCY = 'BTC'

def main():
    df = pd.read_csv(os.path.join(TARGET_PATH, TARGET_FILE), parse_dates=['date'], index_col='date')
    
    plt.plot(df.index, df[CURRENCY])
    plt.xlabel('Date')
    plt.ylabel('Closing price [JPY]')
    plt.show()

if __name__ == '__main__':
    main()