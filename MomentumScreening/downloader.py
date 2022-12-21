# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 08:21:50 2021

@author: Schroeder
"""
# downloads preisdaten von yahho gemäß einer tickerlist und speicher die fiels als csv dateien ab.

from scipy.stats import linregress
import matplotlib.pyplot as plt


from datetime import datetime
from datetime import date
import calendar

from os import listdir
from os.path import isfile, join

# Imports
from pandas_datareader import data as pdr

import numpy as np
import seaborn as sns
from sklearn import linear_model

from pandas import ExcelWriter
import datetime
import yfinance as yf
import pandas as pd
import time 
import csv

import StockscreenerPlotter_stats

################################################################################################################
# europasektoren  USSectors europa styles stylesbroad asiapacificeats 
# AlleAnbieter AlleInternational macro MDAX PrimeAllShare AMERICA600
#################################################################################################################

mypath = StockscreenerPlotter_stats.Universe["tmpdatadir"]

enddatum = "2033-07-03"
startdatum = "2005-01-01"
roll_window = 60

#mypath = "C:/Michael/ETFS/tmpData/"


def momentum(closes):
    returns = closes
    x = np.arange(len(returns))
    slope, _, rvalue, _, _ = linregress(x, returns)
    return ((1 + slope) ** 252) * (rvalue ** 2)  # annualize slope and multiply by R^2


def regression_quality(data):
    linear_mod = linear_model.LinearRegression() #defining the linear regression model
    dates = np.arange(len(data))
    dates = np.reshape(dates,(len(dates),1)) # converting to matrix of n X 1
    prices= data.tolist()
    #prices = data
    prices = np.reshape(prices,(len(prices),1))
    linear_mod.fit(dates,prices) #fitting the data points in the model
    r_sq = linear_mod.score(dates,prices)
    a = linear_mod.intercept_[0]
    m = linear_mod.coef_[0][0]
    
    #predicted_price =linear_mod.predict(x)
    
    return r_sq * m
    #return ((1+m)**250) / (np.mean((linear_mod.predict(dates) - prices)**2))

def regression_stats(data):
    linear_mod = linear_model.LinearRegression() #defining the linear regression model
    dates = np.arange(len(data))
    dates = np.reshape(dates,(len(dates),1)) # converting to matrix of n X 1
    prices= data.to_list()
    prices = np.reshape(prices,(len(prices),1))
    
    linear_mod.fit(dates,prices) #fitting the data points in the model
    r_sq = linear_mod.score(dates,prices)
    a = linear_mod.intercept_[0]
    m = linear_mod.coef_[0][0]
    
    #predicted_price =linear_mod.predict(x)
    print( np.mean((linear_mod.predict(dates) - prices)**2))
    return m,a, r_sq , np.mean((linear_mod.predict(dates) - prices)**2)




def loaddown(tickers):
    
    end_date = datetime.datetime.strptime(enddatum, '%Y-%m-%d')
    start_date =  datetime.datetime.strptime(startdatum, '%Y-%m-%d')

    for ticker in tickers:
        try:
            
            df = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))
            oo = yf.Ticker(ticker)
            ticker = oo.info["longName"]
            if ticker == "CON.DE" : ticker = "CONT.DE"
            df[["Adj Close"]].to_csv(mypath + f'{ticker}',sep=";",decimal=',', float_format='%.5f')
            time.sleep(0.4)    
            
        except:
                print(ticker, " :Abruf fehler haft. ")
        

    
def main():
    etfliste = pd.DataFrame()
    
    
    if 1>2:
        etfliste = pd.read_csv("C:/Users/Schroeder/OneDrive/Trading/ETFS/Mutterlisten/MDAX.csv", sep=";", encoding='latin-1',usecols=["TICKER","TRUENAMES"])
        tickers=etfliste["TICKER"]
        names=etfliste["TRUENAMES"]
        loaddown(tickers)
    
    if 2 > 1:
        universe = pd.DataFrame(StockscreenerPlotter_stats.Universe)
        for index, row in universe.iterrows():
            mypath = row["tmpdatadir"]
            Pfad = mypath
            tickerlst = pd.read_csv(Pfad +row["quelldatei"][:4]+"_result.csv", sep=";", encoding='latin-1',usecols=["ETF"])
            #onlyfiles = [f for f in listdir(Pfad) if (isfile(join(Pfad, f))and not f.startswith("_"))]
            tickerlist = tickerlst["ETF"][:62].tolist()
            
            stocks = (
            (pd.concat(
                [pd.read_csv(Pfad + ticker + ".csv", index_col='Date', sep=";", decimal=',',parse_dates=True)['Factor'].rename(ticker)
                for ticker in tickerlist],
                axis=1,
                sort=True)
            )
            )
            stocks = stocks.loc[:,~stocks.columns.duplicated()]
            stocks = stocks.fillna(method = "ffill")
            #stocks = (stocks.pct_change()+1).cumprod()
            stocks = stocks.fillna(1.0)
            momentums = stocks.copy(deep=True)
            
            momentums=momentums.truncate(before=startdatum)
            momentums=momentums.truncate(after=enddatum)
            
            momentums.to_csv(Pfad + "__FACS.csv",sep=";",decimal=',', float_format='%.5f', index=True)

            for ticker in tickerlist:
                print(ticker)
                if ticker=="LHA.DE":
                    print("stop !")
                #linear fit:
                momentums[ticker]= 100*stocks[ticker].rolling(roll_window).apply(regression_quality,raw=False)
                #momentums[ticker[:-4]+"_pct"]= momentums[ticker[:-4]].pct_change()

                    
                # momentums[ticker[:-4]+"_pctmean"]= momentums[ticker[:-4]+"_pct"].rolling(roll_window).mean()
                # momentums[ticker[:-4]+"_std"]= momentums[ticker[:-4]+"_pct"].rolling(roll_window).std()
                # momentums[ticker[:-4]+"_zs"]=  (momentums[ticker[:-4]+"_pct"]-momentums[ticker[:-4]+"_pctmean"])/momentums[ticker[:-4]+"_std"]
                    #momentums = momentums.sort_index(axis=1)

                    #exp. fitt:
                    #momentums[ticker] = stocks[ticker].rolling(roll_window).apply(momentum, raw=False)
                    
            plotable = momentums[roll_window:]
            momentums.to_csv(Pfad + "__MOMS.csv",sep=";",decimal=',', float_format='%.5f', index=True)
            
            num_of_cols_in_plot = 10

            number_of_tickers = plotable.shape[1]        
            number_of_plots = int(number_of_tickers /num_of_cols_in_plot)
            for j in range(number_of_plots):
                startindex = (j)*num_of_cols_in_plot
                endindex = np.minimum((j+1)*num_of_cols_in_plot,number_of_tickers-1)
                plotme=plotable.iloc[:,startindex:endindex]

                #plt.figure(figsize = (60,30))
                heatm = sns.heatmap(plotme, annot=False)
                fig = heatm.get_figure()
                fig.savefig(Pfad + "__" + str(j)+ "MOMS.png")
        

                #plt.figure(figsize=(12, 9))
                #plt.xlabel('Days')
                #plt.ylabel('Stock Price')
            
                #bests = momentums.max().sort_values(ascending=False).index[:3]
                #bests = momentums.iloc[-1].sort_values(ascending=False).index[:10]
                
                # for best in bests:
                #     print("------")
                #     print(best)
                #     #end = momentums[best].index.get_loc(momentums[best].idxmax())
                #     rets = stocks[best].tail(120)
                #     rets = rets.fillna(1.0)
                #     x = np.arange(len(rets))
                    
                #     #lin fit:
                #     m,a,r_sq,stderr = regression_stats(rets)
                #     #exp. fit:
                #     #slope, intercept, r_value, p_value, std_err = linregress(x, rets)
                    
                #     plt.plot(np.arange(roll_window+100), stocks[best].tail(100))
                #     #exp. fit:
                #     #plt.plot(x, np.e ** (intercept + slope*x))
                #     # lin fit:
                #     plt.plot(x, a + m*x)
                
                
                # for best in bests:
                #     print("------")
                #     print(best)
                #     end = momentums[best].index.get_loc(momentums[best].idxmax())
                #     rets = stocks[best].iloc[end - roll_window : end]
                #     rets = rets.fillna(1.0)
                #     x = np.arange(len(rets))
                    
                #     #lin fit:
                #     m,a,r_sq,stderr = regression_stats(rets)
                #     #exp. fit:
                #     #slope, intercept, r_value, p_value, std_err = linregress(x, rets)
                    
                #     plt.plot(np.arange(roll_window+10), stocks[best][end-roll_window:end+10])
                #     #exp. fit:
                #     #plt.plot(x, np.e ** (intercept + slope*x))
                #     # lin fit:
                #     plt.plot(x, a + m*x)
            
            
        
        
        
        
        
  
    
if __name__ == "__main__":
   # while True:    
        main()
        time.sleep(1) 

