#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

long totalSum = 0;

void *sumNumbers(void *);

int main(){
    pthread_t thread1, thread2;
    int arg1[] = {1, 1000};
    int arg2[] = {1001, 2000};
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

    printf("totalSum at the end: %d\n", &totalSum);

	return 0;
}

void *sumNumbers(void *args){
    int sum = 0;
    int *arr = (int *) args;
    for(int x = arr[0]; x <= arr[1]; x++){
        sum += x;
    }
    printf("totalsum: %ld\n", &totalSum);
    printf("sum: %d\n", &sum);
    totalSum += sum;
}
