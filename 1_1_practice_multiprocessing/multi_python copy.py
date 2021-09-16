from multiprocessing import Process, Queue
import sys, time

class WrongAttributeException(Exception):
    # When the program is given a wrong command input
    pass


## This function was defined to handle the case
## that the input command is single.
def work1(num):
    summation = 0
    for i in range(1, num+1):
        summation += i
    return summation


## This function was defined to handle the case
## that the input command is multi.
def work2(id, queue, start, end):
    mid = 0
    for i in range(start+1, end+1):
        mid += i
    queue.put(mid)
    return


## This Section was defined for main function
def main(args):
    # The number of input command elements always
    # should be 3.
    if len(args) > 3: # ["multi2.py", "single", "1000000"] (for example)
        raise WrongAttributeException("Given 2 more arguments. Expected is 2 arguments.")
    
    # For Single Processing
    elif args[1].lower() == "single":
        _TIME1 = time.time()
        result = work1(int(args[2]))
        _TIME2 = time.time()
        return result, _TIME2 - _TIME1
    
    # For Multi Processing
    elif args[1].lower() == "multi":
        queue = Queue()
        tasks = []
        num = int(args[2])

        # If input number is under 8,
        # then it needs not to use multiprocessing
        # Actually, this number doesn't have to be 8
        # You can choose a number you want.
        if num < 8:
            _TIME1 = time.time()
            result = work1(int(args[2]))
            _TIME2 = time.time()
            return result, _TIME2 - _TIME1
        
        _TIME1 = time.time()
        for i in range(8):
            thrd = Process(target=work2, args = (i, queue, (num*i)//8, (num*(i+1))//8 ))
            # 100000
            # 0~12500, 12500 ~ 25000, ...
            tasks.append(thrd)
            thrd.start()

        for task in tasks:
            task.join()

        # To imprint the end sign at last cell
        queue.put("END")
        result = 0
        
        # Join the results computed by the threads
        while True:
            mid = queue.get()
            if mid == "END":
                _TIME2 = time.time()
                return result, _TIME2 - _TIME1
            result += mid
    
    else:
        ## If the command elements are lacked
        raise WrongAttributeException(f"Not Listed option")

if __name__ == '__main__':
    args = sys.argv
    #print(args)
    result, ex_time = main(args)
    print(f"SUM of 0 ~ {args[2]} : {result} in {ex_time:.5f} sec")