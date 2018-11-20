#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<ctype.h>

int freq_score[] = {81,14,27,42,127,22,20,60,69,1,7,40,24,67,75,19,0,59,63,90,27,9,23,1,19,0};
unsigned char final_decrypt[200];
int high;

int scoreof(int a)
{
	int b = tolower(a);

	if (b >= 97 && b <= 122)
	{
		//printf("***%d***",b);
		return freq_score[b - 97];
	}
	else
	if (b == 32)
		return 232;
	return 0;
}

void hexdecode(char *in, char *out)
{
	int i=0, j=0;

	 while (in[i] != '\0') 
	 {
        int b;
        sscanf(&in[i], "%2x", &b);
        out[j] = b;
        i += 2;
        j++;
    }
}

int twoxor(char *one, char *two, char *exor, int len)
{
	int i = 0;
	int score = 0;
	while(i < len)
	{
		exor[i] = one[i] ^ *two;
		score += scoreof(exor[i]);
		i++;
	}
	return score;
}

void brute(char *a, int len)
{
	unsigned char key = 0x00;
	int score;
	unsigned char decrypted[100];
	int highest = 0;
	while (key != 255)
	{
		unsigned char final[100];
		score = twoxor(a,&key,final,len);
		if(score > highest)
		{
			strcpy(decrypted,final);
			highest = score;
		}
		key = key + 0x01;
	}
	if(high < highest)
	{
		strcpy(final_decrypt,decrypted);
		high = highest;
	}
}

FILE * file_open(char *s)
{
	FILE *p;
	p = fopen("4.txt","r");
	if(p == NULL)
		exit (1);
	return p;
}

void main()
{

	FILE *fp;
	unsigned char in1[100],final[100], pri[100];
	char buf1[200];
	fp = file_open("4.txt");
	while(fgets(&buf1[0],200,fp))
	{
		int s_len = strlen(buf1)/2;
    	hexdecode(buf1,in1);
    	brute(in1,s_len);
    	//free(buf1);
	}
	printf("%s\n",final_decrypt);
	
}

