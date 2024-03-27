# Class to calculate volume weighted average price for a given day of data between start timestamp and end timesamp, exclusive
class VWAP(object):
    def __init__(self, data, startTS, endTS):
        self.v = 0
        self.s = 0
        counter = 0

        for i in range(0, data.getN()):
            if data.getTimestamp(i) < startTS:
                continue
            if data.getTimestamp(i) >= endTS:
                break
            counter = counter + 1
            self.v += (data.getSize(i) * data.getPrice(i))
            self.s += data.getSize(i)

        if counter == 0:
            self._counter = 0
            self._vwap = None
        else:
            self._counter = counter
            self._vwap = self.v / self.s

    def getVWAP(self):
        return self._vwap
    
    def getValue(self):
        return self.v

    def getN(self):
        return self._counter
