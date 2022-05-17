#include <stdlib.h>
#include <pthread.h>

int x = 0;

void *f();
void *g();

int main(){
    pthread_t thread1;
    pthread_t thread2;
    int arg1[] = {};

    pthread_create(&thread1, NULL, f, (void*) arg1);
    pthread_create(&thread2, NULL, g, (void*) arg1);
    
    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
    return 0;
}

void *f(){
    int a = 5;
    x = a;
}

void *g(){
    int b = 10;
    x = b;
}


