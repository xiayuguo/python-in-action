# Convert seconds to time

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