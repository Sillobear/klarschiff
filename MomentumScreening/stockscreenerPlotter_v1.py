  # -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 08:46:16 2021

@author: Schroeder
"""

# Liest holc etc. daten von bereits auf platte befindlichen csv dataframes .
# Soll Plot und Auswertung von datagrabbing trennen.



import TickerSelector, regression 
from datetime import datetime
from datetime import date
import calendar

# Imports
from pandas_datareader import data as pdr
#from yahoo_fin import stock_info as si

import numpy as np
from sklearn import linear_model

from pandas import ExcelWriter 
import yfinance as yf
import pandas as pd
import datetime
import time
import csv
   
import StockscreenerPlotter_stats 
import StockscreenerWinners_stats
import downloader

import os.path
from os.path import isfile, join

from os import listdir
#from os.path import isfile, join

#lieferrt bei gegebenem datatfram mit datum als index das erste Datum, das letzte, und zwei 
# dazwischen


def sort_final(liste):
    liste["rang"]= 0.1*liste[str(m)+"d_rs"]+0.9*liste[str(ll)+"d_rs"]
    liste["ranking"]=liste.rang.rank()
   
 
def max_dd(ser):
    max2here = pd.expanding_max(ser)
    dd2here = ser - max2here
    return dd2here.min()

#testhange

yf.pdr_override()

# Variables
#tickers = si.tickers_sp500()
#tickers = [item.replace(".", "-") for item in tickers] # Yahoo Finance uses dashes instead of dots
  
universe = pd.DataFrame(StockscreenerPlotter_stats.Universe)

for index, row in universe.iterrows():
    tickerfile = row["quellpfad"]+"\\"+row["quelldatei"]+".csv"
    plotfile = row["plotdir"]+"\\"
    resfile = row["resdir"]+"\\"
    tmpdatafile = row["tmpdatadir"]+"\\"
    vamsfile = row["vamsdir"]+"\\"

    print(f"***************     {tmpdatafile}            ********************")

  
    StockscreenerWinners_stats.cleardir(plotfile)
    #StockscreenerWinners_stats.cleardir(resfile)
    
    # etfliste = pd.DataFrame()
    # etfliste = pd.read_csv(tickerfile, sep=";", encoding='latin-1')


    # tickers=etfliste["TICKER"]
    # names=etfliste["TRUENAMES"]
    
    true_tickers=[]
    true_names = []
    true_industry = []
    true_sector = []
    true_marketCap=[]
    true_drawdown=[]
    true_drawdown_actual=[]
    shit_list = []
    last_close=[]
  
    
    ################### Anzahl Balken, also Handelstage !
    xxs = 5
    xs = 10
    s = 21
    m=50

    ll= StockscreenerPlotter_stats.ll
    kw = row["quelldatei"][:4]
    ####################################################
    ## HIer die Anzhal dr Kalendertage
    xxs_d = xxs + 2
    xs_d= xs + 4
    s_d = s + 8
    m_d = m + 20
    l_d = ll + 32
    
    
    
    Anz = 0
    shitflag = False
  
    enddatum = StockscreenerPlotter_stats.enddatum 
     
    #### End_date: Letztes Dtaum der Zeitreihe der Preise !
    end_date = datetime.date.today()
    end_date = end_date - datetime.timedelta(days=7*Anz)
    bis = end_date.strftime("%Y-%m-%d")
    
    #### Start_date: Start der Zeitreihe der Preise in der Vergangeheit
    dAll = l_d + 2 
    start_date =  end_date - datetime.timedelta(days=dAll)
    von = start_date.strftime("%Y-%m-%d")
    
    start_l = end_date - datetime.timedelta(days=l_d)
    if start_l.weekday() == 5:
        start_l=start_l -  datetime.timedelta(days=1)
    if start_l.weekday() == 6:
        start_l=start_l +  datetime.timedelta(days=1)
    
    start_m = end_date - datetime.timedelta(days=m_d)
    if start_m.weekday() == 5:
        start_m=start_m -  datetime.timedelta(days=1)
    if start_m.weekday() == 6:
        start_m=start_m +  datetime.timedelta(days=1)
        
    start_s = end_date - datetime.timedelta(days=s_d)
    if start_s.weekday() == 5:
        start_s=start_s -  datetime.timedelta(days=1)
    if start_s.weekday() == 6:
        start_s=start_s +  datetime.timedelta(days=1)
        
    start_xs = end_date - datetime.timedelta(days=xs_d)
    if start_xs.weekday() == 5:
        start_xs=start_xs -  datetime.timedelta(days=1)
    if start_xs.weekday() == 6:
        start_xs=start_xs +  datetime.timedelta(days=1)
        
    start_xxs = end_date - datetime.timedelta(days=xxs_d)
    if start_xxs.weekday() == 5:
        start_xxs=start_xxs -  datetime.timedelta(days=1)
    if start_xxs.weekday() == 6:
        start_xxs=start_xxs +  datetime.timedelta(days=1)
    
    all_dates = [start_l,start_m,start_s,start_xs,start_xxs]
    
    
    # in form von strings:
    
    
    
    Zeitstempel= bis + "__" + von

    
    returns_l = []
    returns_m = []
    returns_s = []
    returns_xs = []
    returns_xxs = []
    returns_all = []
    # S&P Index Returns
    
    counter =-1
    mypath = universe["tmpdatadir"][index]+"\\"
    onlyfiles = [f for f in listdir(mypath) if (isfile(join(mypath, f)) and not f.startswith("_"))]
    
    _ticker_names = pd.read_csv(mypath + "_ticker_names.csv",sep=";",index_col=0)

    for singleticker_file in list(_ticker_names["ticker"]):

        counter=counter+1
        ticker = singleticker_file
        singleticker_file = singleticker_file+".csv"
        # name des ETFs:
        # Download historical data as CSV for each stock (makes the process faster)
        sthwrong=True
       
     
        
        df = pd.read_csv(mypath  + singleticker_file,sep=";",decimal=',',parse_dates=True,index_col=0)
        #df = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))
        
        ########
        ###############
        ####################



        ### caculate max drawdown in perif
        factor_series = df["Factor"].cummax()
        dd2here = round(100*(df["Factor"] - factor_series)/factor_series,0)
        dd =dd2here.min()
        dd_actual=round(100*(df["Factor"][-1]-factor_series.max())/factor_series.max())



        #oo = yf.Ticker(ticker)
        print(ticker)
        name = _ticker_names["name"][_ticker_names["ticker"]==ticker].values[0]
        industry = _ticker_names["industry"][_ticker_names["ticker"]==ticker].values[0]
        sector= _ticker_names["sector"][_ticker_names["ticker"]==ticker].values[0]
        marketCap = _ticker_names["marketCap"][_ticker_names["ticker"]==ticker].values[0]
        LastClose = df["Close"][-1]
        #name = ticker
        
        """try:
            #print("name:", name)
            print(name)
            name = str(oo.info["longName"])
            #name = ticker
        except:
            print("oo Abruf fehler haft. Nehme NAme aus .csv: ", name)
         """
       
        ## Checke, ob genug taeglioch Datensaetze geladne wurdne, um geforderte Historei zu analysieren
        #long_date,middle_date, short_date,last_date = checkdate(df)
        true_tickers.append(ticker) 
        #true names benennt die ticker, die tatsaechlich Daten lieferten.
        true_names.append(name)    
        true_industry.append(industry)
        true_sector.append(sector)
        true_marketCap.append(marketCap)
        last_close.append(LastClose)
        true_drawdown.append(dd)
        true_drawdown_actual.append(dd_actual)
    
        # Calculating returns relative to the market (returns multiple)
        # fuer die letzen >>LaengeReturnHistorie<< Tage
        
        stock_return = df['Factor'][-1]
        
    
        returns_multiple = 100*round(stock_return-1.0, 4)
        returns_all.extend([returns_multiple])
        print (f'Ticker: {ticker}; Returns Multiple  last {dAll} Days: {returns_multiple:.2f} %\n')
        #df.to_csv(tmpdatafile + f'{ticker}.csv',sep=";",decimal=',', float_format='%.5f',)
        
        
        ## l
        #########################################
        a=df.truncate(before=start_l.strftime("%Y-%m-%d"))
        a['Percent Change'] = a['Close'].pct_change()
        a['Factor'] =  (a['Percent Change'] + 1).cumprod()
    
        stock_return = a['Factor'][-1]
        returns_multiple = 100*round(stock_return-1.0, 4)
        returns_l.extend([returns_multiple])
        print (f'Ticker: {ticker}; Returns Multiple  last {ll} TradeDays: {returns_multiple:.2f} %\n')
        
        
        
        
        ## m:
        #########################################
        a=df.truncate(before=start_m.strftime("%Y-%m-%d"))
        a['Percent Change'] = a['Close'].pct_change()
        a['Factor'] =  (a['Percent Change'] + 1).cumprod()
        



        stock_return = a['Factor'][-1]
        returns_multiple = 100*round(stock_return-1.0, 4)
        returns_m.extend([returns_multiple])
        print (f'Ticker: {ticker}; Returns Multiple  last {m} TradeDays: {returns_multiple:.2f} %\n')
        
        ## s
        ############################################
        a=df.truncate(before=start_s.strftime("%Y-%m-%d"))
        a['Percent Change'] = a['Close'].pct_change()
        a['Factor'] =  (a['Percent Change'] + 1).cumprod()
        
     
        stock_return = a['Factor'][-1]
        returns_multiple = 100*round(stock_return-1.0, 4)
        returns_s.extend([returns_multiple])
        print (f'Ticker: {ticker}; Returns Multiple  last {s} TradeDays: {returns_multiple:.2f} %\n')
        ##################################################################
        
        
        ## xs
        ############################################
        a=df.truncate(before=start_xs.strftime("%Y-%m-%d"))
        a['Percent Change'] = a['Close'].pct_change()
        a['Factor'] =  (a['Percent Change'] + 1).cumprod()
        
        stock_return = a['Factor'][-1]
        returns_multiple = 100*round(stock_return-1.0, 4)
        returns_xs.extend([returns_multiple])
        print (f'Ticker: {ticker}; Returns Multiple  last {xs} TradeDays: {returns_multiple:.2f} %\n')
        ##################################################################
        
        ## xxs
        ############################################
        a=df.truncate(before=start_xxs.strftime("%Y-%m-%d"))
        a['Percent Change'] = a['Close'].pct_change()
        a['Factor'] =  (a['Percent Change'] + 1).cumprod()
        
       
        stock_return = a['Factor'][-1]
        returns_multiple = 100*round(stock_return-1.0, 4)
        returns_xxs.extend([returns_multiple])
        print (f'Ticker: {ticker}; Returns Multiple  last {xxs} TradeDays: {returns_multiple} %\n')
        ##################################################################
    
        if ticker == "COK.DE":
            print("aaaah")
        #time.sleep(0.8)
         

    
    
    rs_df = pd.DataFrame(list(zip(true_tickers,returns_l,returns_m, returns_s, returns_xs, returns_xxs, true_names, true_industry, true_sector,true_marketCap,true_drawdown,true_drawdown_actual)),
                         columns=['Ticker',"return_"+str(ll),'return_'+str(m),'return_'+str(s),'return_'+str(xs),'return_'+str(xxs), 'Name',"Industry","Sector","marketCap","DrawDown","DrawDownActual"])
    rs_df['Rank'] = rs_df["return_"+str(m)].rank(pct=True) * 50 +rs_df['return_'+str(s)].rank(pct=True) * 30 + rs_df['return_'+str(s)].rank(pct=True) * 20
    rs_df = rs_df.sort_values(by=['Rank'],ascending=False)

    
    ##############################################################################################
    # Scheibe fuer alle Ticker die Statics raus (Namen, industrie , multiple, )     
    rs_df.to_csv(resfile + Zeitstempel+"_"+ str(dAll)+'d.csv',sep=";",decimal=',', float_format='%.5f', index=False)
    
    
    # Selektier die top zb 60% der Liste:
    #rs_df = rs_df[(rs_df.Rank >= rs_df.Rank.quantile(.60))]
    
    # Checking Minervini conditions of top 30% of stocks in given list
    rs_stocks = rs_df['Ticker']
    
    Names_2 = open(resfile + Zeitstempel+"_"+str(dAll)+'d_tkr.csv',newline='',mode="w")    
    for tk in rs_stocks:
           Names_2.write("XETR:"+tk+"\n")
    Names_2.close()
    
    
    ###############################################################################
    exportList = pd.DataFrame(columns=['ETF',str(ll)+"d", str(m)+"d",str(s)+"d",str(xs)+"d",str(xxs)+"d","from mean[sigma]","size last move[sigma]"
                                           , str(ll)+"d_rs",str(m)+"d_rs", str(s)+"d_rs"
                                           , str(ll)+"d_r",str(m)+"d_r" , str(s)+"d_r"
                                           , str(ll)+"d_s",str(m)+"d_s" , str(s)+"d_s"
                                           ,"Name","Industry","Sector","marketCap","rang","ranking"
                                           ]
                              )
    ##############################################################################
    
    
    for singleticker_file in list(_ticker_names["ticker"]):
        counter=counter+1
        
        ticker = singleticker_file
        singleticker_file = singleticker_file+".csv"

        industry = _ticker_names["industry"][_ticker_names["ticker"]==ticker].values[0]
        sector = _ticker_names["sector"][_ticker_names["ticker"]==ticker].values[0]
        marketCap = _ticker_names["marketCap"][_ticker_names["ticker"]==ticker].values[0]
        name = _ticker_names["name"][_ticker_names["ticker"]==ticker].values[0]
        try:
            reg_params = []
            for dts in all_dates:
                
                dates = [] 
                prices = []
                vondatum = dts.strftime("%Y-%m-%d") 
                bisdatum = end_date.strftime("%Y-%m-%d") 
                
                dates, prices = regression.get_data_II(tmpdatafile + f'{ticker}.csv', dates, prices,vondatum, bisdatum)
                if len(prices)>3:
                    slope,a,r_sq, rs = regression.regression_stats(dates,prices)
                else:
                    slope = 0
                    r_sq = 0.00000000001

                reg_params.append(slope)
                reg_params.append(r_sq)

                if dts == start_l:
                    dates_2plot = dates
                    prices_2plot = prices
                    rs_2plot = pow(rs, 0.5)
                
            #lese die returns aus den files aus.
            Name = rs_df["Name"][rs_df['Ticker']==ticker].tolist()[0]
            industry = rs_df["Industry"][rs_df['Ticker']==ticker].tolist()[0]
            sector = rs_df["Sector"][rs_df['Ticker']==ticker].tolist()[0]
            marketCap = rs_df["marketCap"][rs_df['Ticker']==ticker].tolist()[0]
            DrawDown =rs_df["DrawDown"][rs_df['Ticker']==ticker].tolist()[0]
            DrawDownActual =rs_df["DrawDownActual"][rs_df['Ticker']==ticker].tolist()[0]
          
            r_l = float(rs_df["return_"+str(ll)][rs_df['Ticker']==ticker])
            r_m = float(rs_df['return_'+str(m)][rs_df['Ticker']==ticker])
            r_s = float(rs_df['return_'+str(s)][rs_df['Ticker']==ticker])
            r_xs = float(rs_df['return_'+str(xs)][rs_df['Ticker']==ticker])
            r_xxs = float(rs_df['return_'+str(xxs)][rs_df['Ticker']==ticker])
            
            helferlein = pd.DataFrame(list(zip(prices)))
            mp = helferlein[0].mean(0)
            
            ll_r =reg_params[1]
            m_r = reg_params[3]
            s_r = reg_params[5]
                        
            ll_s =reg_params[0]
            m_s = reg_params[2]
            s_s = reg_params[4]
            
            ll_slopeXr = ll_r  * ll_s
            m_slopeXr =  m_r   * m_s
            s_slopeXr =  s_r   * s_s
            
            
            condition_1= (ll_s > 0 and m_s > 0 and  s_s > 0 )
            condition_2= (ll_r > 0.7 and m_r > 0.6 )

            condition_3= (s_s > 0)
  
            print(m_s)
           # exportList = exportList.append({'ETF': ticker ,str(ll)+"d": r_l, str(m)+"d": r_m,str(s)+"d": r_s,str(xs)+"d": r_xs,str(xxs)+"d": r_xxs, "Slope": slope, "R": r_sq, "r*s": r_sq*slope, "Name": Name}, ignore_index=True)
            #if ll_s> 0 and ll_r > 0.6:

            ####################
            ##### PLOT PLOT PLOT 
            ####################                
            # If all conditions above are true, add stock to exportList
            if(ll_s != 0 and ll_r != 0 ):
                frommean, lastmove = regression.show_plot(dates_2plot,prices_2plot,rs_2plot,str(Name) + "\n" + " r*s:" + str(int(100000*ll_slopeXr)) +  " r:" + str(round(ll_r,3)) + "  s[%]:" + str(round(100*250*ll_s,2)),str(int(100000*ll_slopeXr))+"_"+str(int(1000*ll_r))+"_"+ticker,plotfile)
                print (f"{ticker}:{name}:{industry} made it")
                #Names_2.write("XE TR"+ticker[:-3]+"\n")


            if 2>1:
            #exportiere nur, wenn 21 Tage slope positive ist !    
                exportList = exportList.append({'ETF': ticker 
                                                , str(ll)+"d": r_l, str(m)+"d": r_m,str(s)+"d": r_s,str(xs)+"d": r_xs,str(xxs)+"d": r_xxs
                                                , "from mean[sigma]": frommean 
                                                , "size last move[sigma]": lastmove
                                                , str(ll)+"d_rs":reg_params[1]*reg_params[0]
                                                , str(m)+"d_rs":reg_params[3]*reg_params[2]
                                                , str(s)+"d_rs":reg_params[5]*reg_params[4]
                                                
                                               , str(ll)+"d_r":reg_params[1]
                                               , str(m)+"d_r":reg_params[3]
                                               , str(s)+"d_r":reg_params[5]
                                               
                                               ,str(ll)+"d_s":reg_params[0]
                                               ,str(m)+"d_s":reg_params[2]
                                               ,str(s)+"d_s":reg_params[4] 
                                               , "Name": Name,"Industry": industry,"Sector": sector, "marketCap": marketCap,"DrawDown": DrawDown,"DrawDownActual": DrawDownActual}, ignore_index=True)
                
                print(f"{ticker}: slope {ll_s},  r_sq: {ll_r}, s*r: {ll_slopeXr}")
            #vamsList = vamsList.append({str(dAll)+"d_r":,str(dAll)+"d_s":, str(dLong)+"d_r":,str(dLong)+"d_s":,str(dMiddle)+"d_r":,str(dShort)+"d_s":})

        except Exception as e:
            print (e) 
    
    
    
    
    sort_final(exportList)
    exportList = exportList.sort_values(by='ranking', ascending=False)

         
        
    
    #print('\n', exportList)
    
    #writer = ExcelWriter(TickerSelector.pfad_results+Zeitstempel+"_"+"Regression_Perf.xlsx")
    #exportList.to_excel(writer, "Sheet1")
    #writer.save()
    
    exportList.to_csv(resfile + kw + Zeitstempel+".csv",sep=";",decimal=',', float_format='%.6f', index=False)
    exportList.to_csv(mypath + kw + "_result.csv",sep=";",decimal=',', float_format='%.6f', index=False)

    Names_2 = open(resfile + kw + Zeitstempel+"_tkr.csv",newline='',mode="w")    
    tks = exportList["ETF"]
    for tk in tks:
        Names_2.write("XETR:"+tk+"\n")
    Names_2.close()
    
    print("Done")
    ##call grafic module with data directory as path
    #downloader.main()
        
        
        
    
# if __name__ == "__main__":
#    # while True:    
#         main()
        
#         onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

#         time.sleep(1)         