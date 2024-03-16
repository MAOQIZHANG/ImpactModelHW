import os
import numpy as np
import pandas as pd
from tqdm import tqdm

from taq import MyDirectories
from taq.TAQTradesReader import TAQTradesReader
from taq.TAQQuotesReader import TAQQuotesReader
from impactUtils.MidQuoteReturnBuckets import MidQuoteReturnBuckets


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
        assert(len(self.dates) == 65)

        with open('../data/stocks.js') as file:
            self.stocks = [line.rstrip() for line in file]

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



if __name__ == "__main__":
    M = MatrixCompute()
    M.get_MidQuoteReturns()
