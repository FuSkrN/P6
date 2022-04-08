#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

int x = 0;
int y = 0;

void *modifyX();
void modifyY();

int main() {
    pthread_t thread1;
    pthread_t thread2;

    int elist[] = {};

    pthread_create(&thread1, NULL, modifyX, (void*) elist);
    pthread_join(thread1, NULL);

    pthread_create(&thread2, NULL, modifyX, (void*) elist);
    pthread_join(thread2, NULL);

    print("x: %d\n", x);
    print("y: %d\n", y);

    return 0;
}

void *modifyX() {
    int a = 10;
    int b;

    a = a + 5;
    b = a - 3;
    x = b;
}

void *modifyY() {
    int a = 10;
    y = y + a;
    x = x - 1;
}