# -*- coding: utf-8 -*-
"""
Spyder Editor

This module is for Scalp M16 Trade analytics

"""
import pandas as pd
import datetime as dt
import os


folder_path = 'G://andyvoid//projects//andyvoid_tools//options_rifle//database//virtual_trades_logs'  # Replace with the path to your folder
files = os.listdir(folder_path)
tradesDf = None
dfList = []
for file in files:
    filepath = folder_path + "//" + file
    df1 = pd.read_csv(filepath)
    #print(df1)
    
    #dfList.append(df1)
    
#df = pd.concat(dfList)
    








        
    
