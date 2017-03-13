#!/usr/bin/python
# coding:utf8

import os
import sys
import time
import fcntl


class FLOCK(object):
    def __init__(self, name):
        """
        :param name: 文件名
        """

        self.fobj = open(name, 'a')
        self.fd = self.fobj.fileno()

    def lock(self):
        try:
            fcntl.lockf(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)  # 给文件加锁，使用了fcntl.LOCK_NB
            print u'给文件加锁, 稍等...'
            time.sleep(5)
            return True
        except:
            print u'文件加锁, 无法执行, 请稍后运行'
            return False

    def unlock(self):
        try:
            fcntl.flock(self.fd, fcntl.LOCK_UN) # 给文件解锁, 使用了fcntl.LOCK_UN
            print u'给文件解锁, 稍等...'
            print u'已解锁'
        except:
            print u'文件无法解锁, 请稍后运行'
        finally:
            self.fobj.close()


if __name__ == "__main__":
    print sys.argv[0]
    locker = FLOCK(sys.argv[0])
    a = locker.lock()
    if a:
        print u'文件已加锁'
        time.sleep(5)
        locker.unlock()
    else:
        print u'无法执行，程序已锁定，请稍等'