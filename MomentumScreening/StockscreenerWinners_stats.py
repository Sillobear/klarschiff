# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 13:21:14 2021

@author: Schroeder
"""
#####
from os import listdir
from os.path import isfile, join
import os


#https://www.dividendenadel.de/indexmonitor-maerz-2021/
#zykliker: Chemie , rohstoofe (spaet im zyklus)Bauträger, Maschiennebau, REITS, Banken, Versicheurngen, Autobauer, ReisenHotels, Kreuztfahreten
#Antizyklishc/Defneisv: telekom, nestle, Metro,



def cleardir(pfad):
    onlyfiles = [f for f in listdir(pfad) if isfile(join(pfad, f))]
    for ticker in onlyfiles:
        os.remove(join(pfad, ticker))
