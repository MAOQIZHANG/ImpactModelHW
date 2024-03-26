from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import json
from scipy.optimize import curve_fit
from sklearn.utils import resample

class ImpactModel:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = pd.DataFrame()
        self.eta = None
        self.beta = None

    @staticmethod
    def read_pkl(path):
        with open(path, 'rb') as f:
            df = pd.read_pickle(f)
        return df

    @staticmethod
    def melt_df(df, var_name):
        melted_df = pd.melt(df.reset_index(), id_vars='index', value_vars=df.columns, var_name='Day',
                            value_name=var_name).rename(columns={'index': 'Stock'})
        return melted_df[var_name]
    def read_data(self):
        json_file_path = f"{self.filepath}/high_vol_days.json"

        with open(json_file_path, 'r') as file:
            high_vol_days = json.load(file)

        stocks = list(high_vol_days.keys())  # Or however you have your stocks defined
        days = range(65)  # Adjust based on your actual days

        # Initialize DataFrame with False values
        high_vol_df = pd.DataFrame(True, index=stocks, columns=days)
        for stock, high_vol_days_list in high_vol_days.items():
            for day_idx in high_vol_days_list:
                if day_idx in high_vol_df.columns:
                    high_vol_df.at[stock, day_idx] = False

        value_imbalance = self.read_pkl(f"{self.filepath}/value_imbalance.pkl")
        volatility = self.read_pkl(f"{self.filepath}/Volatility.pkl")
        volatility = volatility[high_vol_df]
        daily_value = self.read_pkl(f"{self.filepath}/daily_values.pkl")
        temporary_impact = self.read_pkl(f"{self.filepath}/TemporaryImpact.pkl")

        X_long = self.melt_df(value_imbalance, 'X')
        V_long = self.melt_df(daily_value, 'V')
        h_long = self.melt_df(temporary_impact, 'h')
        sigma_long = self.melt_df(volatility, 'sigma')
        self.data["X"] = X_long
        self.data["V"] = V_long.astype(float)
        self.data["h"] = h_long
        self.data["sigma"] = sigma_long.astype(float)
        self.data.dropna(axis=0, inplace=True)

    def universal_model(self, X, eta, beta, sigma, V):
        return eta * sigma * (X / (V * (6 / 6.5)))**beta
    def regress(self):
        if self.data is None:
            print("Data not loaded. Please run read_data() first.")
            return
        X = self.data['X'].values
        sigma = self.data['sigma'].values
        V = self.data['V'].values
        h = self.data['h'].values
        def fit_function(X, eta, beta):
            return self.universal_model(X, eta, beta, sigma, V)
        initial_eta_guess = 1.0
        initial_beta_guess = 0.5
        params, _ = curve_fit(fit_function, X, h, p0=[initial_eta_guess, initial_beta_guess])
        self.eta, self.beta = params
        print(f"Fitted Parameters - eta: {self.eta}, beta: {self.beta}")

# Usage
# Create an instance of the model and call methods
impact_model = ImpactModel('Impact-Model-Matrix')
impact_model.read_data()
impact_model.regress()
