import os
import sys
import unittest
import inspect
import pandas as pd
import numpy as np

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from utils.vol_filter import VolatilityFilter

class Test_Volatility(unittest.TestCase):

    def test_vol(self):

        volTest = VolatilityFilter(65, 10)
        volTest.compute_volatility(False)
        volTest.filter_high_vol(False)

        with open('Impact-Model-Matrix/2MinMidQuoteReturns.pkl', 'rb') as f:
            df = pd.read_pickle(f)

        self.assertEqual((502, 65), volTest.volatility_df.shape)
        self.assertEqual(df.iloc[0][0:1950].std()*np.sqrt(1950), volTest.volatility_df.iloc[0][1])
        self.assertEqual(df.iloc[1][195:2145].std()*np.sqrt(1950), volTest.volatility_df.iloc[1][2])

        # test filter
        self.assertEqual(10, (volTest.volatility_df.iloc[4] > volTest.volatility_threshold).sum())

        
if __name__ == "__main__":
    unittest.main()
