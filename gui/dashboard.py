import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar

# Import data fetching functions from APIs
from apis.stocks import get_stock_history
from apis.crypto import get_crypto_prices
from apis.news import get_market_news
from apis.exchange import get_exchange_rates_all

# For plotting charts
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Plot stock price line chart
def plot_stock_chart(frame):
    dates, prices = get_stock_history("AAPL")

    # Create a matplotlib figure
    fig = Figure(figsize=(5, 2.5), dpi=100)
    ax = fig.add_subplot(111)

    # Plot stock prices
    ax.plot(dates, prices, marker='o')
    ax.set_title("AAPL Stock Prices")
    ax.set_ylabel("Price (USD)")
    ax.set_xticks(dates[::2])  # Reduce x-axis clutter
    ax.tick_params(axis='x', rotation=45)

    # Embed chart into Tkinter frame
    FigureCanvasTkAgg(fig, master=frame).get_tk_widget().pack()


# Plot cryptocurrency bar chart
def plot_crypto_chart(frame):
    data = get_crypto_prices(["BTC", "ETH", "XRP", "ADA"])

    fig = Figure(figsize=(5, 2.5), dpi=100)
    ax = fig.add_subplot(111)

    ax.bar(data.keys(), data.values())
    ax.set_title("Crypto Prices (USD)")
    ax.set_ylabel("Price")

    FigureCanvasTkAgg(fig, master=frame).get_tk_widget().pack()


# Plot exchange rates as a bar chart
def plot_exchange_chart(frame):
    data = get_exchange_rates_all("USD", ["EUR", "GBP", "JPY", "INR", "AUD"])

    fig = Figure(figsize=(5, 2.5), dpi=100)
    ax = fig.add_subplot(111)

    ax.bar(data.keys(), data.values(), color='orange')
    ax.set_title("Exchange Rates (Base: USD)")
    ax.set_ylabel("Rate")

    FigureCanvasTkAgg(fig, master=frame).get_tk_widget().pack()


# Show market news in a table using Treeview
def show_news_table(frame):
    news_items = get_market_news()  # [{'title': ..., 'source': ...}, ...]

    columns = ("Title", "Source")
    tree = ttk.Treeview(frame, columns=columns, show='headings', height=5)

    # Define column headers and formatting
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=400 if col == "Title" else 150, anchor="w")

    # Insert each news item as a row
    for item in news_items:
        tree.insert("", "end", values=(item['title'], item['source']))

    tree.pack()


# Main dashboard function
def start_dashboard():
    window = tk.Tk()
    window.title("Smart Market Analyzer")
    window.geometry("1000x800")  # Set window size

    # Create scrollable content area
    canvas = tk.Canvas(window)
    scrollbar = Scrollbar(window, command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    # Auto-resize scroll area
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Attach scrollable frame to canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Add GUI components
    ttk.Label(scrollable_frame, text="📈 Stock Market", font=("Arial", 16)).pack(pady=5)
    plot_stock_chart(scrollable_frame)

    ttk.Label(scrollable_frame, text="💰 Crypto Prices", font=("Arial", 16)).pack(pady=5)
    plot_crypto_chart(scrollable_frame)

    ttk.Label(scrollable_frame, text="📰 Market News", font=("Arial", 16)).pack(pady=5)
    show_news_table(scrollable_frame)

    ttk.Label(scrollable_frame, text="💱 Exchange Rates", font=("Arial", 16)).pack(pady=5)
    plot_exchange_chart(scrollable_frame)

    # Pack canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Start the GUI loop
    window.mainloop()
