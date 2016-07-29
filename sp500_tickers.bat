@echo off
REM Example use of pyq.

REM Command line explanation:
REM Download all data between 20150101 and 20151231 for
REM the tickers in the text file sp500_tickers.txt
REM and output the lot to sp500_2015.csv

REM The -i means read the tickers from standard input 
REM which in this case implies the file sp500_tickers.txt
REM due to input redirection, rather than from the command line 
REM as would normally be the case without the -i.

REM Note: The command below assumes that the Python interpreter
REM is on your operating system search PATH and that
REM the pyq.py file is in the current directory or also
REM in a folder on the search PATH.  Adjust accordingly if this
REM is not the case.  

REM Note: The content of sp500_tickers.txt are all the tickers 
REM as listed on Wikipedia as of this writing (28/07/2016), 
REM and *also* including the "SPY" ticker itself as well.  
REM (To those who may not know this: SPY is an ETF that tracks 
REM the S&P 500, but isn't itself part of the S&P obviously.   

pyq -i 20150101 20151231 <sp500_tickers.txt  >sp500_2015.csv