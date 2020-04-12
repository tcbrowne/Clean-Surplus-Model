import numpy as np
import sympy as sy
import matplotlib as mpl
from sympy.stats import Normal, cdf
from sympy import init_printing
from matplotlib import pyplot as plt
from joblib import Parallel, delayed
import multiprocessing
import yfinance as yf
import pandas as pd
import csv
import pyodbc
init_printing()


#Connect to database
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Taylor\Documents\SurplusModel.accdb;')
cursor = conn.cursor()

#Pull S&P tickers to run this script recurring - THIS IS NEW, TO REMOVE
data_tick = pd.read_csv (r'C:\Users\Taylor\Desktop\Python Projects\ticker_info.csv')
data = pd.read_csv (r'C:\Users\Taylor\Desktop\Python Projects\ticker_info.csv')   
ticker_list = data['Symbol'].tolist()
#print(ticker_list)

#Define dictionary for all share values
valueDict = dict([("Ticker", "Valuation")])

#Define Functions
Book_Values = []

def fun(currentyear, finalyear, BVpy, pytrt, vROE):
    BVcy = BVpy*(1+((1-pytrt)*vROE))
    #Book_Values.append((BVcy, currentyear))
    Book_Values.append(float(BVcy))
    if currentyear == finalyear:
        return Book_Values
    else:
        return fun(currentyear+1, finalyear, BVcy, pytrt, vROE)

def some(voxvalues, Kc):
    temp = []
    n = 1
    for i in voxvalues:
        temp.append(i/((1+Kc)**(n)))
        n = n+1
    return temp

def ValuationStatement(currentprice, intrinsicprice, ValueComparison):
    if currentprice -  intrinsicprice >= 0:
        statement = "Shares overvalued by {}".format(ValueComparison)
    elif currentprice - intrinsicprice <= 0:
        statement = "Shares undervalued by {}".format(ValueComparison)
    
    return statement

def processInput(tickerIndex):
    try:
        ticker = tickerIndex
        tkr = yf.Ticker(ticker)
        Bta = tkr.info['beta']
        curr_share_value = tkr.info['regularMarketPrice']
        numshares = tkr.info['sharesOutstanding']

        netincome = tkr.financials.loc['Net Income',:].tolist()
        byNI = netincome[0]

        bookvalue1 = tkr.balancesheet.loc['Total Stockholder Equity',:].tolist()
        byBV = bookvalue1[0]
        pyBV = bookvalue1[1]

        divy = tkr.dividends.tolist()
        byDivtemp = divy.reverse()
        byDivtemp = divy[0:4]
        byDiv = (sum(byDivtemp) * numshares)

        vROE = byNI / ((byBV + pyBV) / 2)

        by = 2019
        py = by - 1
        pytrt = byDiv / byNI
        vROElen = 7

        vRf = 0.0245
        vMRP = 0.056

        Kc = (vRf * (1 - Bta)) + (Bta*vMRP)

        Book_Values.insert(0,byBV)
        vOX_Values = [i * (vROE - Kc) for i in Book_Values]

        vPA = byBV + sum(some(vOX_Values, Kc))

        Share_Value = vPA / numshares

        ValueComparison = abs((curr_share_value - Share_Value))

        valueDict.update([(ticker, ValuationStatement(curr_share_value, Share_Value, ValueComparison))]) #update to diciontary

        #Below writes to excel
        with open('over_under_valuation_Test.csv', 'w') as f:
            for key in valueDict.keys():
                f.write("%s,%s\n"%(key,valueDict[key]))

        print(ValueComparison)
    except:
        return print("Index Error when attempting to retrieve {} from Yahoo Finance".format(tickerIndex))

#Parallel processing
num_cores = multiprocessing.cpu_count()

results = Parallel(n_jobs=num_cores)(delayed(processInput)(tickerIndex) for tickerIndex in ticker_list)
