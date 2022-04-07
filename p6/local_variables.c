#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>

void *func(void *args);

int main(void){
    pthread_t thread1, thread2;
    int res1, res2;
    int arg1[] = {10};
    
    pthread_create(&thread1, NULL, func, (void*) arg1);
    pthread_join(thread1, NULL);
    printf("%d\n", arg1[0]); 
}

void *func(void *args){
    int* a = (int*)args;
    a += 10;
    printf("its this one: %d\n", a);
}
