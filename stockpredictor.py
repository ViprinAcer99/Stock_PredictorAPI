import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import simpledialog
from alpha_vantage.timeseries import TimeSeries

API_KEY = 'MGSZWLEZ4WWT2DDL'

def fetch_alpha_vantage_data(stock_symbol, start_datetime, end_datetime):
    try:
        ts = TimeSeries(key=API_KEY, output_format='pandas')
        data, meta_data = ts.get_intraday(symbol=stock_symbol, interval='1min', outputsize='full')
        
        # Filter data based on the specified datetime range
        data = data[(data.index >= start_datetime) & (data.index <= end_datetime)]
        
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def main():
    # Ask for stock symbol
    root = tk.Tk()
    root.withdraw()
    stock_symbol = simpledialog.askstring("Input", "Which stock symbol do you want to predict?")

    # Calculate start and end datetimes for today's date, 9:30 AM to 4:00 PM
    current_date = datetime.now().date()
    market_start_time = datetime(current_date.year, current_date.month, current_date.day, 9, 30)
    market_end_time = datetime(current_date.year, current_date.month, current_date.day, 16, 0)
    
    # Fetch intraday stock data for today
    intraday_data = fetch_alpha_vantage_data(stock_symbol, market_start_time, market_end_time)
    
    if intraday_data is None:
        return

    # Dummy predictions for demonstration
    actual_predictions = intraday_data['4. close'].values + np.random.normal(0, 0.5, size=len(intraday_data))

    # Extract time labels and split them into separate hours and minutes
    time_labels = intraday_data.index.strftime('%H:%M').tolist()

    # Display a subset of time labels for better readability
    label_frequency = max(len(time_labels) // 15, 1)
    time_labels = [label if i % label_frequency == 0 else '' for i, label in enumerate(time_labels)]

    # Reverse the order of data points and time labels
    intraday_data = intraday_data[::-1]
    actual_predictions = actual_predictions[::-1]
    time_labels = time_labels[::-1]

    # Plot the predictions and real values
    plt.figure(figsize=(12, 7))
    plt.plot(range(len(intraday_data)), intraday_data['4. close'], label='Actual Prices', color='blue')
    plt.plot(range(len(intraday_data)), actual_predictions, label='Predicted Prices', linestyle='dashed', color='red')

    # Add data labels to the data points with larger font size
    label_font_size = 12
    for i in range(0, len(intraday_data), label_frequency):
        plt.text(i, intraday_data['4. close'].iloc[i], f'{intraday_data["4. close"].iloc[i]:.2f}', ha='center', va='bottom', color='blue', fontsize=label_font_size)
        plt.text(i, actual_predictions[i], f'{actual_predictions[i]:.2f}', ha='center', va='top', color='red', fontsize=label_font_size)

    plt.title(f"Actual vs Predicted Prices for {stock_symbol} on {current_date}")
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # Set x-axis ticks and labels
    plt.xticks(range(0, len(intraday_data), label_frequency), time_labels[::label_frequency], rotation=45)

    plt.show()

if __name__ == "__main__":
    main()
