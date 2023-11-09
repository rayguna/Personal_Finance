import yfinance as yf
import numpy as np
import pandas as pd


class YFStockData:
    def __init__(self, lstStocks):
        self.lstStocks = lstStocks
        self.stock_data = {}

        self.df_port=pd.DataFrame()


    def fetch_data(self, start_date, end_date):
        """Download stock data from yahoo finance

           inputs:
            - start_date (date): initial date in yyyy-mm-dd (e.g., 2023-01-01)
            - end_date (date): last date in yyyy-mm-dd (e.g., 2023-12-31)
        
           return:
            None

            *Note that percent change is arithmetic and log return is geometric
        """

        for stock_symbol in self.lstStocks:
            stock = yf.Ticker(stock_symbol)
            df = stock.history(period="1d", start=start_date, end=end_date)

            #add log_return
            # Calculate the percentage change
            df['PercentageChange'] = df['Close'].pct_change()

            # Calculate the log return
            df['Log_Return'] = np.log(1 + df['PercentageChange'])

            self.stock_data[stock_symbol] = df

    def get_stock_data(self, stock_symbol):
        """Get stock data

           inputs:
            - stock_symbol (string): a stock symbol
        
           return:
            dataframe
        """

        if stock_symbol in self.stock_data:
            return self.stock_data[stock_symbol]
        else:
            return None

    def portfolio_allocation(self, lstStocks, lstAllocation):
        """Allocate stocks within the portfolio

           inputs:
            - lstStocks (list): a list of stock symbols
            - lstAllocation (list): a list of fractions that correspond to the stock symbols

           return:
            - pandas dataframe (dataframe)

           *The Log return of the combined portfolio is different from the sum of the individual stock log return.
            We can only calculate the covariance from the individual log return, not from the combined portfolio log return. 
        """

        try:
            self.df_port=pd.DataFrame()
            #if len(lstAllocation)==len(lstStocks) and sum(lstAllocation)==1:
                
            #create columns of normalized closing price for the individual symbol
            for i,symbol in enumerate(lstStocks):
                self.df_port=pd.concat([self.df_port, lstAllocation[i]*self.get_stock_data(symbol)["Close"]], axis=1)
            self.df_port.columns=lstStocks

            #create a combined column
            self.df_port["Combined"]=self.df_port[lstStocks].sum(axis=1)

            #create a combined normalized column
            self.df_port["Combined_N"]=self.df_port["Combined"]/self.df_port["Combined"][0]
            
            #create a daily return column
            self.df_port["Daily_Return"]=self.df_port["Combined"].pct_change(1)

            #create log return column
            self.df_port["Log_Return"]=np.log(self.df_port["Combined"]/self.df_port["Combined"].shift(1))

            return self.df_port

            #else:
            #    print("You must specify equal number of allocations to the number of stocks.")
        except:
            print("Some stocks symbols don't exist or don't match to the existing list. Please check!")