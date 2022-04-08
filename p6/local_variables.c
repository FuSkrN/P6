#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>

void *func();

int main(void){
    pthread_t thread1;
    pthread thread2;
    int arg1[] = {};
    
    pthread_create(&thread1, NULL, func, (void*) arg1);
    pthread_create(&thread2, NULL, func, (void*) arg1);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
}

void *func(){
    int a = 0;
    int b = 10;
    double x = 0.5;
    y = 3.14;
    
    //random math
    a = a + 7;
    b = b + a;
    a = b - a;
    a = a + a;
    b = b * a;

    x = x * y;
    y = x* x;
}
