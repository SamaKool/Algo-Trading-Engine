import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Backtester:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.data = None

    def load_data(self):
        print(f"Loading data for {self.symbol}...")
        self.data = yf.download(self.symbol, start=self.start_date, end=self.end_date)
        
        # Flatten MultiIndex columns
        if isinstance(self.data.columns, pd.MultiIndex):
            self.data.columns = self.data.columns.get_level_values(0)

        self.data.dropna(inplace=True)
        
        self.original_data = self.data.copy()
        print("Data loaded successfully.")

    def reset_data(self):
        self.data = self.original_data.copy()

    def add_moving_average(self, window_size):
        if self.data is None:
            return
        
        column_name = f"SMA_{window_size}"
        self.data[column_name] = self.data['Close'].rolling(window=window_size).mean()
        self.data.dropna(inplace=True)
        print(f"Added {column_name} to dataset.")

    def generate_signals(self, fast_window, slow_window):
        fast_col = f"SMA_{fast_window}"
        slow_col = f"SMA_{slow_window}"
        
        if fast_col not in self.data.columns or slow_col not in self.data.columns:
            print(f"Error: Calculate {fast_col} and {slow_col} first.")
            return

        self.data['Signal'] = np.where(self.data[fast_col] > self.data[slow_col], 1, 0)

    def calculate_pnl(self, transaction_cost=0.001):
        # Calculate Returns
        self.data['Daily_Return'] = self.data['Close'].pct_change()
        self.data['Position'] = self.data['Signal'].shift(1)
        
        # Strategy Returns
        self.data['Strategy_Return'] = self.data['Daily_Return'] * self.data['Position']
        
        # Transaction Costs
        self.data['Trades'] = self.data['Signal'].diff().abs().fillna(0)
        self.data['Strategy_Net_Return'] = self.data['Strategy_Return'] - (self.data['Trades'] * transaction_cost)
        
        # Cumulative Returns
        cumulative_return = (1 + self.data['Strategy_Net_Return']).cumprod()
        return cumulative_return

    def plot_results(self):
        if self.data is None: 
            return
        
        plt.figure(figsize=(14, 7))
        buy_and_hold = (1 + self.data['Daily_Return']).cumprod()
        strategy = (1 + self.data['Strategy_Net_Return']).cumprod()
        
        plt.plot(buy_and_hold, label="Buy & Hold", color='gray', alpha=0.5)
        plt.plot(strategy, label="My Strategy", color='blue')
        plt.title(f"Strategy Performance vs Benchmark ({self.symbol})")
        plt.legend()
        plt.grid(True)

        plt.show()
