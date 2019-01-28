# How to Convert Time in Python

## Python 中涉及的几种时间类型
- time string
```python
>>> import time
>>> time.ctime()
'Thu May 18 18:44:39 2017'
```
- datetime tuple(datetime obj)
```python
>>> from datetime import datetime
>>> datetime.now()
datetime.datetime(2017, 5, 18, 18, 43, 29, 275094)
```
- time tuple(time obj)
```python
>>> import time
>>> time.strptime("18 May 17", "%d %b %y")
time.struct_time(tm_year=2017, tm_mon=5, tm_mday=18, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=138, tm_isdst=-1)
```
- timestamp
```python
>>> import time
>>> time.time()
1495104456.522384
```

## 四种类型之间的转换
```seq
Datetime -> String: dt_obj.striftime()
Datetime -> Time: dt_obj.timetuple()
Datetime -> Timestamp: 待定
String -> Datetime: datetime.datetime.strptime(str, format)
String -> Time: time.strptime(str, format)
String -> Timestamp: 待定
Time -> Datetime: datetime.datetime(t_obj)
Time -> String: time.strptime(format, t_obj)
Time -> Timestamp: time.mktime(t_obj)
Timestamp -> Datetime: datetime.datetime.fromtimestamp(ts)
Timestamp -> String: 待定
Timestamp -> Time: time.gmtime(ts)
```

## Convert seconds to time
- 方案一：
```python
import time
output = time.strftime('%H:%M:%S', time.gmtime(12345))
```

- 方案二
```python
m, s = divmod(12345, 60)
h, m = divmod(m, 60)
output = "%02d:%02d:%02d" % (h, m, s)
```

> 当时间在24小时内，两个方案的结果都正确，但是超出时，方案一只取出时分秒的数据，而忽略了年月日，方案二则将多余的小时都堆积到小时这个单位中

- 特殊情况示例
```bash
$ python second2time.py 6666666
output is 03:51:06 from No.1
output is 1851:51:06 from No.2
```

## ctime.py
该文件是各种时间转化成标准时间的大集合
```python
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
```