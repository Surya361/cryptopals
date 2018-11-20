#include<stdio.h>
#include<stdlib.h>

void main()
{
	FILE *p;
	p = fopen("file","r");
	//char test[300];
	unsigned char test[300];
	fread(&test[0],1,100,p);
	printf("%s",test);
}