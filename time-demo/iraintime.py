import sys
import time

from datetime import datetime, date


PY2, PY3 = 2, 3

if sys.version_info[0] == PY2:
    string_type = basestring
    number_type = (int, float, long)
else:
    string_type = str
    number_type = (int, float)


maxsize = sys.maxsize  # 32bit: 2147483647, 64bit: 9223372036854775807


class IRainTime(object):
    """ Convert all displays of time to datetime
        Examples:
        >>> import time
        >>> from datetime import datetime
        >>> from iraintime import iraintime
        >>> iraintime()
        <IRainTime [2018-05-03 10:55:07]>
        >>> iraintime(None)
        <IRainTime [2018-05-03 10:55:15]>
        >>> iraintime('2018-05-03 10:55:15')
        <IRainTime [2018-05-03 10:55:15]>
        >>> iraintime('2018-05-03T10:55:15')
        <IRainTime [2018-05-03 10:55:15]>
        >>> iraintime('2018-05-03T10:55:15.100000')
        <IRainTime [2018-05-03 10:55:15]>
        >>> iraintime('2018-05-03 10:55:15.100000')
        <IRainTime [2018-05-03 10:55:15]>
        >>> iraintime('2018-05-03')
        <IRainTime [2018-05-03 00:00:00]>
        >>> iraintime('10:55:15')
        <IRainTime [1900-01-01 10:55:15]>
        >>> iraintime(datetime.now())
        <IRainTime [2018-05-03 11:04:14]>
        >>> iraintime(time.time())
        <IRainTime [2018-05-03 11:04:22]>
        >>> iraintime(str(time.time()))
        <IRainTime [2018-05-03 11:04:29]>
        >>> iraintime(time.gmtime())
        <IRainTime [2018-05-03 03:06:23]>
        >>> str(iraintime(datetime.now()))
        '2018-05-03 11:15:09'
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
        else:
            raise TypeError("type %s not supported." % type(time_data))
        self._timestamp = time.mktime(self._datetime.timetuple())
        if self._timestamp > maxsize:
            raise ValueError('timestamp(%s) beyond the maxsize(%s)' % (self._timestamp, maxsize))

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
            if "-" in time_str and ":" in time_str and "T" in time_str:
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
        return self._datetime.isoformat(' ')[:19]

    def __repr__(self):
        return '<{0} [{1}]>'.format(self.__class__.__name__, self.__str__())

    def __eq__(self, other):
        return self._timestamp == other._timestamp

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self._timestamp > other._timestamp

    def __ge__(self, other):
        return self._timestamp >= self._timestamp

    def __lt__(self, other):
        return self._timestamp < other._timestamp

    def __le__(self, other):
        return self._timestamp <= other._timestamp

    def __add__(self, other):
        return IRainTime(self._timestamp + other._timestamp)

    __radd__ = __add__

    def __sub__(self, other):
        return IRainTime(self._timestamp - other._timestamp)

    def __rsub__(self, other):
        return IRainTime(other._timestamp - self._timestamp)


iraintime = IRainTime


if __name__ == "__main__":
    iraintime()
