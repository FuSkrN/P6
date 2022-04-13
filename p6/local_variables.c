#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>

void *func();

int main(void){
    pthread_t thread1;
    pthread_t thread2;
    int arg1[] = {};
    
    pthread_create(&thread1, NULL, func1, (void*) arg1);
    pthread_create(&thread2, NULL, func1, (void*) arg1);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
}

void *func1(){
    int a = 0;
    int b = 10;
    long x = 5;
    long y = 3;
    
    //random math
    a = a + 7;
    b = b + a;
    a = b - a;
    a = a + a;
    b = b * a;

    x = x * y;
    y = x * x;
}

