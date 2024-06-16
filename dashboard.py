import requests
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from dotenv import load_dotenv


load_dotenv()
pwd = os.getenv('MY_PASSWORD')
api_key = os.getenv('MY_API_KEY')
if pwd is not None and key is not None:
    print('It worked')

# Function to get data from the API
def get_stock_data(symbol, interval):
    if interval == "Intraday":
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}'
    elif interval == "Daily":
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    elif interval == "Weekly":
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={api_key}'
    elif interval == "Monthly":
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={api_key}'
    
    response = requests.get(url)
    data = response.json()
    # print(f"API Response: {data}")
    return data

# Function to update the stock data in the GUI
def update_stock_data():
    stock_symbol = symbol_entry.get().upper()
    interval = interval_combo.get()
    if stock_symbol and interval:
        data = get_stock_data(stock_symbol, interval)
        if interval == "Intraday":
            time_series_key = 'Time Series (5min)'
        elif interval == "Daily":
            time_series_key = 'Time Series (Daily)'
        elif interval == "Weekly":
            time_series_key = 'Weekly Time Series'
        elif interval == "Monthly":
            time_series_key = 'Monthly Time Series'
        
        if time_series_key in data:
            times = []
            prices = []
            for time_point in sorted(data[time_series_key]):
                times.append(time_point)
                prices.append(float(data[time_series_key][time_point]['1. open']))
            
            latest_time = times[-1]
            latest_data = data[time_series_key][latest_time]
            price = latest_data['1. open']
            volume = latest_data.get('5. volume', 'N/A')
            change = float(latest_data['4. close']) - float(latest_data['1. open'])
            
            price_label.config(text=f"Price: {price}")
            volume_label.config(text=f"Volume: {volume}")
            change_label.config(text=f"Change: {change:.2f}")

            # Update the graph
            ax.clear()
            ax.plot(times, prices, label='Price')
            ax.set_title(f'{stock_symbol} Price Over Time')
            ax.set_xlabel('Time')
            ax.set_ylabel('Price')
            ax.legend()
            ax.grid(True)
            fig.autofmt_xdate()
            plot_canvas.draw()
        else:
            price_label.config(text="Price: N/A")
            volume_label.config(text="Volume: N/A")
            change_label.config(text="Change: N/A")
    root.after(60000, update_stock_data)

def on_closing():
    plt.close('all')
    root.destroy()

root = tk.Tk()
root.title("Stock Market Dashboard")
root.geometry("800x600")
root.protocol("WM_DELETE_WINDOW", on_closing)

# Create and place widgets
symbol_label = ttk.Label(root, text="Stock Symbol:")
symbol_label.grid(column=0, row=0, padx=(300, 0), pady=5)
symbol_entry = ttk.Entry(root)
symbol_entry.grid(column=1, row=0, padx=(0, 300), pady=5)

interval_label = ttk.Label(root, text="Interval:")
interval_label.grid(column=0, row=1, padx=(300, 0), pady=5)
interval_combo = ttk.Combobox(root, values=["Intraday", "Daily", "Weekly", "Monthly"])
interval_combo.grid(column=1, row=1, padx=(0, 300), pady=5)
interval_combo.current(0)

price_label = ttk.Label(root, text="Price: ")
price_label.grid(column=0, row=2, padx=(300, 0), pady=5)
volume_label = ttk.Label(root, text="Volume: ")
volume_label.grid(column=0, row=3, padx=(300, 0), pady=5)
change_label = ttk.Label(root, text="Change: ")
change_label.grid(column=0, row=4, padx=(300, 0), pady=5)

update_button = ttk.Button(root, text="Search", command=update_stock_data)
update_button.grid(column=1, row=5, padx=(0, 300), pady=5)

# Function that creat the graph
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_title("Stock Price Over Time")
ax.set_xlabel("Time")
ax.set_ylabel("Price")
plot_canvas = FigureCanvasTkAgg(fig, master=root)
plot_canvas.get_tk_widget().grid(column=0, row=7, columnspan=2, padx=5, pady=5)

root.mainloop()
