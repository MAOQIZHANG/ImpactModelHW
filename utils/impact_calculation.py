import pandas as pd

with open('Impact-Model-Matrix/vwap_end_57600000.pkl', 'rb') as f:
    VWAP_330 = pd.read_pickle(f)

with open('Impact-Model-Matrix/ArrivalPrice.pkl', 'rb') as f:
    Arrival = pd.read_pickle(f)

with open('Impact-Model-Matrix/TerminalPrice.pkl', 'rb') as f:
    Terminal = pd.read_pickle(f)

# permant impact g
g = (Terminal - Arrival)/2
# temporary impact h
h = VWAP_330 - Arrival - g
h.to_pickle('Impact-Model-Matrix/TemporaryImpact.pkl')