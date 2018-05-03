# coding:utf-8

import sys
import time

tuple()
from datetime import datetime


seconds = 12345
if len(sys.argv) == 2:
    seconds = sys.argv[1]
    if seconds.isdigit():
        seconds = int(seconds)
    else:
        raise ValueError("input is error, %s is not digit" % seconds)

# 方案一
output = time.strftime('%H:%M:%S', time.gmtime(seconds))
print("output is %s from No.1" % output)


# 方案二
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
output_two = "%02d:%02d:%02d" % (h, m, s)
print("output is %s from No.2" % output_two)
