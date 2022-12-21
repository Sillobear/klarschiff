# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 22:55:03 2021

@author: Schroeder
"""


import csv
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
import pandas
#import TickerSelector 

dates = []
prices = []
 
def get_data(filename, AnzahlTage):
   csvfile =  open(filename,mode="r") 
   csvFileReader = csv.reader(csvfile)
   for i in range(1,AnzahlTage):
       next(csvFileReader) #skipping column names
   counter = 1
   for row in csvFileReader:
        dates.append(counter)
        counter = counter + 1
        prices.append(float(row[4]))
   
   csvfile.close() 
   return

def get_data_II(filename,dd,pp,vondatum, bisdatum):
   

   ddff = pandas.read_csv(filename,sep=";",decimal=',', index_col=0)
   ddff=ddff.fillna(value = 1.0)
   ddff = ddff.truncate(after = bisdatum, before = vondatum)
   pp = ddff["Factor"].tolist()
   ddff = ddff.reset_index()
   dd = ddff.index.tolist()

   return dd, pp

 
def show_plot(dates,prices,rs,tit, ticker, file):
    linear_mod = linear_model.LinearRegression()
    dates = np.reshape(dates,(len(dates),1)) # converting to matrix of n X 1
    prices = np.reshape(prices,(len(prices),1))
    linear_mod.fit(dates,prices) #fitting the data points in the model
    pred = linear_mod.predict(dates)
    pred_up = pred + rs
    pred_dwn = pred - rs
    pred_up2 = pred + 2*rs
    pred_dwn2 = pred - 2*rs
    
    plt.scatter(dates,prices,color='gray') #plotting the initial datapoints 
    plt.plot(dates,pred,color='red',linewidth=2)
    plt.plot(dates,pred_up,color='blue',linewidth=1)
    plt.plot(dates,pred_dwn,color='green',linewidth=1)
    plt.plot(dates,pred_up2,color='blue',linewidth=1)
    plt.plot(dates,pred_dwn2,color='green',linewidth=1)
    #plotting the line made by linear regression
    
    
    plt.title(tit,fontsize=12)
    #plt.show()
    plt.savefig(file+ticker+".jpg")
    plt.close()
    
    # returns the deviation from mean und letzte grosse Bewegung gemessen in Sigma
    return int(100*(prices[-1][0]-pred[-1][0])/rs), int(100*(prices[-1][0]-prices[-2][0])/rs)

def predict_price(dates,prices,x):  
    x=np.reshape(x,(1,1))
    linear_mod = linear_model.LinearRegression() #defining the linear regression model
    dates = np.reshape(dates,(len(dates),1)) # converting to matrix of n X 1
    prices = np.reshape(prices,(len(prices),1))
    linear_mod.fit(dates,prices) #fitting the data points in the model
    r_sq = linear_mod.score(dates,prices)
    predicted_price =linear_mod.predict(x)
    return predicted_price[0][0],linear_mod.coef_[0][0] ,linear_mod.intercept_[0], r_sq, np.mean((predicted_price - prices)**2)


def regression_stats(dates,prices):
    linear_mod = linear_model.LinearRegression() #defining the linear regression model
    dates = np.reshape(dates,(len(dates),1)) # converting to matrix of n X 1
    prices = np.reshape(prices,(len(prices),1))
    linear_mod.fit(dates,prices) #fitting the data points in the model
    r_sq = linear_mod.score(dates,prices)
    a = linear_mod.intercept_[0]
    m = linear_mod.coef_[0][0]
    
    return m,a, r_sq , np.mean((linear_mod.predict(dates) - prices)**2)

 

 
#show_plot(dates,prices) 
#image of the plot will be generated. Save it if you want and then Close it to continue the execution of the below code.
 

#print("The stock open price for 29th Feb is: $",str(predicted_price))
#print("The regression coefficient is ",str(coefficient),", and the constant is ", str(constant))
#print("The regression quality is ",str(r_sq))
#print("the relationship equation between dates and prices is: price = ",str(coefficient),"* date + ",str(constant))