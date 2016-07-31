# pyq
Python Quote Grabber. Fetches quotes from Yahoo and Oanda.

A Python module and stand alone utility to retrieve live and historical stock quote data from Yahoo! as well as historical FX closing quote data from Oanda. Original version (0.7) on which this project is based by Rimon Barr.

This project is a fork of the pyQ project by Rimon Barr. The original version of source is version 0.7 and was taken from here: http://rimonbarr.com/repository/pyq/ 

The original page also contains further examples of use etc so please refer there for more information.

This version is updated to run with newer versions of Python (2.x, 3.x) and is improved as follows:
- Mostly PyLint, PyChecker, pep8 compliant
- Fixed ctrl-c/break handling issues when querying large number of tickers
- Fixed "live" and historical quote handling for tickers like ^DJI that Yahoo no longer provide download quotes for.
- Removed dependencies on all deprecated Python modules and constructs (e.g. backticks -> repr(), string module removed, calls to map() replaced by list comprehensions etc.)
- Replaced time module with datetime as some tickers (e.g. ^DJI) use dates well before the start of the Unix time epoch.
- Added better debugging handling/support (introduced "debug_print()")
- Refactored command line argument handling
- Added command line option -r:n/--retryfailed=n to allow external control of cache behaviour.
- Modified default date handling: Specifying 0 for the end date results in it being set to todays date.
- Will download a "provisional" record for today based on current "live" quote if todays date is requested and not yet available from the Yahoo history. (Helps when Yahoo is slow at getting their historical db updated.)

Possible future work:
- Add a command line option to specify the cache DB location and/or name. (But see the next point.)
- Replace the current cache implementation with something better. (SQLite?)
- Add a GUI. It might be useful to add an optional GUI to the app to query and work with the symbols in the cache.

Contributions/suggestions welcome, please contact me via Launchpad if interested.

#Misc. Notes
- pyq will automatically note when a ticker doesn't support the Yahoo CSV download URL and will then retrieve the data out of the web pages instead. 

- pyq will note when todays date is included in the date range and therefore isn't yet included in the historical download data, and will do its best to comply with your request in a sensible way: In such a case it will seamlessly go and scrape the latest available data for todays date from the "live quote" page alongside the data it retrieves from the historical URL or cache, and output it as normal.  It will not however store such live quote data in the cache as it may not be final and subject to change, consequently if if you run pyq again for todays date, it again it will again fetch the latest available O,H,L,C for today.  (Aside, unfortunately some of the problem tickers like ^DJI doesn't provide live quotes, so you'll get a warning from pyq if you try to request a "live" quote for such a ticker for current day.  Not much you can do if no live quote is available.)

- pyq supports historical simple closing price spot quotes for FX pairs from Oanda using ticker names such as 'EURUSD=X' for example.  

- If you use adjusted close for anything you should probably not rely on pyq's cache too much (or at all) since, all historical adjusted close values change when stock prices are adjusted for dividends/splits etc. Pyq does no checking and has no special treatment for adjusted close values at present.  (A possible enhancement would be to detect adjustment events and then invalidate the cache automatically.)

##"retryfailed" option value explanation
The "retryfailed" option deals with any situation where pyq doesn't already have price data for a given security on a given date for any reason, by retrying fetching such dates a number of times.   

What happens is that  pyq will note down dates for which it failed one way or another to retrieve data into the local cache, it will then retry fetching these from Yahoo on future requests when such date (or set of dates) is again included in the requested date range, providing the number of retries do not exceed the limit specified in the paramters.  That is to say the retry parameter value is the maximum retry count, such that pyq will give up trying to get a given date after the number specified has been reached.  

The special value -1 can be used to "reset" retry counts if you'd like to get pyq to forget how many times it's previously tried to fetch missing date, and -2 can be used to force it to get all data from source regardless of what's in the cache. 
