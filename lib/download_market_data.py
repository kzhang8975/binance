import time
import pandas as pd
import datetime as dt

from utils import save_fullbook_data

_dt_dt_ = dt.datetime
_dt_td_ = dt.timedelta
_dt_d_  = dt.date
_dt_t_  = dt.time

from binance.client import Client

def get_market_data(end_time, delay=1):
    client = Client(api_key, api_secret)
    fullbook = pd.DataFrame()
    
    ticker_list = [x['symbol'] for x in client.get_all_tickers()]
    
    while(_dt_dt_.now() < end_time):
        for symbol in ticker_list:
            try:
                depth   = pd.DataFrame(client.get_order_book(symbol=symbol))

                book_update = pd.DataFrame({_dt_dt_.now().strftime("%Y%m%d %H:%M:%S.%f"): {'symbol': symbol, 'q_bid': float(depth.loc[0, 'bids'][1]), 'p_bid': float(depth.loc[0, 'bids'][0]), 
                                           'q_ask': float(depth.loc[0, 'asks'][1]), 'p_ask': float(depth.loc[0, 'asks'][0]), 
                                           'q_bid_2': float(depth.loc[1, 'bids'][1]), 'p_bid_2': float(depth.loc[1, 'bids'][0]), 
                                           'q_ask_2': float(depth.loc[1, 'asks'][1]), 'p_ask_2': float(depth.loc[1, 'asks'][0])
                                           }})

                fullbook = fullbook.append(book_update.T)
            except:
                pass

        time.sleep(delay)

    save_fullbook_data(fullbook, '/home/yizhang/Research/data/%s' % (_dt_dt_.now().strftime("%Y/%m/%d/")))


if __name__ == "__main__":
    api_key_info = pd.read_csv('/home/yizhang/Research/api_key.csv')
    api_key      = api_key_info.loc[0, 'value']
    api_secret   = api_key_info.loc[1, 'value']
    
    get_market_data(end_time=_dt_dt_.combine(_dt_d_.today(), _dt_t_(23,50)))

