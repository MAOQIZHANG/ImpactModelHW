from taq.TAQQuotesReader import TAQQuotesReader
from taq import MyDirectories


class MidQuoteReturnBuckets():
    def __init__(
            self,
            data: TAQQuotesReader,
            numBuckets,
            startTS = 9.5 * 60 * 60 * 1000,  # eg 930AM = 19 * 60 * 60 * 1000 / 2
            endTS = 16 * 60 * 60 * 1000  # eg. 4PM = 16 * 60 * 60 * 10000
    ):
        bucketLen = (endTS - startTS) / numBuckets
        self.start_ts = [None] * numBuckets
        self.end_ts = [None] * numBuckets
        self.start_mid_prices = [None] * numBuckets
        self.end_mid_prices = [None] * numBuckets
        self.mid_returns = [None] * numBuckets

        print(data.getN(), numBuckets, bucketLen)

        iBucket = -1
        for i in range(data.getN()):
            ts = data.getMillisFromMidn(i)
            if ts >= endTS:
                break
            if ts < startTS:
                continue

            newBucket = int((ts - startTS) / bucketLen)
            self.end_ts[newBucket] = ts
            self.end_mid_prices[newBucket] = 0.5 * (data.getAskPrice(i) + data.getBidPrice(i))

            if iBucket != newBucket:
                # new bucket
                self.start_ts[newBucket] = ts
                self.start_mid_prices[newBucket] = 0.5 * (data.getAskPrice(i) + data.getBidPrice(i))
                iBucket = newBucket
        
        # mid-quote returns
        for i in range(numBuckets):
            if self.end_mid_prices[i] is None or self.start_mid_prices[i] is None:
                continue
            self.mid_returns[i] = (self.end_mid_prices[i] / self.start_mid_prices[i]) - 1.0


    def getMidReturn(self, index):
        return self.mid_returns[index]

    def getStartTimestamp(self, index):
        return self.start_ts[index]

    def getEndTimestamp(self, index):
        return self.end_ts[index]

    def getN(self):
        return len(self.mid_returns)

