from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt

import statsmodels.api as sm

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
        data = pd.DataFrame()
        data["X"] = np.abs(X_long)
        data["sign_X"] = np.sign(X_long)
        data["V"] = V_long.astype(float)
        data["h"] = h_long
        data["sigma"] = sigma_long.astype(float)
        data.dropna(axis=0, inplace=True)
        self.data["log_X"] = np.log(data["X"])
        self.data["sign_X"] = data["sign_X"]
        self.data["log_V"] = np.log(data["V"])
        self.data["log_sigma"] = np.log(data["sigma"])
        self.data["log_h"] = np.log(np.abs(data["h"]))
        self.data["sign_h"] = np.sign(data["h"])
        self.log_data = pd.DataFrame()
        self.log_data["y"] = self.data["sign_h"] * data["sign_X"] * (self.data["log_h"] - self.data["log_sigma"])
        self.log_data["X"] = self.data["log_X"] - self.data["log_V"] - np.log(6/6.5)
        self.log_data.replace([np.inf, -np.inf], np.nan, inplace=True)
        self.log_data.dropna(axis=0, inplace=True)


    def regress(self):
        X = sm.add_constant(self.log_data["X"])
        y = self.log_data["y"]
        model = sm.OLS(y, X).fit()
        alpha = model.params[0]  # Intercept (alpha)
        beta = model.params[1]  # Slope(s) (beta values)
        eta = np.exp(alpha)
        print(f"eta = {eta}, beta = {beta}")
        print(model.summary())
        self.eta = eta
        self.beta = beta
        return alpha, beta

    def parametric_bootstrap(self, num_simulations=1000):
        alphas = []
        betas = []

        for _ in range(num_simulations):
            # Simulate data based on estimated parameters
            simulated_data = self.simulate_data()

            # Fit regression model on simulated data
            X_sim = sm.add_constant(simulated_data["X"])
            y_sim = simulated_data["y"]
            model_sim = sm.OLS(y_sim, X_sim).fit()

            # Append estimated parameters to lists
            alphas.append(model_sim.params.iloc[0])  # Use iloc indexer
            betas.append(model_sim.params.iloc[1])  # Use iloc indexer

        return alphas, betas

    def simulate_data(self):
        # Simulate data based on estimated parameters
        # You need to replace this with actual simulation logic based on your model
        simulated_X = np.random.normal(loc=self.log_data["X"].mean(), scale=self.log_data["X"].std(), size=len(self.log_data))
        simulated_y = np.random.normal(loc=self.log_data["y"].mean(), scale=self.log_data["y"].std(), size=len(self.log_data))

        simulated_data = pd.DataFrame({"X": simulated_X, "y": simulated_y})

        return simulated_data


# Usage
# Create an instance of the model and call methods
impact_model = ImpactModel('Impact-Model-Matrix')
impact_model.read_data()
impact_model.regress()
# Perform parametric bootstrap
alphas_bootstrap, betas_bootstrap = impact_model.parametric_bootstrap(num_simulations=10)

def plot_histograms(alphas, betas, filename='bootstrap_histogram.png'):
    plt.hist(alphas, bins=30, alpha=0.5, label='Alphas')
    plt.hist(betas, bins=30, alpha=0.5, label='Betas')
    plt.legend()
    plt.savefig(filename)  # Save the plot to a file
    plt.close()  # Close the plot to release memory

plot_histograms(alphas_bootstrap, betas_bootstrap, filename='bootstrap_histogram.png')