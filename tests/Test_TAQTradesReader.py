import unittest
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from taq import MyDirectories
from taq.TAQTradesReader import TAQTradesReader


class Test_TAQTradesReader(unittest.TestCase):

    def test1(self):

        reader = TAQTradesReader( MyDirectories.getTradesDir() + '/20070920/IBM_trades.binRT' )
        
        zz = list([
            reader.getN(),
            reader.getSecsFromEpocToMidn(),
            reader.getMillisFromMidn( 0 ),
            reader.getSize( 0 ),
            reader.getPrice( 0 )
        ])

        self.assertEqual(
            '[25367, 1190260800, 34210000, 76600, 116.2699966430664]',
            str( zz )
        )


if __name__ == "__main__":
    unittest.main()
