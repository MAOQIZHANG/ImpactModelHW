import os
import sys
import unittest
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from impactUtils.TickTest import TickTest
from taq import MyDirectories
from taq.TAQTradesReader import TAQTradesReader

# Test of TickTest, a class used to classify
# trades as either buyer or seller initiated.
class Test_TickTest(unittest.TestCase):

    # Demonstrate how classification works
    def test_classify(self):
        tickTest = TickTest()
        self.assertTrue(tickTest.classify(100) == 0)
        self.assertTrue(tickTest.classify(100) == 0)
        self.assertTrue(tickTest.classify(101) == 1)
        self.assertTrue(tickTest.classify(101) == 1)
        self.assertTrue(tickTest.classify(102) == 1)
        self.assertTrue(tickTest.classify(101) == -1)
        self.assertTrue(tickTest.classify(101) == -1)
        self.assertTrue(tickTest.classify(102) == 1)

    # Classify an entire day of data and compare
    # to first 10 expected classifications
    def test_classifyAll(self):
        filePathName = MyDirectories.getTradesDir() + "/20070919/IBM_trades.binRT"
        data = TAQTradesReader(filePathName)
        tickTest = TickTest()
        startOfDay = 18 * 60 * 60 * 1000 / 2
        endOfDay = startOfDay + (13 * 60 * 60 * 1000 / 2)
        classifications = tickTest.classifyAll(data, startOfDay, endOfDay)
        # In the Expressions window, paste: list(map(lambda i: data.getPrice(i), range( 0, 10 )))
        # Each classification is a tuple containing timestamp, price, and classification
        self.assertEqual(
            '[(34216000, 116.9000015258789, 100, 0), (34216000, 116.9000015258789, 100, 0), (34216000, 116.94999694824219, 1000, 1), (34216000, 116.98999786376953, 500, 1), (34216000, 117.19000244140625, 400, 1), (34216000, 117.18000030517578, 100, -1), (34219000, 117.0199966430664, 100, -1), (34219000, 117.02999877929688, 200, 1), (34219000, 116.7699966430664, 100, -1), (34219000, 116.7699966430664, 100, -1)]',
            str(classifications[0:10])
        )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
