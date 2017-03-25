#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------
# DESCRIPTION
# ===========
# result
# ('Size of pool', 4)
# ('Size of pool', 4)
# ('Size of pool', 4)
# ('Size of pool', 4)
# ('Size of pool', 4)
# ('Size of pool', 4)
# ('Size of pool', 4)
# ('Size of pool', 4)
# ('Size of pool', 2)
# ('Size of pool', 2)
# Hello, 0
# Hello, 1
# Hello, 2
# Hello, 3
# Hello, 4
# Hello, 5
# Hello, 6
# Hello, 7
# Hello, 8
# Hello, 9
# Size of gevent pool is 4
# Total jobs is 10
# Cost time: 3.00399494171
# ----------------------------------------

# build-in, 3rd party and my modules
import time
import gevent
from gevent.pool import Pool


POOL_SIZE = 4
TOTAL_JOBS = 10

pool = Pool(POOL_SIZE)


def hello_from(n):
    gevent.sleep(1)
    print('Size of pool', len(pool))
    return "Hello, %s" % n


def test():
    start_time = time.time()
    greenlets = []
    for i in xrange(TOTAL_JOBS):
        # <Greenlet at 0x10c3ca2d0: hello_from(8)>
        greenlet = pool.spawn(hello_from, i)
        greenlets.append(greenlet)

    pool.join()
    for greenlet in greenlets:
        print greenlet.value

    print "Size of gevent pool is %s" % POOL_SIZE
    print "Total jobs is %s" % TOTAL_JOBS
    print "Cost time: %s" % (time.time() - start_time)


# ----------------------------------------
# test cases
# ----------------------------------------
def run_doctest():
    '''python -B <__file__> -v
    '''
    import doctest
    doctest.testmod()


if '__main__' == __name__:
    test()

