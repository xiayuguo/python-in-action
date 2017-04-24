import os
import sys
import traceback

from threading import Thread


def func():
    try:
        os._exit(1)
    except SystemExit as e:
        print(e)
t = Thread(target=func)
print("test exit start...")
t.start()
t.join()
print("test exit finish...")
