# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 08:46:16 2021
 
@author: Schroeder
"""


# Liest ETF historien von yahoo finance aus und macth ein ranking.
#


import StockscreenerWinners_stats

###### Insert the following three lines to make any import lib in he project dir setup visible to an other
###### Directory in the project setup
import os
import sys
currentdir = os.path.abspath('')
parentdir = os.path.realpath(os.path.join(currentdir, '..'))
sys.path.insert(0, parentdir) 
#############################################################
#print(parentdir)
 
from datetime import datetime


# Imports
#from yahoo_fin import stock_info as si


import yfinance as yf
import pandas as pd
import datetime
import time
   
import stockDataGrabber_stats_v1
import my_setup
import logging


import os.path
import os 
import sys

import Indikatoren

currentdir = os.path.abspath('')
parentdir = os.path.realpath(os.path.join(currentdir, '..'))
sys.path.insert(0, parentdir) 

pfad = os.path.realpath(os.path.join(currentdir, 'ETFS'))
path = os.path.realpath(os.path.join(pfad, 'Mutterlisten'))

logpfad = os.path.realpath(os.path.join(parentdir, 'LOG'))

#lieferrt bei gegebenem datatfram mit datum als index das erste Datum, das letzte, und zwei 
# dazwischen 




def sort_final(liste):
    liste["rang"]= 0.1*liste[str(m)+"d_rs"]+0.9*liste[str(ll)+"d_rs"]
    liste["ranking"]=liste.rang.rank()



yf.pdr_override()

##########################################
##########################################
list_of_classes = ["styles","Indices","Laender","USSectors"]
##EUsektoren  USSectors SP500 europa Aristokraten Rohstoffe styles stylesbroad asiapacificeats 
## ,"EUsektoren","styles","Rohstoffe","europa","Laender","Indices","asiapacificeast","Aristokraten"
## AlleAnbieter AlleInternational macro MDAX Laender PrimeAllShare Deutschland500 AMERICA600 MyPort

   
for keyword in list_of_classes:     

        print("Grabbing for: ",keyword)       
        Univ = {'quellpfad':[path],
                    'quelldatei': [keyword], 
                    'plotdir':[os.path.realpath(os.path.join(pfad,"RES_"+keyword + "\\Plots\\"))],
                    'resdir':[ os.path.realpath(os.path.join(pfad,"RES_"+keyword + "\\Res\\"))],
                    'vamsdir':[os.path.realpath(os.path.join(pfad,"RES_"+keyword + "\\Vams\\"))],
                    'tmpdatadir':[os.path.realpath(os.path.join(pfad,"RES_"+keyword +  "\\Data\\"))],
                    }        
        universe = pd.DataFrame(Univ)

        if my_setup.logger == "On":
            fname = logpfad + "\\" + str(datetime.datetime.now().day)+ "--"+str(datetime.datetime.now().hour)+"-"+ str(datetime.datetime.now().minute)+".log"
            logging.basicConfig(filename=fname,
                                format="%(asctime)s %(message)s", 
                                datefmt="%m/%d %I:%M:%S %p", 
                            level=logging.INFO)  

        logging.info("Start DataGrabbing")
        for index, row in universe.iterrows():
            tickerfile = row["quellpfad"]+"\\" + row["quelldatei"]+".csv"
            plotfile = row["plotdir"]+"\\"
            resfile =  row["resdir"]+"\\"
            tmpdatafile = row["tmpdatadir"]+"\\"
            vamsfile = row["vamsdir"]+"\\"

            
            logging.info("Grabbing: "+row["quelldatei"])

            
            StockscreenerWinners_stats.cleardir(tmpdatafile)
            StockscreenerWinners_stats.cleardir(plotfile)

            etfliste = pd.DataFrame()
            etfliste = pd.read_csv(tickerfile, sep=";", encoding='latin-1')

            tickers=etfliste["TICKER"]
            names=etfliste["TRUENAMES"]
            
            true_tickers=[]
            true_names = []
            true_industry = []
            true_sector = []
            true_marketCap =[]
            shit_list = []
            
            
            ################### Anzahl Balken, also Handelstage !
            xxs = 5
            xs = 10
            s = 21
            m=50

            ll=stockDataGrabber_stats_v1.ll

            ####################################################
            ## HIer die Anzhal dr Kalendertage
            xxs_d = xxs + 2
            xs_d= xs + 4
            s_d = s + 8
            m_d = m + 20
            ### 80 BusinessTage sind 16 Wochen, also 16X2 TAge S,So dazu !
            l_d = ll + 32
            
            
            
            Anz = -1 
            shitflag = False
            while Anz <  stockDataGrabber_stats_v1.Anzahl:
                Anz=Anz+1
                #print("################################")
                #print("Anzhal Wochen: ", Anz)
                #print("################################")
                enddatum = stockDataGrabber_stats_v1.enddatum 
                
            
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
                
                ##all_dates = [start_l,start_m,start_s,start_xs,start_xxs]
                
                
                # in form von strings:
                
                
                
                Zeitstempel= bis + "__" + von
                
            
                
                
            
                # S&P Index Returns
                
                counter =-1
            
                for ticker in tickers:
                    df = pd.DataFrame()
                    counter=counter+1
                    
                    # name des ETFs:
                    # Download historical data as CSV for each stock (makes the process faster)
                    sthwrong=True
                
                    time.sleep(0.2)
                    try:
                        oo = yf.Ticker(ticker)
                    except:
                        print(f"{ticker}, {name}: Geht garnix !!!")
                
                #   df = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))
                    try:
                        name = names[counter]
                        df = oo.history(period=stockDataGrabber_stats_v1.periode)    
                    except:
                        print(f"{ticker}, {name}: korrupt. Keine History")
                    try:
                        #print("name:", name)
                        print(oo.info["longName"])
                        name = oo.info["longName"]
                    except:
                        print(f"{ticker}: korrupt. Kein Longname")
                    try:
                            industry = oo.info["industry"]
                            sector = oo.info["sector"]
                            marketCap = int(oo.info["marketCap"]/1000000000)
                    except:
                            industry="ETF"    
                            sector = "sector"
                            marketCap=1
                    
                    if (len(df) < ll - 8) or ((end_date -  df.index[-1].date()).days > 3 ):
                        l = len(df)
                        if l>0 :
                            dt = str((end_date - df.index[-1].date()).days)
                        else:
                            dt = "NaN"
                        print(ticker, " : On shit_list !" )
                        print("date: "+ str(end_date) + " Anzahl Tage:"+str(l)+" dt:"+dt+" | "+str( name)+"\n")
                        shit_list.append(ticker+":"+" Anzahl Tage:"+str(l)+" dt:"+dt+" | "+str(name))
                    
                    if (len(df) >= ll - 8) and ((end_date - df.index[-1].date()).days <= 3 ):
                        ## Checke, ob genug taeglioch Datensaetze geladne wurdne, um geforderte Historei zu analysieren
                        #long_date,middle_date, short_date,last_date = checkdate(df)
                        true_tickers.append(ticker) 
                        #tbiontrue names benennt die ticker, die tatsaechlich Daten lieferten.
                        true_names.append(name)  
                        true_industry.append(industry)  
                        true_sector.append(sector)
                        true_marketCap.append(marketCap)
                    
                        # Calculating returns relative to the market (returns multiple)
                        # fuer die letzen >>LaengeReturnHistorie<< Tage
                        df['Percent Change'] = df['Close'].pct_change()
                        df['Factor'] =  (df['Percent Change'] + 1).cumprod()
                        
                        stock_return = df['Factor'][-1]

                        df=Indikatoren.ATR(df,20)
                        df["EMA50"]=df["Factor"].ewm(span=50,adjust=False).mean()
                        df["EMA80"]=df["Factor"].ewm(span=80,adjust=False).mean()
                        df["EMA10"]=df["Factor"].ewm(span=10,adjust=False).mean()
                        df["EMA21"]=df["Factor"].ewm(span=21,adjust=False).mean()
                        df["EMA100"]=df["Factor"].ewm(span=100,adjust=False).mean()
                        df["EMA200"]=df["Factor"].ewm(span=200,adjust=False).mean()
                        

                        Indikatoren.MACD(df, 12, 26,9,"_day")
                        Indikatoren.MACD(df, 60, 130,45,"_week")       


                        returns_multiple = 100*round(stock_return-1.0, 4)
                        print (f'Ticker: {ticker}; Returns Multiple: {returns_multiple:.2f} %\n')
                        df.to_csv(tmpdatafile + f'{ticker}.csv',sep=";",decimal=',', float_format='%.5f',)               
                    ## schreibe Ticker und die Longnames raus !
                    _ticker_names = pd.DataFrame(list(zip(true_tickers,true_names,true_industry,true_sector,true_marketCap)),
                                    columns=['ticker','name','industry',"sector","marketCap"])
                    _ticker_names = _ticker_names.sort_values("ticker")               
                    _ticker_names.to_csv(tmpdatafile + "_ticker_names.csv",sep=";")  
                
                if shitflag==False:
                    shitflag = True    
                    shit_file = open(resfile+"_shit"+'.csv','w')
                    for item in shit_list:
                        shit_file.write(item+"\n")
                    shit_file.close()    

print("Done")