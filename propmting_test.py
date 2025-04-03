import time
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import matplotlib.pyplot as plt


class NiftyScraper:
    def __init__(self, url):
        self.url = url
        self.driver = None
        self.headers = []
        self.rows_data = []

    def initialize_driver(self):
        """Initialize the Selenium WebDriver."""
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

    def open_url(self):
        """Open the target URL."""
        self.driver.get(self.url)
        time.sleep(5)  # Wait for the page to load

    def extract_headers(self):
        """Extract table headers from the webpage."""
        for i in range(1, 15):  # 14 columns
            xpath = f'//*[@id="equityStockTable"]/thead/tr/th[{i}]'
            header_element = self.driver.find_element(By.XPATH, xpath)
            self.headers.append(header_element.text.strip())

    def extract_table_data(self):
        """Extract table data dynamically."""
        row_index = 2  # Start from second row
        while True:
            try:
                row_xpath = f'//*[@id="equityStockTable"]/tbody/tr[{row_index}]'
                row_element = self.driver.find_element(By.XPATH, row_xpath)
                columns = row_element.find_elements(By.TAG_NAME, "td")

                if not columns:
                    break  # Stop if there are no more rows

                row_values = [col.text.strip() for col in columns]
                self.rows_data.append(row_values)

                row_index += 1  # Move to the next row
            except Exception:
                break  # Exit loop if no more rows

    def save_to_csv(self, filename="nifty50_data.csv"):
        """Save the extracted data to a CSV file."""
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(self.headers)  # Write headers
            writer.writerows(self.rows_data)  # Write row data
        print(f"Data successfully saved to {filename}")

    def close_driver(self):
        """Close the browser."""
        self.driver.quit()


class NiftyAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.df = pd.read_csv("/home/shtlp_0042/Desktop/TICKETS/nifty50_data.csv",delimiter=",",encoding="utf-8", header=0, skiprows=1)
        self.df = self.df.loc[:, ~self.df.columns.str.contains('^Unnamed')]
        column_names = pd.read_csv("/home/shtlp_0042/Desktop/TICKETS/nifty50_data.csv").columns
        self.df.columns = column_names


    def get_top_gainers_losers(self):
        """Get top 5 gainers and top 5 losers based on '%CHNG'."""
        top_gainers = self.df.nlargest(5, "%CHNG")
        top_losers = self.df.nsmallest(5, "%CHNG")
        return top_gainers, top_losers

    def identify_below_52W_high(self):
        """Identify 5 stocks that are currently 30% below their 52-week high."""
        # self.df["LTP"] = pd.to_numeric(self.df["LTP"])
        # self.df["52W H"] = pd.to_numeric(self.df["52W H"])
        self.df["LTP"] = self.df["LTP"].str.replace(",", "", regex=True).astype(float)
        self.df["52W H"] = self.df["52W H"].str.replace(",","",regex=True).astype(float)
        self.df["below_52W_H"] = ((self.df["52W H"] - self.df["LTP"]) / self.df["52W H"]) * 100
        below_30_percent = self.df[self.df["below_52W_H"] >= 30].nlargest(5, "below_52W_H")
        return below_30_percent

    def identify_above_52W_low(self):
        """Identify 5 stocks that are currently 20% above their 52-week low."""
        self.df["52W L"] = self.df["52W L"].str.replace(",","",regex=True).astype(float)
        self.df["above_52W_L"] = ((self.df["LTP"] - self.df["52W L"]) / self.df["52W L"]) * 100
        above_20_percent = self.df[self.df["above_52W_L"] >= 20].nlargest(5, "above_52W_L")
        return above_20_percent
    
    def top_5_highest_returns(self):
    # Get top 5 stocks based on 30-day percentage change
        top_5 = self.df.nlargest(5, "30 D\n%CHNG")

        return top_5[["SYMBOL", "LTP", "30 D\n%CHNG"]] 

    def display_results(self):
        """Display the results."""
        top_gainers, top_losers = self.get_top_gainers_losers()
        print("\nTop 5 Gainers:")
        print(top_gainers[["SYMBOL", "%CHNG"]])

        print("\nTop 5 Losers:")
        print(top_losers[["SYMBOL", "%CHNG"]])

        print("\n5 Stocks 30% Below Their 52-Week High:")
        print(self.identify_below_52W_high()[["SYMBOL", "LTP", "52W H"]])

        print("\n5 Stocks 20% Above Their 52-Week Low:")
        print(self.identify_above_52W_low()[["SYMBOL", "LTP", "52W L"]])

        print("\n 5 stocks that gave maximum returns in last 30 days")
        print(self.top_5_highest_returns()[["SYMBOL", "LTP", "30 D\n%CHNG"]])

    def plot_gainers_losers(self,top_gainers, top_losers):
        """Plot a bar chart for the top 5 gainers and losers based on %CHNG."""
        
        fig, ax = plt.subplots(figsize=(10, 5))

        # Gainers
        gainers_symbols = top_gainers["SYMBOL"]
        gainers_changes = top_gainers["%CHNG"]

        # Losers
        losers_symbols = top_losers["SYMBOL"]
        losers_changes = top_losers["%CHNG"]

        # Combine data
        symbols = list(gainers_symbols) + list(losers_symbols)
        changes = list(gainers_changes) + list(losers_changes)
        colors = ["green"] * 5 + ["red"] * 5  # Green for gainers, Red for losers

        # Create bar chart
        ax.bar(symbols, changes, color=colors)
        ax.set_xlabel("Stock Symbol")
        ax.set_ylabel("% Change")
        ax.set_title("Top 5 Gainers & Losers in NIFTY 50")
        ax.axhline(0, color="black", linewidth=0.8)  # Reference line at 0
        plt.xticks(rotation=45)
        # plt.show(block=True)
        plt.savefig("nifty_gainers_losers.png")

if __name__ == "__main__":
    # Scraping the data
    url = "https://www.nseindia.com/market-data/live-equity-market?symbol=NIFTY%2050"
    scraper = NiftyScraper(url)
    scraper.initialize_driver()
    scraper.open_url()
    scraper.extract_headers()
    scraper.extract_table_data()
    scraper.save_to_csv()
    scraper.close_driver()

    # Analyzing the data
    analyzer = NiftyAnalyzer("nifty50_data.csv")
    analyzer.display_results()
    top_gainers, top_losers = analyzer.get_top_gainers_losers()
    analyzer.plot_gainers_losers(top_gainers, top_losers)
