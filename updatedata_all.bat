REM By default this batch file will not auto retry any
REM missing data values since the long date ranges make
REM this generally impractical.  However if we want to 
REM redo the cache from scratch, then feel free to change
REM this:
set retry=0

pyq.py -r%retry% 19281001 "^DJI" >".\CSV\^DJI.csv"
pyq.py -r%retry% 20090915 "CEY.L" >".\CSV\CEY.L.csv"
pyq.py -r%retry% 20000104 "^FTMC" >".\CSV\^FTMC.csv"
pyq.py -r%retry% 19840402 "^FTSE" >".\CSV\^FTSE.csv"
pyq.py -r%retry% 20050811 "CF" >".\CSV\CF.csv"
pyq.py -r%retry% 20020813 "ISF.L" >".\CSV\ISF.L.csv"
pyq.py -r%retry% 20000526 "IWM" >".\CSV\IWM.csv"
pyq.py -r%retry% 20040330 "MIDD.L" >".\CSV\MIDD.L.csv"
pyq.py -r%retry% 19860313 "MSFT" >".\CSV\MSFT.csv"
pyq.py -r%retry% 19620102 "IBM" >".\CSV\IBM.csv"
pyq.py -r%retry% 20051026 "NNVC" >".\CSV\NNVC.csv"
pyq.py -r%retry% 20070301 "UUP" >".\CSV\UUP.csv"
pyq.py -r%retry% 19500103 "^GSPC" >".\CSV\^GSPC.csv"
pyq.py -r%retry% 19801223 "^DJA" >".\CSV\^DJA.csv"
pyq.py -r%retry% 19600104 "^DJT" >".\CSV\^DJT.csv"
pyq.py -r%retry% 19600104 "^DJU" >".\CSV\^DJU.csv"
pyq.py -r%retry% 20000104 "^FTLC" >".\CSV\^FTLC.csv"
pyq.py -r%retry% 20000104 "^FTT1X" >".\CSV\^FTT1X.csv"
pyq.py -r%retry% 19901126 "^GDAXI" >".\CSV\^GDAXI.csv"
pyq.py -r%retry% 19960423 "^GOX" >".\CSV\^GOX.csv"
pyq.py -r%retry% 19901025 "^IXBK" >".\CSV\^IXBK.csv"
pyq.py -r%retry% 20000103 "^IXF" >".\CSV\^IXF.csv"
pyq.py -r%retry% 19840104 "^N225" >".\CSV\^N225.csv"
pyq.py -r%retry% 19851001 "^NDX" >".\CSV\^NDX.csv"
pyq.py -r%retry% 19870910 "^RUT" >".\CSV\^RUT.csv"
pyq.py -r%retry% 19831219 "^XAU" >".\CSV\^XAU.csv"
pyq.py -r%retry% 19830826 "^XOI" >".\CSV\^XOI.csv"
