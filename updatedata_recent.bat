REM Retry the recent data missing parts 7 times
REM so if run on a daily basis, any late data not delayed
REM by more than 7 days will get picked up without slowing
REM down downloads later on.
..\..\..\pyq\pyq.py -r7 20120401 0 "BP.L" "^DJA" "^DJI" "^DJT" "^DJU" "^FTLC" "^FTMC" "^FTSE" "^FTT1X" "^GDAXI" "^GOX" "^GSPC" "^IXBK" "^IXF" "^N225" "^NDX" "^XAU" "^XOI" CF "ISF.L" IWM MSFT IBM NNVC UUP

REM OK now that the cache has been updated, rewrite all the CSV files:
updatedata_all.bat