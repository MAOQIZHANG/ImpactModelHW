import os
import sys
import unittest
import inspect
import pandas as pd
import numpy as np

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from utils.impact_calculation import ImpactCalculation

class Test_Impact(unittest.TestCase):

    def test_vol(self):

        hTest = ImpactCalculation()
        hTest.compute_h()

        with open('Impact-Model-Matrix/2MinMidQuoteReturns.pkl', 'rb') as f:
            df = pd.read_pickle(f)

        self.assertEqual((502, 65), hTest.g.shape)
        self.assertEqual((502, 65), hTest.h.shape)
        self.assertEqual(-0.009999990463256836, hTest.g.loc['JAVA'][0])
        self.assertEqual(0.000626563322088991, hTest.h.loc['JAVA'][0])
        
        
if __name__ == "__main__":
    unittest.main()
