import logger
import logging
import pandas as pd
import datetime as dt

_dt_dt_ = dt.datetime
_dt_td_ = dt.timedelta
_dt_d_  = dt.date
_dt_t_  = dt.time

from binance.client import Client

def get_client(api_key_file = '/home/yizhang/Research/api_key.csv'):
    api_key_info = pd.read_csv(api_key_file)
    api_key      = api_key_info.loc[0, 'value']
    api_secret   = api_key_info.loc[1, 'value']
    
    return Client(api_key, api_secret)

class QuoteHandler:

    def __init__(self, config, client):
        """ initializing quote handler class """
        self.p_bid       = 0
        self.p_ask       = 0
        self.q_bid       = 0
        self.q_ask       = 0
        self.p_mid       = 0
        self.p_bary      = 0
        self.p_bid_2     = 0
        self.p_ask_2     = 0
        self.q_bid_2     = 0
        self.q_ask_2     = 0
        self.p_bid_prev  = 0
        self.p_ask_prev  = 0
        self.q_bid_prev  = 0
        self.q_ask_prev  = 0
        self.p_mid_prev  = 0
        self.p_bary_prev = 0
        
        self.base_asset_position  = 0
        self.trade_asset_position = 0
        
        self.client      = client
        self.config      = config
        self.trade_asset = config['trade_asset']
        self.base_asset  = config['base_asset']
        self.symbol      = config['trade_asset'] + config['base_asset']
     
    def connect_to_market(self):
        """ connect to market and get market data update """

        while(True):
            try:
                self.on_quote_update(self.client.get_order_book(symbol=self.symbol))
            except:
                logger.warning("Bad market data update!!!")
       
    def on_quote_update(self, update):
        """ update class members on market data tick """

        # set prev values before update
        self.p_bid_prev  = self.p_bid 
        self.p_ask_prev  = self.p_ask 
        self.q_bid_prev  = self.q_bid 
        self.q_ask_prev  = self.q_ask 
        self.p_mid_prev  = self.p_mid 
        self.p_bary_prev = self.p_bary
        
        # set current value to the new update
        self.p_bid       = float(update['bids'][0][0])
        self.q_bid       = float(update['bids'][0][1])
        self.p_ask       = float(update['asks'][0][0])
        self.q_ask       = float(update['asks'][0][1])
        self.p_bid_2     = float(update['bids'][1][0])
        self.q_bid_2     = float(update['bids'][1][1])
        self.p_ask_2     = float(update['asks'][1][0])
        self.q_ask_2     = float(update['asks'][1][1])
        
        self.p_mid       = 0.5 * (self.p_bid + self.p_ask)
        self.p_bary      = (self.p_bid * self.q_ask + self.p_ask * self.q_bid) / (self.q_bid + self.q_ask)
        self.base_asset_position  = float(self.client.get_asset_balance(asset=self.base_asset)['free'])
        self.trade_asset_position = float(self.client.get_asset_balance(asset=self.trade_asset)['free'])
        
        logger.debug("bidSz=%f|bid=%f|ask=%f|askSz=%f|mid=%f|bary=%f|bap=%f|tap=%f" % (self.q_bid, self.p_bid, self.p_ask, self.q_ask, self.p_mid, self.p_bary, self.base_asset_position, self.trade_asset_position))

    def check_buy_or_sell(self):
        """ write your strategy here """
	
    def check_passive_buy(self):
        pass

    def check_passive_sell(self):
        pass

    def check_passive_cancel_buy(self):
        pass

    def check_passive_cancel_sell(self):
        pass
 
    def check_active_buy(self):
        pass

    def check_active_sell(self):
        pass



if __name__ == "__main__":
    config = {'log_dir': '/home/yizhang/Research/logs/', 'trade_asset': 'ETH', 'base_asset': 'BTC'}
    #import pdb; pdb.set_trace()
    logger = logger.get_logger(config['log_dir'], "CryptoDaddyStrategy", _dt_dt_.now().strftime("%Y%m%d"), logging.DEBUG)
    ETH = QuoteHandler(config, get_client())
    ETH.connect_to_market()
