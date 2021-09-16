import time, sys
from multiprocessing import Process
#Thread,threading

def single():
    result = 0
    for i in range(1, n+1):
        result += i/
        # print(f"At/1 : {}i")
def multi(id, start, end): # id는 몇번째 쓰레드를 활성화할건지, start end는 나눠서 관리
    result = 0
    for i in range(start, end+1):
        print(f"At {id} : {i}")
        # result += i
        return

def main(arg = None, n = 16):
    n = int(n)

    if (n%8 != 0):
        print("Wrong Value: n")
        sys.exit(1)
    if  (arg == "single"):
        _TIME = time.time()
        single(n)
        _TIME2 = time.time()

    elif (arg == "multi"):
        tasks = []

        _TIME = time.time()
        for i in range(1,9):
            thread = Process(target = multi, args = (i, (i-1)*n//8, i*n//8))
            tasks.append(thread)
            thread.start()
        
        # thrd = Process(target=multi, args=(i))
        # for문을 사용하지 않는다면,,,
        # thrd1 = Process(target=multi, args=(i))
        # thrd2 = Process(target=multi, args=(i))
        # thrd3 = Process(target=multi, args=(i))



        # _TIME2 = time.time()
        for task in tasks:
            task.join()
        _TIME2 = time.time()

    else:
        print("Wrong Argument")
        sys.exit()

    print(f"RESULT : {_TIME2 - _TIME} sec")

if __name__ = '__main__':
    _val = sys.argv
    # print(_val)
    main(_val[1], _val[2])

