import pandas as pd
import os

class ImpactCalculation():

    def __init__(
            self, 
        ):

        with open('Impact-Model-Matrix/vwap_end_55800000.pkl', 'rb') as f:
            self.VWAP_330 = pd.read_pickle(f)

        with open('Impact-Model-Matrix/ArrivalPrice.pkl', 'rb') as f:
            self.Arrival = pd.read_pickle(f)

        with open('Impact-Model-Matrix/TerminalPrice.pkl', 'rb') as f:
            self.Terminal = pd.read_pickle(f)

    def compute_h(self):
        # permanent impact g
        self.g = (self.Terminal - self.Arrival)/2
        # temporary impact h
        self.h = self.VWAP_330 - self.Arrival - self.g

        output_path = 'Impact-Model-Matrix/TemporaryImpact.pkl'
        if not os.path.exists(output_path):
            self.h.to_pickle(output_path)
            print("Finish calculating impacts")
        else:
            print("Impact file exists")


if __name__ == "__main__":
    impact_cal = ImpactCalculation()
    impact_cal.compute_h()
