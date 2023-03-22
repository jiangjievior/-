import threading,queue

#1.用于测试的函数
def print_number(i):
    for _ in range(10):

        print(f'执行线程{i}')


threads=[]
for j in range(1,3):
    t=threading.Thread(target=print_number,args=(j,))
    t.start()
    threads.append(t)


#保证执行完子线程再执行主线程
for thread in threads:
    thread.join()

print('主线程执行')

k=2


#2.当函数具有return的返回值
q=queue.Queue()
def return_number(i,q):
    for _ in range(10):
        print(f'执行线程{i}')

    return q.put(f'线程{i}')


threads = []
results = []
for i in range(10):
    t = threading.Thread(target=return_number, args=(i, q))
    t.start()
    threads.append(t)

for thread in threads:
    thread.join()  # 等待子线程结束后，再往后面执行

for _ in range(10):
    results.append(q.get())#通过q获得返回值
print(results)
























