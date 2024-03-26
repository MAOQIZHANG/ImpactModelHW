import pandas as pd
import os

with open('Impact-Model-Matrix/vwap_end_57600000.pkl', 'rb') as f:
    VWAP_330 = pd.read_pickle(f)

with open('Impact-Model-Matrix/ArrivalPrice.pkl', 'rb') as f:
    Arrival = pd.read_pickle(f)

with open('Impact-Model-Matrix/TerminalPrice.pkl', 'rb') as f:
    Terminal = pd.read_pickle(f)

# permanent impact g
g = (Terminal - Arrival)/2
# temporary impact h
h = VWAP_330 - Arrival - g

output_path = 'Impact-Model-Matrix/TemporaryImpact.pkl'
if not os.path.exists(output_path):
    h.to_pickle(output_path)
    print("Finish calculating impacts")
else:
    print("Impact file exists")
