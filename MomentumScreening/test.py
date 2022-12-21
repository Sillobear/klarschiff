import os
import sys
import os.path
import yfinance as yf

yf.pdr_override()
currentdir = os.path.abspath('') 
parentdir = os.path.realpath(os.path.join(currentdir, '..'))
sys.path.insert(0, parentdir) #Inserts parentdir path to list of accesable path for interpreters

print("Currentdir: ",currentdir)
print("Parentdir: ",parentdir)

import StockscreenerWinners_stats
# from fileLib import Indikatoren
from datetime import datetime
import pandas as pd
import datetime
import time
# import stockDataGrabber_stats_v1
import my_setup
import logging


etfsPfad = os.path.realpath(os.path.join(parentdir, 'ETFS')) 
mutterlistenPfad = os.path.realpath(os.path.join(etfsPfad, 'Mutterlisten'))

logpfad = os.path.realpath(os.path.join(parentdir, 'LOG'))

list_of_classes = ["styles","Indices","Laender","USSectors"]

   
for indClass in list_of_classes:     #indikator Klassen Iterator

        print("Grabbing for: ",indClass)       
        Univ = {'quellpfad':[mutterlistenPfad],
                    'quelldatei': [indClass], 
                    'plotdir':[os.path.realpath(os.path.join(etfsPfad,"RES_"+indClass + "\\Plots\\"))],
                    'resdir':[ os.path.realpath(os.path.join(etfsPfad,"RES_"+indClass + "\\Res\\"))],
                    'vamsdir':[os.path.realpath(os.path.join(etfsPfad,"RES_"+indClass + "\\Vams\\"))],
                    'tmpdatadir':[os.path.realpath(os.path.join(etfsPfad,"RES_"+indClass +  "\\Data\\"))],
                    }        
        universe = pd.DataFrame(Univ)
        