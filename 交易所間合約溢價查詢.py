#使用python 3.10.9
#作者:0xCatduck
#https://twitter.com/0xCatduck
#作者還超菜，真正的工程師看代碼應該會受不了，但能動就好
#這是簡單查詢Binance、Bybit、Bitget、BingX任意兩交易所合約溢價指數的程式
#這是沒錢買Tradingview的窮鬼寫的簡單程式，用於套利時建倉平倉參考用
#這邊用最新成交價所以會比TV的指數價格快一點，但準確度要同時考量交易所訂單簿的深度

import ccxt
import matplotlib.pyplot as plt

# 查詢交易所最新成交價
def binance_last_price(symbol):
    binance = ccxt.binance({
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future',
        },
    })

    binance_symbol = symbol

    binance_ticker = binance.fapipublic_get_ticker_price({'symbol': binance_symbol})
    binance_latest_price = binance_ticker['price']
    return binance_latest_price

def bybit_last_price(symbol):
    bybit = ccxt.bybit({
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future',
        },
    })

    bybit_symbol = symbol

    bybit_ticker = bybit.public_get_v2_public_tickers({'symbol': bybit_symbol})
    bybit_latest_price = bybit_ticker['result'][0]['last_price']
    return bybit_latest_price

def bitget_last_price(symbol):
    bitget = ccxt.bitget({
        'enableRateLimit': True,
    })

    bitget_symbol = f'{symbol}_UMCBL'

    bitget_ticker = bitget.publicMixGetMarketTicker({'symbol': bitget_symbol})
    bitget_latest_price = bitget_ticker['data']['last']
    return bitget_latest_price

def bingx_last_price(symbol):
    bingx = ccxt.bingx({
        'enableRateLimit': True,
        'options': {
            'defaultType': 'futures',
        },
    })

    bingx_symbol = symbol[0:-4] + '-' + symbol[-4:]

    bingx_ticker = bingx.swap_v2_public_get_quote_price({'symbol': bingx_symbol})
    bingx_latest_price = bingx_ticker['data']['price']
    return bingx_latest_price

# 讓使用者選擇要查詢的交易所與交易對
while True:

    #輸入第一間查詢的交易所
    exchange1 = input('第一間(分子)比對交易所 (BINANCE, BYBIT, BITGET, BINGX): ').upper()

    # 檢查使用者輸入的交易所是否有效
    if exchange1 not in ['BINANCE', 'BYBIT', 'BITGET', 'BINGX']:
        print('只有上述四間，再多要加錢')
        continue
    
    while True:

        #輸入第二間查詢的交易所
        exchange2 = input('第二間(分母)比對交易所 (BINANCE, BYBIT, BITGET, BINGX): ').upper()

        # 檢查使用者輸入的交易所是否有效
        if exchange2 not in ['BINANCE', 'BYBIT', 'BITGET', 'BINGX']:
            print('只有上述四間，再多要加錢')
            continue

        while True:
            
            #輸入查詢交易對
            symbol = input('輸入交易對 (e.g. BTCUSDT): ').upper()
            
            #檢查交易所是否有此交易對
            if exchange1 == 'BINANCE':
                try:
                    binance_last_price(symbol)
                except Exception as e:
                    print(f'{exchange1}無此交易對')
                    continue

            elif exchange1 == 'BYBIT':
                try:
                    bybit_last_price(symbol)
                except Exception as e:
                    print(f'{exchange1}無此交易對')
                    continue

            elif exchange1 == 'BITGET':
                try:
                    bitget_last_price(symbol)
                except Exception as e:
                    print(f'{exchange1}無此交易對')
                    continue

            elif exchange1 == 'BINGX':
                try:
                    bingx_last_price(symbol)
                except Exception as e:
                    print(f'{exchange1}無此交易對')
                    continue

            if exchange2 == 'BINANCE':
                try:
                    binance_last_price(symbol)
                except Exception as e:
                    print(f'{exchange2}無此交易對')
                    continue

            elif exchange2 == 'BYBIT':
                try:
                    bybit_last_price(symbol)
                except Exception as e:
                    print(f'{exchange2}無此交易對')
                    continue

            elif exchange2 == 'BITGET':
                try:
                    bitget_last_price(symbol)
                except Exception as e:
                    print(f'{exchange2}無此交易對')
                    continue
            
            elif exchange2 == 'BINGX':
                try:
                    bingx_last_price(symbol)
                except Exception as e:
                    print(f'{exchange2}無此交易對')
                    continue

            break
        break
    break

ratio_list = []

while True:
    if exchange1 == 'BINANCE':
        price1 = binance_last_price(symbol)
    elif exchange1 == 'BYBIT':
        price1 = bybit_last_price(symbol)
    elif exchange1 == 'BITGET':
        price1 = bitget_last_price(symbol)
    elif exchange1 == 'BINGX':
        price1 = bingx_last_price(symbol)

    if exchange2 == 'BINANCE':
        price2 = binance_last_price(symbol)
    elif exchange2 == 'BYBIT':
        price2 = bybit_last_price(symbol)
    elif exchange2 == 'BITGET':
        price2 = bitget_last_price(symbol)
    elif exchange2 == 'BINGX':
        price2 = bingx_last_price(symbol)

    ratio = float(price1) / float(price2) * 100
    ratio_list.append(ratio)

    print(f'{exchange1}/{exchange2} 的{symbol}合約溢價指數為 {"%.4f%%" % ratio}')

    plt.clf()
    plt.plot(ratio_list[-30:], color='lightgreen')
    plt.title(f'{exchange1}/{exchange2} {symbol} Premium Index')
    plt.xlabel('Time')
    plt.ylabel('Ratio')
    plt.axhline(y=100, color='r', linestyle='--')
    plt.grid(color='lightgray', linestyle='--')
    plt.show(block=False)
    plt.pause(0.01)