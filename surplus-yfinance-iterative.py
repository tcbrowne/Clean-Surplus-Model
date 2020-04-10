import numpy as np
import scipy.stats as si
import sympy as sy
import matplotlib as mpl
from sympy.stats import Normal, cdf
from sympy import init_printing
from matplotlib import pyplot as plt
import yfinance as yf
import pandas as pd
import csv
init_printing()


#Pull S&P tickers to run this script recurring
data_tick = pd.read_csv (r'/path') #Update based on where you dropped CSV
data = pd.read_csv (r'/path') #Update based on where you dropped CSV
ticker_list = data['Symbol'].tolist()

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

#loop the tickers specified and pulling with API from yFinance

for tickerIndex in ticker_list:
    try:
        ticker = tickerIndex #str(input("ticker symbol: ")) #example: MSFT
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

        by = 2019 #by = int(input("Base Year: ")) i.e., year zero
        py = by - 1 #previous year (base year - 1)
        pytrt = byDiv / byNI #payout ratio defined as Dividend (base year) / NI (base year) #assume will continue for seven years
        vROElen = 7 #vROElen = float(input("Number of years ROE is expected to persist (i.e., Horizon): ")) #after which ROE will equal cost of capital

        vRf = 0.0245 #these will not fluctuate much - but should be updated on occasion (pre-populated)
        vMRP = 0.056 #these will not fluctuate much - but should be updated on occasiono (pre-populated)

        Kc = (vRf * (1 - Bta)) + (Bta*vMRP)

        #print("Recursive Book Values calculated for Year {} to Year {}".format(by+1,int(by+vROElen - 1)))        
        #print(fun(by + 1, by + vROElen - 1, byBV, pytrt, vROE))

        Book_Values.insert(0,byBV)
        vOX_Values = [i * (vROE - Kc) for i in Book_Values]

        #print("Abnormal Earnings for Year {} to Year {}".format(by+1,int(by + vROElen)))
        #print(vOX_Values)

        #print("Discounted Abnormal Earnings for Year {} to Year {}".format(by+1, int(by + vROElen)))
        #print(some(vOX_Values, Kc))
        
        #print("Sum of Total Abnormal Earnings for Year {} to Year {}".format(by+1, int(by + vROElen)))
        #print(sum(some(vOX_Values, Kc)))

        vPA = byBV + sum(some(vOX_Values, Kc))

        Share_Value = vPA / numshares

        #print("Valuation of Shares as of {} Year-End".format(by))
        #print(Share_Value)
        
        ValueComparison = abs((curr_share_value - Share_Value))

        #print(ValuationStatement(curr_share_value, Share_Value, ValueComparison))

        valueDict.update([(ticker, ValuationStatement(curr_share_value, Share_Value, ValueComparison))])
        #print(valueDict)
    except:
        print("Index Error when attempting to retrieve {} from Yahoo Finance".format(tickerIndex))

#output to dictionary csv 
with open('over_under_valuation_FINAL.csv', 'w') as f:
            for key in valueDict.keys():
                f.write("%s,%s\n"%(key,valueDict[key]))
