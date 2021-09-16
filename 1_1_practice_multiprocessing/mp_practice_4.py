import time, sys
from multiprocessing import Process

# Thread, Threading, Pool

def single(n):
    result = 0
    for i in range(1, n+1):
        result +=i
        #print(f"At 1 :{i}")


def multi(id, start, end):
    result = 0
    for i in range(start, end+1):
        # print(f"At {id} : {i}")
        result += i
    return

def main(arg = None, n = 16):
    n =int(n)