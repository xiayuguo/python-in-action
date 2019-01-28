import sys
import time

from functools import reduce
from datetime import datetime, date, timedelta


PY2, PY3 = 2, 3

NONE_TIME = "0000-00-00 00:00:00"

if sys.version_info[0] == PY2:
    string_type = basestring
    number_type = (int, float, long)
else:
    string_type = str
    number_type = (int, float)


maxsize = sys.maxsize  # 32bit: 2147483647, 64bit: 9223372036854775807


class CTime(object):
    """ Convert all displays of time to datetime
        Examples:
        >>> import time
        >>> import ctime
        >>> from datetime import datetime
        >>> ctime()
        <CTime [2018-05-03 10:55:07]>
        >>> ctime(None)
        <CTime [2018-05-03 10:55:15]>
        >>> ctime('2018-05-03 10:55:15')
        <CTime [2018-05-03 10:55:15]>
        >>> ctime('2018-05-03T10:55:15')
        <CTime [2018-05-03 10:55:15]>
        >>> ctime('2018-05-03T10:55:15.100000')
        <CTime [2018-05-03 10:55:15]>
        >>> ctime('2018-05-03 10:55:15.100000')
        <CTime [2018-05-03 10:55:15]>
        >>> ctime('2018-05-03')
        <CTime [2018-05-03 00:00:00]>
        >>> ctime('10:55:15')
        <CTime [1900-01-01 10:55:15]>
        >>> ctime(datetime.now())
        <CTime [2018-05-03 11:04:14]>
        >>> ctime(time.time())
        <CTime [2018-05-03 11:04:22]>
        >>> ctime(str(time.time()))
        <CTime [2018-05-03 11:04:29]>
        >>> ctime(time.gmtime())
        <CTime [2018-05-03 03:06:23]>
        >>> str(ctime(datetime.now()))
        '2018-05-03 11:15:09'
        >>> ctime(ctime('2018-05-08'))
        <CTime [2018-05-08 00:00:00]>
        >>> a = ctime()
        >>> b = ctime()
        >>> a
        <CTime [2018-07-25 09:53:23]>
        >>> b
        <CTime [2018-07-25 09:53:30]>
        >>> a < b
        True
        >>> a <= b
        True
        >>> a + b
        <CTime [2067-02-15 11:46:53]>
        >>> b - a
        datetime.timedelta(0, 6, 601950)
        >>> format(ctime(), '%Y%m%d%H%M%S')
        '20180725102809'
    """
    def __init__(self, time_data=None):
        self._datetime = datetime.now()
        if time_data is None:
            pass
        elif isinstance(time_data, datetime):
            self._datetime = time_data
        elif isinstance(time_data, string_type):
            self.fromtimestring(time_data)
        elif isinstance(time_data, number_type):
            self.fromtimestamp(time_data)
        elif isinstance(time_data, time.struct_time):
            self._datetime = datetime.fromtimestamp(time.mktime(time_data))
        elif isinstance(time_data, date):
            self._datetime = datetime.combine(time_data, datetime.min.time())
        elif isinstance(time_data, CTime):
            self._datetime = time_data._datetime
        else:
            raise TypeError("type %s not supported." % type(time_data))
        self._timestamp = int(time.mktime(self._datetime.timetuple())) if self._datetime else 0
        if self._timestamp > maxsize:
            raise ValueError('timestamp(%s) beyond the maxsize(%s)' % (self._timestamp, maxsize))

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def datetime(self):
        return self._datetime

    def fromtimestamp(self, timestamp):
        ts = self._get_timestamp_from_input(timestamp)
        self._datetime = datetime.fromtimestamp(ts)

    def fromtimestring(self, time_str):
        if not time_str:
            return
        if self.is_number(time_str):
            self.fromtimestamp(time_str)
        elif len(time_str) >= 19:
            time_str = time_str[:19]
            if time_str == NONE_TIME:
                self._datetime = None
            elif "-" in time_str and ":" in time_str and "T" in time_str:
                self._datetime = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")
            elif "-" in time_str and ":" in time_str and " " in time_str:
                self._datetime = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            else:
                raise ValueError("cannot parse '{0}' as a timestring".format(time_str))
        elif ":" in time_str:
            self._datetime = datetime.strptime(time_str, "%X")
        elif "-" in time_str:
            self._datetime = datetime.strptime(time_str, "%Y-%m-%d")
        else:
            raise ValueError("cannot parse '{0}' as a timestring".format(time_str))

    @staticmethod
    def _get_timestamp_from_input(timestamp):
        try:
            ts = float(timestamp)
        except:
            raise ValueError("cannot parse '{0}' as a timestamp".format(timestamp))
        else:
            if ts < 0:
                raise ValueError('timestamp(%s) must be greater than 0' % ts)
            elif ts > maxsize:
                raise ValueError('timestamp(%s) beyond the maxsize(%s)' % (ts, maxsize))
            else:
                return ts

    @staticmethod
    def is_number(content):
        try:
            float(content)
        except:
            return False
        else:
            return True

    def __str__(self):
        return self._datetime.isoformat(' ')[:19] if self._datetime else ""

    def __repr__(self):
        return '<{0} [{1}]>'.format(self.__class__.__name__, self.__str__())

    def __eq__(self, other):
        return self._timestamp == other._timestamp

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self._timestamp > other._timestamp

    def __ge__(self, other):
        return self._timestamp >= other._timestamp

    def __lt__(self, other):
        return self._timestamp < other._timestamp

    def __le__(self, other):
        return self._timestamp <= other._timestamp

    def __add__(self, other):
        return CTime(self._timestamp + other._timestamp)

    __radd__ = __add__

    def __sub__(self, other):
        return self._datetime - other._datetime

    def __rsub__(self, other):
        return other._datetime - self._datetime

    def __format__(self, format_spec):
        return self._datetime.strftime(format_spec)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            return self._datetime.__getattribute__(item)


ctime = CTime


if __name__ == "__main__":
    ctime()
