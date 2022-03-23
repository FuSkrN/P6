#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

int x = 0;
int y = 0;

void *setX();
void *setY();

int main(){
    pthread_t thread1;
	pthread_t thread2;
    int arg1[] = {1, 1000000};
    int arg2[] = {1000001, 2000000};
    int iret1;
	int iret2;

    iret1 = pthread_create(&thread1, NULL, setX, (void*) arg1);
    iret2 = pthread_create(&thread2, NULL, setY, (void*) arg2);
    
    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

	printf("%d\n", x);
    printf("%d\n", y);

	return 0;
}

void *setX(){
	int a = 5;
	int b;

	a = a + 10;
	b = a - 5;
	x = b;
}

void *setY(){
	int a = 5;
	x = x + a;
	y = x;
	x = x - 10;
}


