import os
import numpy as np
import pandas as pd
from tqdm import tqdm

import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from taq import MyDirectories
from taq.TAQTradesReader import TAQTradesReader
from taq.TAQQuotesReader import TAQQuotesReader
from impactUtils.FirstPriceBuckets import FirstPriceBuckets
from impactUtils.LastPriceBuckets import LastPriceBuckets
from impactUtils.MidQuoteReturnBuckets import MidQuoteReturnBuckets
from impactUtils.VWAP import VWAP
from impactUtils.ImbalanceValue import ImbalanceValue
from impactUtils.DailyVolume import DailyVolume


class MatrixCompute():

    def __init__(
            self, 
            startTS = 9.5 * 60**2 * 1000,
            endTS = 16 * 60**2 * 1000
        ):
        self.startTS = startTS
        self.endTS = endTS
        self.trades_dir = MyDirectories.getTradesDir()
        self.quotes_dir = MyDirectories.getQuotesDir()
        self.dates = os.listdir(self.trades_dir)
        for date in self.dates:
            if not date.startswith('20'):
                self.dates.remove(date)
        assert(len(self.dates) == 65)
        with open('data/stocks.js') as file:
            self.stocks = [line.rstrip() for line in file]

        self.trades_reader = TAQTradesReader
        self.quotes_reader = TAQQuotesReader
    

    def get_MidQuoteReturns(self, ):
        numBuckets = int((self.endTS - self.startTS) / (2.0 * 60 * 1000))
        return_matrix = np.array([], dtype=float).reshape(0, numBuckets * len(self.dates))

        for stock in tqdm(self.stocks):
            Returns = np.array([])
            for date in self.dates:
                file_path = os.path.join(self.quotes_dir, date, stock + '_quotes.binRQ')
                if not os.path.exists(file_path):
                    print(f"File {file_path} does not exist!")
                    continue
                data = self.quotes_reader(file_path)
                returnBuckets = MidQuoteReturnBuckets(
                    data,
                    numBuckets = numBuckets,
                    startTS = self.startTS,
                    endTS = self.endTS
                )
                return_d = np.array(returnBuckets.mid_returns, dtype=float)
                Returns = np.concatenate([Returns, return_d])
            return_matrix = np.vstack([return_matrix, Returns])

        print(f'Matrix shape: {return_matrix.shape}')
        df = pd.DataFrame(return_matrix, index=self.stocks)
        df.to_pickle(os.path.join(MyDirectories.getOutputDir(), '2MinMidQuoteReturns.pkl'))


    def get_VWAP(self, startTS = 9.5 * 60**2 * 1000, endTS = 16 * 60**2 * 1000):
        Vwaps = np.array([], dtype=float).reshape(0, len(self.dates))
        for stock in tqdm(self.stocks):
            prices = []
            for date in self.dates:
                file_path = os.path.join(self.trades_dir, date, stock + '_trades.binRT')
                if not os.path.exists(file_path):
                    print(f"File {file_path} does not exist!")
                    continue
                data = self.trades_reader(file_path)
                vwap = VWAP(
                    data, 
                    startTS = startTS, 
                    endTS = endTS
                )
                prices.append(vwap.getVWAP())
            prices = np.array(prices, dtype=float)
            Vwaps = np.vstack([Vwaps, prices])

        print(f'Matrix shape: {Vwaps.shape}')
        df = pd.DataFrame(Vwaps, index=self.stocks)
        df.to_pickle(os.path.join(MyDirectories.getOutputDir(), 'vwap_end_' + str(int(endTS)) + '.pkl'))
    

    def get_DailyVolume(self, startTS = 9.5 * 60**2 * 1000, endTS = 16 * 60**2 * 1000):
        Volume = np.array([], dtype=float).reshape(0, len(self.dates))
        for stock in tqdm(self.stocks):
            sizes = []
            for date in self.dates:
                file_path = os.path.join(self.trades_dir, date, stock + '_trades.binRT')
                if not os.path.exists(file_path):
                    print(f"File {file_path} does not exist!")
                    continue
                data = self.trades_reader(file_path)
                daily_volume = DailyVolume(
                    data, 
                    startTS = startTS, 
                    endTS = endTS
                )
                sizes.append(daily_volume.getVolume())
            sizes = np.array(sizes, dtype=float)
            Volume = np.vstack([Volume, sizes])

        print(f'Matrix shape: {Volume.shape}')
        df = pd.DataFrame(Volume, index=self.stocks)
        df.to_pickle(os.path.join(MyDirectories.getOutputDir(), 'daily_volume.pkl'))
    

    def get_DailyValue(self, startTS = 9.5 * 60**2 * 1000, endTS = 16 * 60**2 * 1000):
        Values = np.array([], dtype=float).reshape(0, len(self.dates))
        for stock in tqdm(self.stocks):
            prices = []
            for date in self.dates:
                file_path = os.path.join(self.trades_dir, date, stock + '_trades.binRT')
                if not os.path.exists(file_path):
                    print(f"File {file_path} does not exist!")
                    continue
                data = self.trades_reader(file_path)
                vwap = VWAP(
                    data, 
                    startTS = startTS, 
                    endTS = endTS
                )
                prices.append(vwap.getValue())
            prices = np.array(prices, dtype=float)
            Values = np.vstack([Values, prices])

        print(f'Matrix shape: {Values.shape}')
        df = pd.DataFrame(Values, index=self.stocks)
        df.to_pickle(os.path.join(MyDirectories.getOutputDir(), 'daily_values.pkl'))
    

    def get_StartEndPrice(self, startTS = 9.5 * 60**2 * 1000, endTS = 16 * 60**2 * 1000):
        startPrices = np.array([], dtype=float).reshape(0, len(self.dates))
        endPrices = np.array([], dtype=float).reshape(0, len(self.dates))

        for stock in tqdm(self.stocks):
            prices_0 = []
            prices_1 = []
            for date in self.dates:
                file_path = os.path.join(self.trades_dir, date, stock + '_trades.binRT')
                if not os.path.exists(file_path):
                    print(f"File {file_path} does not exist!")
                    continue

                data = self.trades_reader(file_path)
                fstPrices = FirstPriceBuckets(data, numBuckets=1, startTS=startTS, endTS=startTS + 60**2 * 1000)
                lastPrices = LastPriceBuckets(data, numBuckets=1, startTS=endTS - 60**2 * 1000, endTS=endTS)
                prices_0.append(fstPrices.getPrice(0))
                prices_1.append(lastPrices.getPrice(0))

            prices_0 = np.array(prices_0, dtype=float)
            prices_1 = np.array(prices_1, dtype=float)
            startPrices = np.vstack([startPrices, prices_0])
            endPrices = np.vstack([endPrices, prices_1])

        print(f'Matrix shape: {startPrices.shape}, {endPrices.shape}')
        df = pd.DataFrame(startPrices, index=self.stocks)
        df.to_pickle(os.path.join(MyDirectories.getOutputDir(), 'ArrivalPrice.pkl'))
        df = pd.DataFrame(endPrices, index=self.stocks)
        df.to_pickle(os.path.join(MyDirectories.getOutputDir(), 'TerminalPrice.pkl'))


    def get_ImbalanceValue(self, startTS = 9.5 * 60**2 * 1000, endTS = 15.5 * 60**2 * 1000):
        Values = np.array([], dtype=float).reshape(0, len(self.dates))
        for stock in tqdm(self.stocks):
            vals = []
            for date in self.dates:
                file_path = os.path.join(self.trades_dir, date, stock + '_trades.binRT')
                data = self.trades_reader(file_path)
                IV = ImbalanceValue(data, startTS=startTS, endTS=endTS)
                vals.append(IV.getImbalnceValue())
            Values = np.vstack([Values, np.array(vals, dtype=float)])
        print(f'Matrix shape: {Values.shape}')
        df = pd.DataFrame(Values, index=self.stocks)
        df.to_pickle(os.path.join(MyDirectories.getOutputDir(), 'value_imbalance.pkl'))


if __name__ == "__main__":
    M = MatrixCompute()
    # M.get_MidQuoteReturns()
    # M.get_VWAP(startTS = 9.5 * 60**2 * 1000, endTS = 15.5 * 60**2 * 1000)
    # M.get_VWAP(startTS = 9.5 * 60**2 * 1000, endTS = 16 * 60**2 * 1000)
    # M.get_StartEndPrice()
    # M.get_DailyValue()
    # M.get_ImbalanceValue()
    M.get_DailyVolume()
