import unittest
from taq import MyDirectories
from taq.TAQQuotesReader import TAQQuotesReader
from impactUtils.MidQuoteReturnBuckets import MidQuoteReturnBuckets


class Test_ReturnBuckets(unittest.TestCase):

    def testName(self):
        startTS = 18 * 60 * 60 * 1000 / 2  # 930AM
        endTS = 16 * 60 * 60 * 1000  # 4PM

        data = TAQQuotesReader( MyDirectories.getQuotesDir() + '/20070920/IBM_quotes.binRQ' )

        numBuckets = 10
        returnBuckets = MidQuoteReturnBuckets(data, numBuckets, startTS, endTS)

        self.assertTrue(returnBuckets.getN() == numBuckets)
        self.assertEqual(returnBuckets.start_mid_prices[0], 0.5 * (data.getAskPrice(0) + data.getBidPrice(0)))
        self.assertEqual(returnBuckets.end_mid_prices[0], 116.89500045776367)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
