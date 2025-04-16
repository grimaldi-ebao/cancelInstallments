#!/usr/bin/python

import threading
import time

def worker():
    if l._RLock__owner is threading.current_thread():
        print ("I own the lock")
    else:
        print ("I don't own the lock")
    l.acquire()
    if l._RLock__owner is threading.current_thread():
        print ("Now I own the lock")
    else:
        print ("Now I don't own the lock")
    time.sleep(5)
    l.release()

if __name__ == "__main__":
    l = threading.RLock()
    thds = []
    for i in range(0, 2): 
        thds.append(threading.Thread(target=worker))
        thds[i].start()

    for t in thds:
        t.join()