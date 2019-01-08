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


class IRainTime(object):
    """ Convert all displays of time to datetime
        Examples:
        >>> import time
        >>> from datetime import datetime
        >>> from irain_lib.iraintime import iraintime
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
        >>> iraintime(iraintime('2018-05-08'))
        <IRainTime [2018-05-08 00:00:00]>
        >>> a = iraintime()
        >>> b = iraintime()
        >>> a
        <IRainTime [2018-07-25 09:53:23]>
        >>> b
        <IRainTime [2018-07-25 09:53:30]>
        >>> a < b
        True
        >>> a <= b
        True
        >>> a + b
        <IRainTime [2067-02-15 11:46:53]>
        >>> b - a
        datetime.timedelta(0, 6, 601950)
        >>> format(iraintime(), '%Y%m%d%H%M%S')
        '20180725102809'
        >>>iraintime().grape
        '180725102848'

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
        elif isinstance(time_data, IRainTime):
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

    @property
    def grape(self):
        """Tianyun's special attribute"""
        return format(self, '%y%m%d%H%M%S')

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
        return IRainTime(self._timestamp + other._timestamp)

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


iraintime = IRainTime


class TimeRange(object):
    """时间范围处理工具(交集，并集，补集, ...)

    Examples:
    >>> from irain_lib.iraintime import TimeRange
    >>> A = TimeRange("2018-09-01", "2018-10-01")
    >>> B = TimeRange("2018-09-15", "2018-09-20")
    >>> A & B
    [<IRainTime [2018-09-15 00:00:00]>, <IRainTime [2018-09-20 00:00:00]>]

    """
    def __init__(self, start_time, end_time):
        self.start_time = iraintime(start_time)
        self.end_time = iraintime(end_time)
        self.time_list = [self.start_time, self.end_time]

    def __and__(self, other):
        """交集"""
        start_time = max(self.start_time, other.start_time)
        end_time = min(self.end_time, other.end_time)
        if start_time < end_time:
            return [start_time, end_time]
        else:
            return []

    def __getitem__(self, item):
        return self.time_list[item]

    def __repr__(self):
        return f"<TimeRange({self.start_time}, {self.end_time})>"

    __str__ = __repr__


class AuthTime(object):
    def __init__(self, sday, eday, time_range, day_of_week):
        self.sday = iraintime(sday)
        self.eday = iraintime(eday)
        if isinstance(time_range, str):
            self.start_time, self.end_time = time_range.split(",")
        else:
            self.start_time, self.end_time = time_range
        if isinstance(day_of_week, str):
            self.day_of_weekday = list(map(int, day_of_week.split(",")))
        else:
            self.day_of_weekday = list(map(int, day_of_week))
        self.valid_list = self._get_valid_time_list()

    def _daterange(self, start_date, end_date):
        """生成器: 处理日期遍历"""
        for n in range(int((end_date - start_date).days + 1)):
            yield start_date + timedelta(n)

    def _dateslice(self, date_list):
        """给不连续的时间序列分段"""
        tmp = []
        for index, _ in enumerate(date_list):
            if index == 0 or date_list[index] - date_list[index - 1] != timedelta(1):
                tmp.append([date_list[index]])
            else:
                tmp[-1].append(date_list[index])
        return tmp

    def _get_valid_time_list(self):
        """授权记录拆分成连续时间段的多条记录
            (一天内不可以有两段授权时间段
            跨夜除外, 示例:
                传入:

                返回:

            )
        :return:
            :type TimeRange
                :param start_time: 有效开始时间
                :type start_time: DateTime String
                :param end_time: 有效截止时间
                :type end_time: DateTime String
        """

        # 1. 处理连续时间(连续时间以用户输入的sday, eday为开始时间和结束时间)
        if len(self.day_of_weekday) == 7 and self.start_time == "00:00:00" and self.end_time == "23:59:59":
            return [TimeRange(f"{str(self.sday)[:10]} 00:00:00",
                              f"{str(self.eday)[:10]} 23:59:59")]

        valid_dates = [
            x for x in self._daterange(
                iraintime(self.sday)._datetime,
                iraintime(self.eday)._datetime
            ) if x.isoweekday() in self.day_of_weekday
        ]
        if self.start_time < self.end_time:
            # 还要判断时间是否连续 00:00:00 23:59:59;
            def comp_time(item):
                sday, eday = str(iraintime(item[0]))[:10], str(iraintime(item[-1]))[:10]
                return TimeRange(
                    iraintime("{0} {1}".format(sday, self.start_time)),
                    iraintime("{0} {1}".format(eday, self.end_time))
                )

            if self.start_time == "00:00:00" and self.end_time == "23:59:59":
                validity_list = list(map(comp_time, self._dateslice(valid_dates)))
            else:
                validity_list = list(map(comp_time, [(x, x) for x in valid_dates]))
        else:
            validity_list = [TimeRange(
                iraintime(f"{str(iraintime(x))[:10]} {self.start_time}"),
                iraintime(f"{str(iraintime(x + timedelta(1)))[:10]} {self.end_time}")
            ) for x in valid_dates]
        return validity_list

    @property
    def sum_days(self):
        return self._sum_auth_date()

    def _sum_auth_date(self):
        """获得全部授权有效天数

        计算规则:
            每个授权段中, 授权结束时间 - 授权开始时间, 差值少于一天的按一天算;
            多于一天并有零头(少于一天)的时间, 向下取整;
            然后累加各个段获得的天数.

        :param auth_time_list: 授权有效期列表
        :param auth_time_list: List 示例: [("2017-09-09 10:00:00", "2017-09-09 20:00:00"),
                                          ("2017-09-19 10:00:00", "2017-09-29 10:00:00")]
        :return:
            :param days: 天数
            :param days: Int
        """

        def get_days(start_time, end_time):
            tmp_days = end_time - start_time
            if tmp_days.days:
                return tmp_days.days
            elif tmp_days.days == 0 and tmp_days.seconds != 0:
                return 1
            else:
                return 0

        if self.valid_list:
            days = sum([get_days(x[0], x[1]) for x in self.valid_list])
            return days
        else:
            return 0

    def isdisjoint(self, other):
        """判断两个集合是否不相交"""
        return False if self & other else True

    def __and__(self, other):
        if all((self.sday == other.sday,
                self.eday == other.eday,
                self.start_time == other.start_time,
                self.end_time == other.end_time,
                self.day_of_weekday == other.day_of_weekday)):
            return self.valid_list
        else:
            valid_list = []

            def cmp(x, y):
                intersection = x & y
                if intersection:
                    valid_list.append(intersection)
                return y

            sorted_list = sorted(self.valid_list + other.valid_list, key=lambda x: x.start_time)
            reduce(cmp, sorted_list)
            return valid_list

    def __repr__(self):
        return f"<AuthTime(sday={self.sday}, " \
               f"eday={self.eday}, " \
               f"start_time={self.start_time}, " \
               f"end_time={self.end_time}, " \
               f"day_of_week={self.day_of_weekday})>"

    __str__ = __repr__


if __name__ == "__main__":
    iraintime()
