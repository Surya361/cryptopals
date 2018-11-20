#include<stdio.h>
#include<stdlib.h>
#include<time.h>

int guess()
{
	int r = (rand() % 38) + 2;
}

int hammind_distance(unsigned char *a, unsigned char *b, int slen)
{
	unsigned char final[100];
	int i =0,c=0;
	int distance = 0;
	while (i < slen)
	{
		final[i] = (a[i]^b[i]);
		for (; final[i]; distance++)
			final[i] &= final[i]-1;

		i++;

	}
	return distance;

}

int main()
{
	int distance = hammind_distance("this is a test","wokka wokka!!!",14);
	printf("%d\n",distance );
}