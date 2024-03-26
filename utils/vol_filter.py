import pandas as pd
import numpy as np
import json

class VolatilityFilter():

    def __init__(
            self, 
            num_of_days,
            rolling_window_days,  # no of look back days
        ):

        with open('Impact-Model-Matrix/2MinMidQuoteReturns.pkl', 'rb') as f:
            self.df = pd.read_pickle(f)  # Shape should be (500, 12675)
        if num_of_days == None:
            self.num_of_days = 65
        if rolling_window_days == None:
            self.rolling_window_days = 10   # Use the last 10 days data as default
        
        self.num_of_days = num_of_days
        self.rolling_window_days = rolling_window_days
        self.num_of_intervals = 195  # Each day has 195 intervals (6.5 hours)
        self.step_size = self.rolling_window_days * self.num_of_intervals
        
    def compute_volatility(self, save_to_file=True):
        # volatility dataframe of 2-min returns in the last 10 days scaled to daily value
        self.volatility_df = pd.DataFrame(index=self.df.index, columns=range(self.num_of_days))

        # Plug in the volatility of the first day
        self.volatility_df.iloc[:, 0] = self.df.iloc[:, 0:self.num_of_intervals].std(axis=1) * np.sqrt(self.num_of_intervals)

        for day in range(0, self.num_of_days-1):
            start_day = day * self.num_of_intervals
            end_day = start_day + self.step_size
            rolling_volatility = self.df.iloc[:, start_day:end_day].std(axis=1)
            # Convert to daily value
            daily_volatility = rolling_volatility * np.sqrt(self.step_size)
            self.volatility_df.iloc[:, day+1] = daily_volatility

        print("Volatility computation finished!")
        
        if save_to_file:
            self.volatility_df.to_pickle('Impact-Model-Matrix/Volatility_'+str(self.rolling_window_days)+'.pkl')
            print("Volatility saved to file!")
    
    def filter_high_vol(self, save_to_file=True):
        # Calculate the 95th percentile of the volatility distribution
        self.volatility_threshold = np.percentile(self.volatility_df.values.flatten(), 95)

        # high_vol_dict containing high-vol days for each stock, with ticker as key and days no. as value
        self.high_vol_dict = {}
        for i, row in self.volatility_df.iterrows():
            exceeding_columns = row.index[row > self.volatility_threshold].tolist()
            self.high_vol_dict[i] = exceeding_columns
        
        if save_to_file:
            with open("data/high_vol_days.json", "w") as outfile: 
                json.dump(self.high_vol_dict, outfile)


if __name__ == "__main__":
    Vol_10 = VolatilityFilter(65, 10)
    Vol_10.compute_volatility()
    Vol_10.filter_high_vol()