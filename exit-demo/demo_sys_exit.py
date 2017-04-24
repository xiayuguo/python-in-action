import os
import sys

from threading import Thread


def func():
    try:
        sys.exit(1)
    except SystemExit as e:
        print(e)
t = Thread(target=func)
print("test exit start...")
t.start()
t.join()
print("test exit finish...")
