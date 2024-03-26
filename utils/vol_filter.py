import pandas as pd
import numpy as np
import json

with open('/Users/chenjiaying/Desktop/hw2_data/Impact-Model-Matrix/2MinMidQuoteReturns.pkl', 'rb') as f:
    df = pd.read_pickle(f)

# DataFrame containing 2-minute mid-quote returns of 500 stocks for 65 days
# Shape should be (500, 12675)

num_of_days = 65

rolling_window_days = 10  # Use the last 10 days data to calculate volatility

num_of_intervals = 195  # Each day has 195 intervals (6.5 hours)

step_size = rolling_window_days * num_of_intervals

# volatility dataframe of 2-min returns in the last 10 days scaled to daily value
volatility_df = pd.DataFrame(index=df.index, columns=range(num_of_days))

# Plug in the volatility of the first day
volatility_df.iloc[:, 0] = df.iloc[:, 0:num_of_intervals].std(axis=1) * np.sqrt(num_of_intervals)

for day in range(0, num_of_days-1):
    start_day = day * num_of_intervals
    end_day = start_day + step_size
    rolling_volatility = df.iloc[:, start_day:end_day].std(axis=1)
    # Convert to daily value
    daily_volatility = rolling_volatility * np.sqrt(step_size * rolling_window_days)
    volatility_df.iloc[:, day+1] = daily_volatility

# print(volatility_df)
# print(volatility_df.isnull().sum())
    
# volatility_df.to_pickle('Volatility.pkl')

# Calculate the 95th percentile of the volatility distribution
volatility_threshold = np.percentile(volatility_df.values.flatten(), 95)

# high_vol_dict containing high-vol days for each stock, with ticker as key and days no. as value
high_vol_dict = {}
for i, row in volatility_df.iterrows():
    exceeding_columns = row.index[row > volatility_threshold].tolist()
    high_vol_dict[i] = exceeding_columns
# print(high_vol_dict)
    
"""with open("high_vol_days.json", "w") as outfile: 
    json.dump(high_vol_dict, outfile)"""