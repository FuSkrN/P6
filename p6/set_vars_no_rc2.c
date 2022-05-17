#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

int x = 0;
int y = 0;

void *modifyX();
void *modifyY();

int main() {
    pthread_t thread1;
    pthread_t thread2;
    pthread_t thread3;

    int elist[] = {};

    pthread_create(&thread1, NULL, modifyX, (void*) elist);
    pthread_join(thread1, NULL);

    pthread_create(&thread2, NULL, modifyY, (void*) elist);
    pthread_join(thread2, NULL);

    pthread_create(&thread3, NULL, modifyX, (void*) elist);
    pthread_join(thread3, NULL);

    printf("x: %d\n", x);
    printf("y: %d\n", y);

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
