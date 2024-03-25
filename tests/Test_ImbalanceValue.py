import sys
import os
import unittest
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from taq.TAQTradesReader import TAQTradesReader
from taq import MyDirectories
from impactUtils.ImbalanceValue import ImbalanceValue

# Test ReturnBuckets class used to compute
# returns of some length of time, e.g. 2 minutes
# or 15 minutes
class Test_ImbalanceValue(unittest.TestCase):

    def test1(self):
        filePathName = MyDirectories.getTradesDir() + "/20070919/IBM_trades.binRT"
        data = TAQTradesReader(filePathName)
        iv = ImbalanceValue(data)
        tolerance = 0.0001
        self.assertAlmostEqual(-388366, iv.getImbalanceSize(), 0)
        self.assertAlmostEqual(-45224126.4439625, iv.getImbalnceValue(), places=6)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
