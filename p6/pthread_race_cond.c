#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

long totalSum = 0;

void *sumNumbers(void *);

int main(){
    pthread_t thread1, thread2;
    int arg1[] = {1, 1000000};
    int arg2[] = {1000001, 2000000};
    int iret1, iret2;
    pthread_t threads[10];

    iret1 = pthread_create(&thread1, NULL, sumNumbers, (void*) arg1);
    iret2 = pthread_create(&thread2, NULL, sumNumbers, (void*) arg2);
    
    for(int x=0; x<10; x++){
        pthread_create(&threads[x], NULL, sumNumbers, (void*) arg1);
    }

    totalSum += pthread_join(thread1, NULL);
    totalSum += pthread_join(thread2, NULL);

    for(int x=0; x<10; x++){
        pthread_join(threads[x], NULL);
    }

    printf("%d\n", &totalSum);

	return 0;
}

void *sumNumbers(void *args){
    int sum = 0;
    int *arr = (int *) args;
    for(int x = arr[0]; x <= arr[1]; x++){
        sum += x;
    }
    printf("%ld\n", &totalSum);
    printf("%d", &sum);
    totalSum += sum;
}

/*import threading
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

#threads = []

#sumArray = [0]*5

#for x in range(1, 100):
#    threads.append(summationThread(x, f"thread-{x}", x,\
#            range((x-1)*1000000+1, x*1000000+1)))
#
#for thread in threads:
#    thread.start()


#for thread in threads:
#    thread.join()
#
#for summation in sumArray:
#    print(f"adding {summation} to n")
#    n += summation

#print(n)
*/
