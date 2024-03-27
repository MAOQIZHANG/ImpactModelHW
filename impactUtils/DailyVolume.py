# Class to calculate volume (sum of all trade sizes) for a given day of data between start timestamp and end timesamp
class DailyVolume(object):
    def __init__(self, data, startTS, endTS):
        self.v = 0
        counter = 0

        for i in range(0, data.getN()):
            if data.getTimestamp(i) < startTS:
                continue
            if data.getTimestamp(i) >= endTS:
                break
            counter = counter + 1
            self.v += data.getSize(i)

        if counter == 0:
            self._counter = 0
        else:
            self._counter = counter
    
    def getVolume(self):
        return self.v

    def getN(self):
        return self._counter
