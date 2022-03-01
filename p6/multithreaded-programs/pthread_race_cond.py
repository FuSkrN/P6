import threading
n = 0

class summationThread(threading.Thread):
    def __init__(self, threadID, name, counter,\
            sumRange):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.sumRange = sumRange
    def run(self):
        #print("Starting " + self.name)
        print(f'Thread {self.name} adding {sumNumbers(self.threadID, self.sumRange)} to sumArray[{self.threadID % 5}].')
        #print("Exiting " + self.name)

def sumNumbers(threadID, numberRange):
    global sumArray
    summedNumber = sumArray[threadID % 5]
    for x in numberRange:
        summedNumber += x
    sumArray[threadID % 5] = summedNumber
    return summedNumber

threads = []

sumArray = [0]*5

for x in range(1, 100):
    threads.append(summationThread(x, f"thread-{x}", x,\
            range((x-1)*1000000+1, x*1000000+1)))

for thread in threads:
    thread.start()


for thread in threads:
    thread.join()

for summation in sumArray:
    print(f"adding {summation} to n")
    n += summation

print(n)
