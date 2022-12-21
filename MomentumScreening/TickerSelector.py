# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 14:58:33 2020

@author: Schroeder
"""

pfad_src = ".data/ETFS/ETFsrc/"
pfad_MutterListen = ".data/ETFS/Mutterlisten/"
pfad_tmpData=".data/ETFS/tmpData/"
pfad_tmpPlots=".data/ETFS/tmpData/Plots/"
pfad_vams=".data/ETFS/results/VAMS/"
pfad_results=".data/ETFS/results/"
pfad_python = ".data/ETFS/python/"
pfad_TickerListen = ".data/ETFS/Tickerlisten/"

name = "Communication"

import pandas as pd
import re
import os
import csv

import yfinance as yf

#  [match.start() for match in re.finditer(",", s)]
# Out[5]: [6, 19, 31, 36, 40, 44, 50, 69, 99, 101, 103]

# a=[match.start() for match in re.finditer(",", s)]


#wenn ticker an sechster komma stellekommt : 
#ticker =s[a[len(a)-6-1]+1:a[len(a)-6]]
# a
# Out[7]: [6, 19, 31, 36, 40, 44, 50, 69, 99, 101, 103]

# s[a[2]]
# Out[8]: ','

# s[a[3]]
# Out[9]: ','

# s[a[3]:a[4]]
# Out[10]: ',01"'

# s[a[4]]
# Out[11]: ','





muster = re.compile("\"[\w\s]*\"")

ishares = re.compile(".*ISHARES.*|.*ISHRS.*|.*ISHS.*|.*ISHSI.*|.*ISIV.*|.*I-SHAR.*")

banks = re.compile(".*Bank.*|.*Financ.*")
dividends = re.compile(".*Divid.*|.*divid.*")
inflation = re.compile(".*Inflat.*|.*inflat.*")

etf = re.compile("EXCHANGE")
stock = re.compile("AKTIE")


start_anf = "^\""
doppelt = " \"\" "


def splitter(filen,ext,tickercolumn,namecolumn): 
    etf_csv = open(pfad_MutterListen + filen,newline='',mode="r")
    csv_f = csv.reader(etf_csv)
    
    tickerliste=[]
    nameliste=[]
    counter = 1
    marker = 2
    
    for row in csv_f:
        print(row)
        pair=[]
        aa = row[0][1:-1]
        row_neu = aa.split(";")
        name =row_neu[namecolumn]
        #print("--------------------------\n")
        #print(aa+"\n")
        ticker = row_neu[tickercolumn]+ext
        tickerliste.append(ticker)
        nameliste.append(name)
        
        
        # print(ticker + " " + name+ "\n ")
        # msft = yf.Ticker(ticker)
        # data =msft.history(period="100d")
        # if len(data) > 1 :
        #     print(data["Close"].iloc[-1])
        #     print("\n")
    return tickerliste, nameliste



def ETFDtBoerse(filen,ext): 
    etf_csv = open(pfad_MutterListen + filen,newline='',mode="r")
    csv_f = csv.reader(etf_csv,delimiter=',')
    
    tickerliste=[]
    nameliste=[]
    counter = 1
    marker = 2
    
    for row in csv_f:
        print(row)
        pair=[]
        aa = row[0][1:-1]
        row_neu = aa.split(";")
        name =row_neu[2]
        #print("--------------------------\n")
        #print(aa+"\n")
        ticker = row_neu[5]#+ext
        tickerliste.append(ticker)
        nameliste.append(name)
        
        
        # print(ticker + " " + name+ "\n ")
        # msft = yf.Ticker(ticker)
        # data =msft.history(period="100d")
        # if len(data) > 1 :
        #     print(data["Close"].iloc[-1])
        #     print("\n")
    return tickerliste, nameliste


def ETFDtBoerse_trial(): 
    etf_csv = open(pfad_MutterListen + "ETFsDtBoerse - Kopie",newline='',mode="r")
    csv_f = csv.reader(etf_csv)
    tickerliste=[]
   
    counter = 1
    marker = 2
    for row in csv_f:
        aa = row[0][1:-1]
        row_neu = aa.split(";")
        name =row_neu[2]
        print("--------------------------\n")
        print(aa+"\n")
        ticker = row_neu[5]+".DE"
        tickerliste.append(ticker)
        
        print(ticker + " " + name+ "\n ")
        msft = yf.Ticker(ticker)
        data =msft.history(period="100d")
        if len(data) > 1 :
            print(data["Close"])
            print("\n")
    return tickerliste    




def stocketf_out(): 
    stock_csv = open(pfad_MutterListen + "LS_stock.csv",newline='',mode="r")
    etf_csv  = open(pfad_MutterListen + "LS_ETF.csv",newline='',mode="r")
  
    
    name = "LS_stock_kuerzel"
    stock_kuerzel = open(pfad_MutterListen + name + ".csv",newline='',mode="w")
    etf_kuerzel  = open(pfad_MutterListen + "LS_ETF_kuerzel.csv",newline='',mode="w")
                
                    
    stock_writer = csv.writer(stock_kuerzel)
    etf_writer = csv.writer(etf_kuerzel)
    
    #print(arr)
    etf_row=[]
    stock_row=[]
    
    csv_f = csv.reader(stock_csv)
    counter = 1
    marker = 2
    for row in csv_f:
        
        if row[5]== "AKTIE":
            #stock_kuerzel.write("XETR:"+row[4]+"\n")
            stock_kuerzel.write("SWB:"+row[4]+"\n")
        counter = counter + 1
        if counter > 988:
            stock_kuerzel.close()
            name_neu = name+str(marker)
            stock_kuerzel = open(pfad_MutterListen + name_neu + ".csv",newline='',mode="w")
            counter = 1
            marker=marker+1
            
        
        print(row[4])
        
    csv_f = csv.reader(etf_csv)
    for row in csv_f:    
        if row[5] == "EXCHANGE":
            if re.match(ishares,row[2]):
                etf_kuerzel.write("SWB:"+row[4]+"\n")
                etf_kuerzel.write("XETR:"+row[4]+"\n")
        print(row[4])


def inflationetf_out(): 
    
    etf_csv  = open(pfad_MutterListen + "ETFsDtBoerse.csv",newline='',mode="r")
  
    
    etf_ticker  = open(pfad_TickerListen + "Inflation_ETF_ticker.csv",newline='',mode="w")
    etf_list  = open(pfad_MutterListen + "DtBoerseListen/Inflation_ETF_liste.csv",newline='',mode="w")
                
                    
   
    #print(arr)
    etf_row=[]
    
    
    
    counter = 1
    marker = 2
        
    csv_f = csv.reader(etf_csv)
    for row in csv_f:
            row_neu = row[0].split(";")
            if re.match(inflation,row_neu[2]):
                etf_ticker.write("XETR:"+row_neu[5]+"\n")
                etf_list.write(row[0]+"\n")
                print(row_neu[2])

    etf_ticker.close()
    etf_list.close()



def dividendsetf_out(): 
    
    etf_csv  = open(pfad_MutterListen + "ETFsDtBoerse.csv",newline='',mode="r")
  
    
    etf_ticker  = open(pfad_TickerListen + "Dividend_ETF_ticker.csv",newline='',mode="w")
    etf_list  = open(pfad_MutterListen + "DtBoerseListen/Dividend_ETF_liste.csv",newline='',mode="w")
                
                    
   
    #print(arr)
    etf_row=[]
    
    
    
    counter = 1
    marker = 2
        
    csv_f = csv.reader(etf_csv)
    for row in csv_f:
            row_neu = row[0].split(";")
            if re.match(dividends,row_neu[2]):
                etf_ticker.write("XETR:"+row_neu[5]+"\n")
                etf_list.write(row[0]+"\n")
                print(row_neu[2])

    etf_ticker.close()
    etf_list.close()


def banketf_out(): 
    
    etf_csv  = open(pfad_src + "ETFsDtBoerse.csv",newline='',mode="r")
  
    
    etf_ticker  = open(pfad_TickerListen + "Bank_ETF_ticker.csv",newline='',mode="w")
    etf_list  = open(pfad_MutterListen + "DtBoerseListen/Bank_ETF_liste.csv",newline='',mode="w")
                
                    
   
    #print(arr)
    etf_row=[]
    
    
    
    counter = 1
    marker = 2
        
    csv_f = csv.reader(etf_csv)
    for row in csv_f:
            row_neu = row[0].split(";")
            if re.match(banks,row_neu[2]):
                etf_ticker.write("XETR:"+row_neu[5]+"\n")
                etf_list.write(row[0]+"\n")
                print(row_neu[2])

    etf_ticker.close()
    etf_list.close()
    

def stocketfcrash(): 
    arr = os.listdir(pfad_src)
    stock_csv = open(pfad_MutterListen + "LS_stock.csv",newline='',mode="w")
    etf_csv  = open(pfad_MutterListen + "LS_ETF.csv",newline='',mode="w")
    crsh_csv  = open(pfad_MutterListen + "LS_CRASH.csv",newline='',mode="w")
    
    stock_writer = csv.writer(stock_csv)
    etf_writer = csv.writer(etf_csv)
    crash_writer = csv.writer(crsh_csv)
    
    #print(arr)
    etf_row=[]
    stock_row=[]
    
    for f in arr:
        f = open(pfad_src+str(f))
        csv_f = csv.reader(f)
        for row in csv_f:
            if len(row)==1:
                crash_writer.writerow(row) 
            elif row[0]=="":
                a=1
            elif row[0]=="WKN":   
                a=1
            elif row[5]== "AKTIE":
                stock_writer.writerow(row)
            elif row[5] == "EXCHANGE":
                etf_writer.writerow(row)
            print(row)
    
        
        # print(f)
        # read_file = pd.read_excel(pfad_src+str(f))
        # name = str(str(f)[:-5])
        # read_file[["Symbol"]].to_csv (pfad_MutterListe + name+".txt", sep = ",", index = None, header=False)
    
def browse_Crash():
    crsh_csv  = open(pfad_MutterListen + "LS_CRASH.csv",newline='',mode="r")
    csv_f = csv.reader(crsh_csv)
    stock_2 = open(pfad_MutterListen + "LS_stock2.csv",newline='',mode="w")
    stock_writer = csv.writer(stock_2)
    for row in csv_f:
        print
        print(row[0])
        aa = row[0][1:-1]
        a=aa.replace("-,","##")
        b=a.replace("100,000","100.000")
        c=b.replace("1,000","1.000")
        c = re.sub(r"\"[\w\s]*.*,*[\w\s]*\"","QQQQ",row[0])
        row_neu = c.split(",")
        stock_writer.writerow(row_neu)
        print(c)
        print(row_neu)              
        
        
    
    
        
    



def browse_Kuerzel():
    stock_csv = open(pfad_MutterListen + "LS_stock.csv",newline='',mode="r")
    etf_csv  = open(pfad_MutterListen + "LS_ETF.csv",newline='',mode="r")
    crsh_csv  = open(pfad_MutterListen + "LS_CRASH.csv",newline='',mode="r")

    stock = open(pfad_MutterListen + "STOCK.csv",newline='',mode="w")
    etf  = open(pfad_MutterListen + "ETF.csv",newline='',mode="w")
    crsh  = open(pfad_MutterListen + "LS_CRASH.csv",newline='',mode="w")



if __name__ == "__main__":
    #while True:    
        #stocketfcrash()
        #browse_Crash()
        inflationetf_out()    
        #dividendsetf_out()
        #banketf_out()    
        #ETFDtBoerse_trial()
        #browse_Kuerzel()
        
        #time.sleep(30)