
import pandas as pd

def read_pkl(path):
    with open(path, 'rb') as f:
        df = pd.read_pickle(f)
    return df

filepath = "Impact-Model-Matrix"
temporary_impact = read_pkl(f"{filepath}/TemporaryImpact.pkl")
print(temporary_impact.iloc[0])