@echo off
REM Command line explanation:
REM Download all data between 20110101 and 20111231 for
REM the tickers in the text file sp500_tickers.txt
REM and output the lot to sp500.csv
REM The -i means read the tickers from standard input 
REM (which in this case is the file sp500_tickers.txt)
REM rather than from the command line itself as is
REM otherwise the case without the -i.

REM The command below assumes that the Python interpreter
REM is on your operating system search PATH and that
REM the pyq.py file is in the current directory or also
REM in a folder on the search PATH.

REM Note: sp500_tickers are all the tickers as listed on 
REM Wikipedia as of this writing, and *also* including the ticker
REM SPY itself as well.  SPY is an ETF that tracks the S&P 500 
REM but isn't part of the S&P itself obviously.  

pyq -i 20110101 20111231 <sp500_tickers.txt  >sp500_tickers.csv