import time

start_time = time.time()

def count(name):
    for i in range(1, 50001):
        print(name, " : ",i)
num_list = ['p1','p2','p3','p4']
for num in num_list:
    count(num)

print("---%s seconds ---" % (time.time() - start_time))