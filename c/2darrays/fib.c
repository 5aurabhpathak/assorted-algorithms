#include<stdio.h>

void printFibonacci(int);

int main(){

    int n;

    printf("Enter the range of the Fibonacci series: ");
    scanf("%d",&n);

    printf("Fibonacci Series: ");
    printf("%d %d ",0,1);
    printFibonacci(n);
	printf("\n");

    return 0;
}

void printFibonacci(int n){

    static int first=0,second=1,sum;

    if(n>0){
         sum = first + second;
         first = second;
         second = sum;
         printf("%d ",sum);
         printFibonacci(n-1);
    }

}
