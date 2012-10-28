REM By setting retry to 7 and using a recent start date,
REM you ensure that so long as this batch file is run 
REM regularly, the cache will be updated with new data on
REM yahoo without either referencing large date ranges
REM (which the current DBM cache can be slow on) or
REM hitting Yahoo's website needlessly.  So this 
REM batch file will basically update the DBM cache
REM and then call the other batch file to extract all
REM the data into CSV files.
set retry=7

pyq.py -r%retry% 20120601 0 "^FTSE" >".\CSV\^FTSE.csv_"
pyq.py -r%retry% 20120601 0 "ISF.L" >".\CSV\ISF.L.csv_"
pyq.py -r%retry% 20120601 0 "^FTMC" >".\CSV\^FTMC.csv_"
pyq.py -r%retry% 20120601 0 "MIDD.L" >".\CSV\MIDD.L.csv_"
pyq.py -r%retry% 20120601 0 "^DJI" >".\CSV\^DJI.csv_"
pyq.py -r%retry% 20120601 0 "DIA" >".\CSV\DIA.csv_"
pyq.py -r%retry% 20120601 0 "^TNX" >".\CSV\^TNX.csv_"
pyq.py -r%retry% 20120601 0 "^IXIC" >".\CSV\^IXIC.csv_"
pyq.py -r%retry% 20120601 0 "^STOXX50E" >".\CSV\^STOXX50E.csv_"
pyq.py -r%retry% 20120601 0 "^SSMI" >".\CSV\^SSMI.csv_"
pyq.py -r%retry% 20120601 0 "^OEX" >".\CSV\^OEX.csv_"
pyq.py -r%retry% 20120601 0 "^GSPC" >".\CSV\^GSPC.csv_"
pyq.py -r%retry% 20120601 0 "BP.L" >".\CSV\BP.L.csv_"
pyq.py -r%retry% 20120601 0 "RRL.L" >".\CSV\RRL.L.csv_"
pyq.py -r%retry% 20120601 0 "CEY.L" >".\CSV\CEY.L.csv_"
pyq.py -r%retry% 20120601 0 "CF" >".\CSV\CF.csv_"
pyq.py -r%retry% 20120601 0 "IWM" >".\CSV\IWM.csv_"
pyq.py -r%retry% 20120601 0 "MSFT" >".\CSV\MSFT.csv_"
pyq.py -r%retry% 20120601 0 "IBM" >".\CSV\IBM.csv_"
pyq.py -r%retry% 20120601 0 "NNVC" >".\CSV\NNVC.csv_"
pyq.py -r%retry% 20120601 0 "UUP" >".\CSV\UUP.csv_"
pyq.py -r%retry% 20120601 0 "^DJA" >".\CSV\^DJA.csv_"
pyq.py -r%retry% 20120601 0 "^DJT" >".\CSV\^DJT.csv_"
pyq.py -r%retry% 20120601 0 "^DJU" >".\CSV\^DJU.csv_"
pyq.py -r%retry% 20120601 0 "^FTLC" >".\CSV\^FTLC.csv_"
pyq.py -r%retry% 20120601 0 "^FTT1X" >".\CSV\^FTT1X.csv_"
pyq.py -r%retry% 20120601 0 "^GDAXI" >".\CSV\^GDAXI.csv_"
pyq.py -r%retry% 20120601 0 "^GOX" >".\CSV\^GOX.csv_"
pyq.py -r%retry% 20120601 0 "^IXBK" >".\CSV\^IXBK.csv_"
pyq.py -r%retry% 20120601 0 "^IXF" >".\CSV\^IXF.csv_"
pyq.py -r%retry% 20120601 0 "^N225" >".\CSV\^N225.csv_"
pyq.py -r%retry% 20120601 0 "^NDX" >".\CSV\^NDX.csv_"
pyq.py -r%retry% 20120601 0 "^RUT" >".\CSV\^RUT.csv_"
pyq.py -r%retry% 20120601 0 "^XAU" >".\CSV\^XAU.csv_"
pyq.py -r%retry% 20120601 0 "^XOI" >".\CSV\^XOI.csv_"
pyq.py -r%retry% 20120601 0 "TSCO.L" >".\CSV\TSCO.L.csv_"
pyq.py -r%retry% 20120601 0 "TSCO" >".\CSV\TSCO.csv_"
pyq.py -r%retry% 20120601 0 "^SOX" >".\CSV\^SOX.csv_"
REM Data not available on Yahoo
REM pyq.py -r%retry% 20120601 0 "^IXM" >".\CSV\^IXM.csv_"
pyq.py -r%retry% 20120601 0 "XLF" >".\CSV\XLF.csv_"

REM OK now that the cache has been updated, rewrite all the CSV files:
extract_to_csv.bat

del .\CSV\*.csv_