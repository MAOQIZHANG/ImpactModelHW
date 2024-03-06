import unittest

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from taq import MyDirectories
from taq.TAQQuotesReader import TAQQuotesReader


class Test_TAQQuotesReader(unittest.TestCase):

    def test1(self):

        reader = TAQQuotesReader( MyDirectories.getQuotesDir() + '/20070920/IBM_quotes.binRQ' )
        
        zz = list([
            reader.getN(),
            reader.getSecsFromEpocToMidn(),
            reader.getMillisFromMidn( 0 ),
            reader.getAskSize( 0 ),
            reader.getAskPrice( 0 ),
            reader.getBidSize( 0 ),
            reader.getBidPrice( 0 )
        ])
        self.assertEqual( '[70166, 1190260800, 34210000, 1, 116.19999694824219, 38, 116.19999694824219]', str( zz ) )


if __name__ == "__main__":
    unittest.main()
