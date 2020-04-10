# Clean-Surplus-Model (Risidual Income Model)

Objective: use model to estimate the value of firm's shares then compare to actual market value

Theory supplied by Feltham and Ohlson (FO; 1995).

Model provides framework for determining market value by utilizing balance sheet and income statement fundamentals.

# Assumptions
Assumes capital market conditions are stable and dividend irrelevancy.

Assumes that the company is not in a growth stage (i.e., negative ROE). Might be more appropriate to use projected or industry average ROE.

Assumes that ROE stays constant for horizon input. In reality, ROE can change in response to a number of factors such as competition. ROE has been determined from the fundamentals of the financial statements in one particular year. Therefore, it is static and may not encapsulate all the information gathered / researched, for instances, by analysts.

Additionally, model assumes that abnormal earnings persist for the horizon given and then drop to zero. Reality could be quite different, for example, persist for only three years or fifteen. There is potential for a 'declining abnormal earnings pattern' that is not captured in this model.

# Estimates and Variables
High level: risk-free interest rate, dividend payout ratio, and cost of capital (CAPM).

Variables in play (in millions for values):
- Base Year
- Net Income (Base Year)
- Book Value (Previous Year)
- Book Value (Base Year)
- Return on Equity
- Expected Horizon for ROE to persist
- Dividends Paid (Base Year)

CAP Variables
- Risk Free Rate
- Market Risk Premium
- Beta

# Versions
1) Non-interative - manually put in all variables
2) Iterative - most variables are pulled via yfinance API, few assumptions are hardcoded (i.e., CAPM and ROE horizon), assumes most recent year and data that is available, will loop through all tickers in CSV file in referenced path and spit out over / under valuation

# Results from S&P500 Companies (Over/Under Valued)
![Value Variance](https://user-images.githubusercontent.com/13516076/78972479-d9e03f00-7adb-11ea-99b2-40ea159dc067.png)

Observed an average unvervaluation of ~$50 over entire population of sampled companies (357 total after removing outliers / faulty data) as of run occuring on April 10, 2020. Hardcoded variables: risk-free rate 2.45% (based on BoC prime rate), market risk premium 5.6%, ROE horizon of 7 years and base year of 2019/20 (depending on most recent report of 10k).

# Sources
Scott, William R. Financial Accounting Theory. Toronto, Ont: Pearson Prentice Hall, 2009. Print.
