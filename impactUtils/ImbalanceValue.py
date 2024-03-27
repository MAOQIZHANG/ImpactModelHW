from taq.TAQTradesReader import TAQTradesReader
from impactUtils.TickTest import TickTest
from impactUtils.VWAP import VWAP


class ImbalanceValue():
    def __init__(
            self, 
            data: TAQTradesReader, 
            startTS = 9.5 * 60 * 60 * 1000, 
            endTS = 15.5 * 60 * 60 * 1000
    ):
        self.tick_test = TickTest()
        self.classifications = self.tick_test.classifyAll(data, startTS, endTS)
        self.vwap = VWAP(data, startTS, endTS)

        self.imbalance_size = 0
        for i in range(len(self.classifications)):
            ts, price, size, side = self.classifications[i]
            self.imbalance_size += side * size
    
    def getImbalanceSize(self):
        return self.imbalance_size

    def getImbalnceValue(self):
        if self.vwap.getVWAP() is None:
            return None
        else:
            return self.imbalance_size * self.vwap.getVWAP()

