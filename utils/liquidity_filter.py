import os
import numpy as np
import pandas as pd
import json

# this file is used to calculate average daily volume over the last 10 days
# and divide all stocks to liquid and illiquid groups based on the average daily volume

with open('Impact-Model-Matrix/daily_volume.pkl', 'rb') as f:
    daily_volume = pd.read_pickle(f)  # (502, 65) matrix

num_of_days = 65
avg_volume = pd.DataFrame(index=daily_volume.index, columns=range(num_of_days))

for day in range(num_of_days):
    if day <= 9:
        rolling_volume = daily_volume.iloc[:, 0:day+1].mean(axis=1)
    else:
        rolling_volume = daily_volume.iloc[:, day-9:day+1].mean(axis=1)
    avg_volume.iloc[:, day] = rolling_volume

threshold = avg_volume.sum(axis=1).median()

stock_dict = {
    'liquid': avg_volume[avg_volume.sum(axis=1) > threshold].index.tolist(),
    'illiquid': avg_volume[avg_volume.sum(axis=1) <= threshold].index.tolist()
}

with open("data/liquidity.json", "w") as outfile: 
    json.dump(stock_dict, outfile)