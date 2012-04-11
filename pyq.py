#!/usr/bin/env python

"""
Retrieve stock quote data from Yahoo and forex rate data from Oanda.
"""

##################################################
# Name:        pyQ - Python Quote Grabber
# Author:      Rimon Barr <barr@cs.cornell.edu>
# Start date:  10 January 2002
# Purpose:     Retrieve stock quote data in Python
# License:     GPL 2.0

##################################################
# Activity log:
#
# 10/01/02 - Initial release
# 14/10/02 - Yahoo changed url format
# 31/10/02 - More convenient programmatic interface and local caching
# 21/09/04 - Updated by Alberto Santini to accomodate Yahoo changes
# 27/01/05 - Updated by Alberto Santini to accomodate Yahoo changes
# 11/01/07 - Updated by Ehud Ben-Reuven, Historical currency exchnage tickers
#            (e.g. USDEUR=X) are retrieved from www.oanda.com
# 15/03/07 - code cleanup; updated Yahoo date format, thanks to Cade Cairns
# 11/04/12 - 0.7.1 Walter Prins: Fixed exception handling during long runs 
#            where ctrl-c would get caught by unconditional exception clauses.
#            Also cleaned up/refactored to 99% pass PyLint, Pep8 and Pychecker.

import sys, re, traceback, getopt, urllib, anydbm, time

Y2KCUTOFF = 60
__version__ = "0.7.1"
CACHE = 'stocks2.db'
DEBUG = 2


def debug_print(level, msg):
    """ Utility method to handle debug output.  Messages are only printed
    if the DEBUG level is equal to or higher than the msg level.  Thus
    setting DEBUG = 0 will disable all debug output while higher values
    will increase debug output successively. """
    if DEBUG >= level:
        print msg


def print_header():
    """Print program header information to stdout"""
    print 'pyQ v%s, by Rimon Barr:' % __version__
    print '- Python Yahoo Quote fetching utility'


def exit_version():
    """Display version message to command line user."""
    print_header()
    sys.exit(0)


def exit_usage():
    """Display usage/help message to command line user."""
    print_header()
    print """
Usage: pyQ [-i] [start_date [end_date]] ticker [ticker...]
             pyQ -h | -v

    -h, -?, --help      display this help information
    -v, --version       display version'
    -i, --stdin         tickers fed on stdin, one per line

    - date formats are yyyymmdd
    - if enddate is omitted, it is assume to be the same as startdate
    - if startdate is omitted, we use *current* stock tables and otherwise, use
        historical stock tables. Current stock tables will give previous close
        price before market closing time.)
    - tickers are exactly what you would type at finance.yahoo.com
    - output format: "ticker, date (yyyymmdd), open, high, low, close, vol"
    - currency exchange rates are also available, but only historically.
        The yahoo ticker for an exchange rate is of the format USDEUR=X. The
        output format is "ticker, date, exchange".

    Send comments, suggestions and bug reports to <rimon@acm.org>
"""
    sys.exit(0)


def exit_usage_error():
    """Display error message to command line user."""
    sys.exit("pyQ: command syntax error\n" +
             "Try 'pyQ --help' for more information.")


def is_int(i):
    """Checks whether the given object can be converted to an integer"""
    try:
        int(i)
        return 1
    except ValueError:
        return 0


def split_lines(buf):
    """Splits the given buffer/line on whitespace/newlines into a list"""
    return buf.split()


def parse_date(yyyymmdd):
    """Convert yyyymmdd string to tuple (yyyy, mm, dd)"""
    return (yyyymmdd[:-4], yyyymmdd[-4:-2], yyyymmdd[-2:])


def yy2yyyy(yy_2digits):
    """Convert a 2 digit century string to a 4 digit century string."""
    yy_2digits = int(yy_2digits) % 100
    if yy_2digits < Y2KCUTOFF:
        return repr(yy_2digits + 2000)
    else:
        return repr(yy_2digits + 1900)


# convert month to number
MONTH2NUM = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
    'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}


def dd_mmm_yy2yyyymmdd(dd_mmm_yy):
    """Convert a dd_mmm_yy string to yyyymmdd format"""
    dd_mmm_yy = dd_mmm_yy.split('-')
    day = '%02d' % int(dd_mmm_yy[0])
    month = '%02d' % MONTH2NUM[dd_mmm_yy[1]]
    year = yy2yyyy(dd_mmm_yy[2])
    return year + month + day


DAYSECS = 60 * 60 * 24


def all_dates(startdate, enddate):
    """Return all dates in ascending order. Inputs in yyyymmdd format"""
    if int(startdate) > int(enddate):
        raise IndexError('startdate must be smaller than enddate')
    startdate = time.mktime(time.strptime(startdate, '%Y%m%d'))
    enddate = time.mktime(time.strptime(enddate, '%Y%m%d')) + 1
    dates = []
    while startdate < enddate:
        dates.append(time.strftime('%Y%m%d', time.localtime(startdate)))
        startdate += DAYSECS
    return dates


def agg_dates(dates):
    """Aggregate list of dates (yyyymmdd) in range pairs"""
    if not dates:
        return []
    aggs = []
    dates = [int(date) for date in dates]
    dates.sort()
    high = dates.pop(0)
    low = high
    for date in dates:
        if date == high + 1:
            high = date
        else:
            aggs.append((low, high,))
            high = date
            low = high
    aggs.append((low, high,))
    return [(str(low), str(high)) for (low, high) in aggs]


def get_rate(startdate, enddate, ticker):
    """Retrieve FX exchange closing rates for the pair specified as "ZZZYYY=X"
    where ZZZ is the one currency and YYY is the other currency. Only the
    closing rate is fetched as that's all that's available."""
    if not (len(ticker) == 8 and ticker.endswith('=X')):
        raise Exception('Illegal FX rate ticker')
    debug_print(1, '# Querying Oanda historical for %s (%s-%s)' %
                (ticker, startdate, enddate)
               )
    cur1, cur2 = ticker[0:3], ticker[3:6]

    def yyyymmdd2mmddyy(yyyymmdd):
        """Converts a date string in format yyyymmdd to mmddyy format."""
        return yyyymmdd[4:6] + '%2F' + yyyymmdd[6:8] + '%2F' + yyyymmdd[2:4]

    def mmddyy2yyyymmdd(mmddyy):
        """Converts a date string in format mmddyy to  yyyymmdd format."""
        if len(mmddyy) != 10 or mmddyy[2] != '/' or mmddyy[5] != '/':
            raise Exception('Illegal date format')
        return mmddyy[6:10] + mmddyy[0:2] + mmddyy[3:5]

    startdate, enddate = yyyymmdd2mmddyy(startdate), yyyymmdd2mmddyy(enddate)
    url = 'http://www.oanda.com/convert/fxhistory'
    query = (
        ('lang', 'en'),
        ('date1', startdate),
        ('date', enddate),
        ('date_fmt', 'us'),
        ('exch', cur1),
        ('exch2', ''),
        ('expr', cur2),
        ('expr2', ''),
        ('margin_fixed', '0'),
        ('SUBMIT', 'Get+Table'),
        ('format', 'CSV'),
        ('redirected', '1')
        )
    query = ['%s=%s' % (var, val) for (var, val) in query]
    query = '&'.join(query)
    page = urllib.urlopen(url + '?' + query).read().splitlines()
    table = False
    result = []
    for line in page:
        if line.startswith('<PRE>'):
            table = True
            line = line[5:]
        elif line.startswith('</PRE>'):
            table = False
        if table:
            line = line.split(',')
            line[0] = mmddyy2yyyymmdd(line[0])
            line = [ticker] + line
            result.append(line)
    return result


def get_ticker(startdate, enddate, ticker):
    """Get historical ticker data for the specified ticker as on Yahoo
    between the specified dates directly from Yahoo."""
    if len(ticker) == 8 and ticker.endswith('=X'):
        return get_rate(startdate, enddate, ticker)
    debug_print(1, '# Querying Yahoo! historical for %s (%s-%s)' %
                (ticker, startdate, enddate)
               )
    startdate, enddate = parse_date(startdate), parse_date(enddate)
    url = 'http://ichart.finance.yahoo.com/table.csv'
    query = (
        ('a', '%02d' % (int(startdate[1]) - 1)),
        ('b', startdate[2]),
        ('c', startdate[0]),
        ('d', '%02d' % (int(enddate[1]) - 1)),
        ('e', enddate[2]),
        ('f', enddate[0]),
        ('s', ticker),
        ('y', '0'),
        ('g', 'd'),
        ('ignore', '.csv'),)
    query = ['%s=%s' % (var, str(val)) for (var, val) in query]
    query = '&'.join(query)
    urldata = urllib.urlopen(url + '?' + query).read()
    lines = split_lines(urldata)
    if re.match('no prices|Not Found', lines[0], re.I):
        debug_print(2, '# No prices found for ticker %s, range %s - %s'
                    % (ticker, startdate, enddate)
                   )
        return
    lines, result = lines[1:], []
    for line in lines:
        line = line.split(',')
        result.append([ticker, line[0].replace('-', '')] + line[1:])
    return result


def get_cached_ticker(startdate, enddate, ticker, forcefailed=0):
    """Get tickers, hopefully from cache.
        startdate, enddate = yyyymmdd starting and ending
        ticker = symbol string
        forcefailed = integer for cachebehaviour
            =0 : do not retry failed data points
            >0 : retry failed data points n times
            -1 : retry failed data points, reset retry count
            -2 : ignore cache entirely, refresh ALL data points"""

    debug_print(1, '# Querying cache for %s (%s-%s)' %
                (ticker, startdate, enddate)
               )

    dates = all_dates(startdate, enddate)
    # get from cache
    data = {}
    cache_db = anydbm.open(CACHE, 'c')
    for date in dates:
        try:
            data[(date, ticker)] = cache_db[repr((date, ticker))]
        except KeyError:
            pass
    # forced failed
    if forcefailed:
        for key in data.keys():
            if (forcefailed == -2 or
                    (forcefailed == -1 and type(eval(data[key])) == type(0)) or
                    eval(data[key]) < forcefailed):
                del data[key]
    # compute missing
    cached = [date for date, ticker in data.keys()]
    missing = [date for date in dates if date not in cached]
    for startdate, enddate in agg_dates(missing):
        #try:
        tickerdatalist = get_ticker(startdate, enddate, ticker)
        for row in tickerdatalist:
            _, date, datum = row[0], row[1], row[2:]
            data[(date, ticker)] = cache_db[repr((date, ticker))] = repr(datum)
        #except: pass
    # failed
    cached = [date for date, row in data.keys()]
    failed = [date for date in missing if date not in cached]
    for date in failed:
        try:
            times = eval(cache_db[repr((date, ticker))])
        except KeyError:
            times = 0
        if forcefailed < 0:
            times = 1
        if times < forcefailed:
            times = times + 1
        data[(date, ticker)] = cache_db[repr((date, ticker))] = repr(times)
    # result
    result = []
    for date in dates:
        datum = eval(data[(date, ticker)])
        if type(datum) != type(0):
            result.append([ticker, date] + datum)
    return result


def get_tickers(startdate, enddate, tickers, forcefailed=0):
    """Get tickers.
        startdate, enddate = yyyymmdd starting and ending
        tickers = list of symbol strings
        forcefailed = integer for cachebehaviour
            =0 : do not retry failed data points
            >0 : retry failed data points n times
            -1 : retry failed data points, reset retry count
            -2 : ignore cache entirely, refresh ALL data points"""
    result = []
    for ticker in tickers:
        result += get_cached_ticker(startdate, enddate, ticker, forcefailed)
    return result


def get_tickers_now_chunk(tickers):
    """Get current value of specified tickers directly from Yahoo."""
    url = 'http://finance.yahoo.com/d/quotes.csv?%s' % urllib.urlencode(
            {'s': ''.join(tickers), 'f': 'sohgpv', 'e': '.csv'})
    urldata = urllib.urlopen(url).read()
    lines, datetime, result = split_lines(urldata), time.localtime(), []
    for line in lines:
        line = line.split(',')
        result.append(
            [(line[0][1:-1]).lower(), '%4d%02d%02d' % datetime[0:3]] + line[1:]
            )
    return result


def get_tickers_now(tickers):
    """Get current value of specified tickers directly from Yahoo."""
    result = []
    while tickers:
        result += get_tickers_now_chunk(tickers[:150])
        tickers = tickers[150:]
    return result


def arg_startdate(args):
    """Parse the startdate from the command line."""
    todaydate = time.localtime()
    startdate = '%4d%02d%02d' % (todaydate[0], todaydate[1], todaydate[2])
    if len(args) >= 1 and is_int(args[0]) and int(args[0]) > 0:
        startdate = args[0]
    return startdate


def arg_enddate(args):
    """Parse the enddate from the command line."""
    enddate = arg_startdate(args)
    if len(args) >= 2 and is_int(args[1]) and int(args[1]) > 0:
        enddate = args[1]
    return enddate


def arg_fetchlive(args):
    """Parse the fetchlive parameter from the command line."""
    fetchlive = 1
    if len(args) >= 1 and is_int(args[0]):
        fetchlive = 0
    return fetchlive


def arg_tickers(args):
    """Parse the tickers from the command line."""
    tickers = []
    for arg in args:
        if not is_int(arg):
            tickers.append(arg)
    return tickers


def main():
    """Main program: Implements arg command line interface to fetching stock
    data from Yahoo."""
    # parse options
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], 'hv?i', ['help', 'version', 'stdin']
            )
    except getopt.GetoptError:
        exit_usage_error()

    # process options
    stdin_tickers = []
    for option, _ in opts:
        if option in ("-h", "--help", "-?"):
            exit_usage()
        if option in ("-v", "--version"):
            exit_version()
        if option in ("-i", "--stdin"):
            stdin_tickers = split_lines(sys.stdin.read())

    startdate = arg_startdate(args)
    enddate = arg_enddate(args)
    fetchlive = arg_fetchlive(args)
    tickers = arg_tickers(args)
    tickers.extend(stdin_tickers)

    if len(tickers) == 0:
        exit_usage()

    if fetchlive:
        result = get_tickers_now(tickers)
    else:
        result = get_tickers(startdate, enddate, tickers)

    for line in result:
        print ','.join(line)


try:
    if __name__ == '__main__':
        main()
except KeyboardInterrupt:
    traceback.print_exc()
    print 'Break!'
