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