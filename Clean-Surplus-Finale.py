import numpy as np
import scipy.stats as si
import sympy as sy
import matplotlib as mpl
from sympy.stats import Normal, cdf
from sympy import init_printing
from matplotlib import pyplot as plt
init_printing()

print("Please enter all values in millions.")

#Financial Statement Variables
by = int(input("Base Year: ")) #i.e., year zero
py = by - 1 #previous year (base year - 1)
byNI = float(input("Base year Net Income: "))
pyBV = float(input("Previus year Book Value: "))
byBV = float(input("Base year Book Value: "))
vROE = float(input("ROE as of January 1st, {}, or as at December 31, {}: ".format(by,py)))
vROElen = float(input("Number of years ROE is expected to persist (i.e., Horizon): ")) #after which ROE will equal cost of capital
byDiv = float(input("Dividend in base year (per share): "))
pytrt = byDiv / byNI #payout ratio defined as Dividend (base year) / NI (base year), assume will contineu for seven years

#CAPM variables
vRf = float(input("Risk-Free Rate: ")) #use Canadian bank prime rate of 0.0125 per annum
vMRP = float(input("Market Risk Premium: ")) # risk premium demanded by market
vMR = vRf + vMRP # market return, i.e., risk-free rate + market risk premium
Bta = float(input("Beta: ")) # define beta, i.e., the market risk, can be found from Reuters for particular stock exchange; future addition, pull from website based on market selection
Kc = (vRf * (1 - Bta)) + (Bta*vMR) # cost of capital of Company - calculation

#Sample variables below (based on Canadian Tire 2012 10-K SEC report)

#Financial Statement Variables
#by = 2012
#byNI = 499.2
#pyBV = 4409
#byBV = 4763.6
#vROE = 0.1132
#vROElen = 7
#byDIV = 101.7

#CAPM Variables
#vRf = 0.0125
#vMRP = 0.058
#Bta = 0.66

#Calculate projected book values for [base year + 1, ..., base year + vROElen (i.e., horizon) - 1]
#Example for base year of 2012: [2013, 2014, 2015, 2016, 2017, 2018]
Book_Values = []

def fun(currentyear, finalyear, BVpy, pytrt, vROE):
    BVcy = BVpy*(1+((1-pytrt)*vROE))
    #Book_Values.append((BVcy, currentyear))
    Book_Values.append(float(BVcy))
    if currentyear == finalyear:
        return Book_Values
    else:
        return fun(currentyear+1, finalyear, BVcy, pytrt, vROE)

print("Recursive Book Values calculated for Year {} to Year {}".format(by+1,int(by+vROElen - 1)))        
print(fun(by + 1, by + vROElen - 1, byBV, pytrt, vROE))

#Insert base year book value into range of book values determined above
Book_Values.insert(0,byBV)

#Determine surplus (i.e., abnormal earnings) for each book value (book value * (ROE - cost of capital)
vOX_Values = [i * (vROE - Kc) for i in Book_Values]

print("Abnormal Earnings for Year {} to Year {}".format(by+1,int(by + vROElen)))
print(vOX_Values)

#Discount the abnormal earnings for [base year + 1, ..., base year + vROElen (i.e., horizon)]
#Example for base year of 2012: [2013, 2014, 2015, 2016, 2017, 2018, 2019]
#Abnormal earnings is synonymous with Goodwill
def some(voxvalues, Kc):
    temp = []
    n = 1
    for i in voxvalues:
        temp.append(i/((1+Kc)**(n)))
        n = n+1
    return temp

print("Discounted Abnormal Earnings for Year {} to Year {}".format(by+1, int(by + vROElen)))
print(some(vOX_Values, Kc))

print("Sum of Total Abnormal Earnings for Year {} to Year {}".format(by+1, int(by + vROElen)))
print(sum(some(vOX_Values, Kc)))

#Base year book value + abnormal earnings (i.e., Goodwill) = Total Valuation of Company
vPA = byBV + sum(some(vOX_Values, Kc))

#Number of shares outstanding as of base year-end date
#Sample Shares Outstanding: 81,143,767
numshares = float(input("Number of Shares Outstanding: "))

#Determination of Share value = Total Valuation of Company / Number of Shares / 1 million
#Divide by a million because initial variable input was in millions
Share_Value = vPA / (numshares / 1000000)

print("Valuation of Shares as of {} Year-End".format(by))
print(Share_Value)

#Enter share value as at base year-end date trading on particular market
curr_share_value = float(input("Current Share Value for Comparison: "))

ValueComparison = abs((curr_share_value - Share_Value))

#Determines if overvalued or undervalued with simple arithmetic
def ValuationStatement(currentprice, intrinsicprice, ValueComparison):
    if currentprice -  intrinsicprice >= 0:
        statement = "Shares overvalued by {}".format(ValueComparison)
    elif currentprice - intrinsicprice <= 0:
        statement = "Shares undervalued by {}".format(ValueComparison)
    
    return statement

print(ValuationStatement(curr_share_value, Share_Value, ValueComparison))


