# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 13:21:14 2021

@author: Schroeder
"""
#https:\\\\www.dividendenadel.de\\indexmonitor-maerz-2021\\
#zykliker: Chemie , rohstoofe (spaet im zyklus)Bauträger, Maschiennebau, REITS, Banken, Versicheurngen, Autobauer, ReisenHotels, Kreuztfahreten
#Antizyklishc\\Defneisv: telekom, nestle, Metro,

###### Insert the following three lines to make any import lib in he project dir setup visible to an other
###### Directory in the project setup
import os
import sys
currentdir = os.path.abspath('')
parentdir = os.path.realpath(os.path.join(currentdir, '..'))
sys.path.insert(0, parentdir) 
#############################################################

from MomentumScreening import my_setup
###
### The whole \\ETFS\\ Tree has to be located on ame level as repository !
pfad = os.path.realpath(os.path.join(parentdir, 'ETFS'))

##########################################################################

path = os.path.realpath(os.path.join(pfad, 'Mutterlisten'))

Universe = {'quellpfad':[  path,
                           path,
                           path,
                           path,
                           path,
                           path,
                           path,
                           path,
                           path,
                           path,
                           path],
                        #    path,
                        #    path] ,
             'quelldatei': [ 'SP500', 
                             'USSectors',
                             'Rohstoffe',
                             'europa',
                             'asiapacificeast',
                             "PrimeAllShare",
                             "styles",
                             "Aristokraten",
                             "EUsektoren",
                             "Deutschland500",
                             "MyPortfolio"],
                            #  'AlleAnbieter',
                            #  'AlleInternational'], 
             'plotdir':[os.path.realpath(os.path.join(pfad,"RES_SP500\\Plots\\")),
                        os.path.realpath(os.path.join(pfad,"RES_USSectors\\Plots\\")),
                        os.path.realpath(os.path.join(pfad,"RES_Rohstoffe\\Plots\\")),
                        os.path.realpath(os.path.join(pfad,"RES_europa\\Plots\\")),
                        os.path.realpath(os.path.join(pfad,"RES_asiapacificeast\\Plots\\")),
                        os.path.realpath(os.path.join(pfad,"RES_PrimeAllShare\\Plots\\")),
                        os.path.realpath(os.path.join(pfad,"RES_styles\\Plots\\")),
                        # my_setup.path+"ETFS\\RES_styles\\Plots\\",
                        os.path.realpath(os.path.join(pfad,"RES_Aristokraten\\Plots\\")),
                        os.path.realpath(os.path.join(pfad,"RES_EUsektoren\\Plots\\")),
                        os.path.realpath(os.path.join(pfad,"RES_Deutschland500\\Plots\\")),
                        os.path.realpath(os.path.join(pfad,"RES_MyPortfolio\\Plots\\"))],
                        # my_setup.path+"ETFS\\RES_AMERICA600\\Plots\\",           
                        # my_setup.path+"ETFS\\RES_AlleAnbieter\\Plots\\",
                        # my_setup.path+"ETFS\\RES_AlleInternational\\Plots\\"],
             'resdir':[ os.path.realpath(os.path.join(pfad,"RES_SP500\\Res\\")),
                        os.path.realpath(os.path.join(pfad,"RES_USSectors\\Res\\")),
                        os.path.realpath(os.path.join(pfad,"RES_Rohstoffe\\Res\\")),
                        os.path.realpath(os.path.join(pfad,"RES_europa\\Res\\")),
                        os.path.realpath(os.path.join(pfad,"RES_asiapacificeast\\Res\\")),
                        os.path.realpath(os.path.join(pfad,"RES_PrimeAllShare\\Res\\")),
                        os.path.realpath(os.path.join(pfad,"RES_styles\\Res\\")),
                        # my_setup.path+"ETFS\\RES_styles\\Res\\",
                        os.path.realpath(os.path.join(pfad,"RES_Aristokraten\\Res\\")),
                        os.path.realpath(os.path.join(pfad,"RES_EUsektoren\\Res\\")),
                        os.path.realpath(os.path.join(pfad,"RES_Deutschland500\\Res\\")),
                        os.path.realpath(os.path.join(pfad,"RES_MyPortfolio\\Res\\"))],
                        # my_setup.path+"ETFS\\RES_AMERICA600\\Res\\",
                        # my_setup.path+"ETFS\\RES_AlleAnbieter\\Res\\",
                        # my_setup.path+"ETFS\\RES_AlleInternational\\Res\\"],
             'vamsdir':[os.path.realpath(os.path.join(pfad,"RES_SP500\\Vams\\")),
                       os.path.realpath(os.path.join(pfad,"RES_USSectors\\Vams\\")),
                       os.path.realpath(os.path.join(pfad,"RES_Rohstoffe\\Vams\\")),
                       os.path.realpath(os.path.join(pfad,"RES_europa\\Vams\\")),
                       os.path.realpath(os.path.join(pfad,"RES_asiapacificeast\\Vams\\")),
                       os.path.realpath(os.path.join(pfad,"RES_PrimeAllShare\\Vams\\")),
                       os.path.realpath(os.path.join(pfad,"RES_styles\\Vams\\")),
                    #    my_setup.path+"ETFS\\RES_styles\\Vams\\",
                       os.path.realpath(os.path.join(pfad,"RES_Aristokraten\\Vams\\")),
                       os.path.realpath(os.path.join(pfad,"RES_EUsektoren\\Vams\\")),
                       os.path.realpath(os.path.join(pfad,"RES_Deutschland500\\Vams\\")),
                       os.path.realpath(os.path.join(pfad,"RES_MyPortfolio\\Vams\\"))],
                    #    my_setup.path+"ETFS\\RES_AMERICA600\\Vams\\",
                    #    my_setup.path+"ETFS\\RES_AlleAnbieter\\Vams\\",
                    #    my_setup.path+"ETFS\\RES_AlleInternational\\Vams\\"],
            'tmpdatadir':[os.path.realpath(os.path.join(pfad,"RES_SP500\\Data\\")),
                       os.path.realpath(os.path.join(pfad,"RES_USSectors\\Data\\")),
                       os.path.realpath(os.path.join(pfad,"RES_Rohstoffe\\Data\\")),
                       os.path.realpath(os.path.join(pfad,"RES_europa\\Data\\")),
                       os.path.realpath(os.path.join(pfad,"RES_asiapacificeast\\Data\\")),
                       os.path.realpath(os.path.join(pfad,"RES_PrimeAllShare\\Data\\")),
                       os.path.realpath(os.path.join(pfad,"RES_styles\\Data\\")),
                    #    my_setup.path+"ETFS\\RES_styles\\Data\\",
                       os.path.realpath(os.path.join(pfad,"RES_Aristokraten\\Data\\")),
                       os.path.realpath(os.path.join(pfad,"RES_EUsektoren\\Data\\")),
                       os.path.realpath(os.path.join(pfad,"RES_Deutschland500\\Data\\")),
                       os.path.realpath(os.path.join(pfad,"RES_MyPortfolio\\Data\\"))],
                    #    my_setup.path+"ETFS\\RES_AMERICA600\\Data\\",
                    #    my_setup.path+"ETFS\\RES_AlleAnbieter\\Data\\",
                    #    my_setup.path+"ETFS\\RES_AlleInternational\\Data\\"]   
            }


################################################################################################################
# EUsektoren  USSectors fx Indices SP500 europa Aristokraten Rohstoffe styles stylesbroad asiapacificeats 
# AlleAnbieter AlleInternational macro MDAX Laender PrimeAllShare Deutschland500 AMERICA600 MyPortfolio 
#################################################################################################################

keyword = "MyPortfolio"

# Universe = {'quellpfad':[path],
#             'quelldatei': [keyword], 
#             'plotdir':[os.path.realpath(os.path.join(pfad,"RES_"+keyword + "\\Plots\\"))],
#             'resdir':[ os.path.realpath(os.path.join(pfad,"RES_"+keyword + "\\Res\\"))],
#             'vamsdir':[os.path.realpath(os.path.join(pfad,"RES_"+keyword + "\\Vams\\"))],
#             'tmpdatadir':[os.path.realpath(os.path.join(pfad,"RES_"+keyword +  "\\Data\\"))],
#             } 
        
enddatum=my_setup.enddatum 
Anzahl = 0 

if 2>1:
    periode = "15y"
    ll=500
else:
    periode = "12mo"
    ll=80


for pdir in Universe["plotdir"]:
   os.makedirs(pdir,exist_ok=True)
for pdir in Universe["tmpdatadir"]:
   os.makedirs(pdir,exist_ok=True)   
for pdir in Universe["resdir"]:
   os.makedirs(pdir,exist_ok=True)
for pdir in Universe["vamsdir"]:
   os.makedirs(pdir,exist_ok=True)
os.makedirs(pfad+"//Analyse_data",exist_ok=True)
os.makedirs(parentdir+"//LOG",exist_ok=True)
os.makedirs(parentdir+"//ETFS",exist_ok=True)
