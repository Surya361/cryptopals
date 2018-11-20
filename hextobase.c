#include<stdio.h>
#include<stdlib.h>
#include<string.h>

static const char coding[] = {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S',\
		'T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p'\
		,'q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','+','/'};

void encode(unsigned char *in, unsigned char *out, int len)
{
	out[0] = coding[(int) (in[0] >> 2)];
	out[1] = coding[(int) (((in[0] & 0x03) << 4) | (in[1] >> 4) )];
	out[2] = len > 1 ? coding[(int) ((in[1] & 0x0f) << 2) | ((in[2] & 0xc0) >> 6)] : '=';
	out[3] = len > 2 ? coding[(int) (in[2] & 0x3f)] : '=';
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

void main()
{
	unsigned char in[100];
	char buf[200];
	scanf("%s",buf);
	int s_len = strlen(buf)/2;
    int i = 0; 
    hexdecode(buf,in);
	unsigned char out[4];
	
	for(i =0; i < s_len/3; i++)
	{
		encode(&in[i*3], &out[0],3);
		printf("%s",&out[0]);
	}
	if((s_len % 3) != 0)
	{
		encode(&in[ i*3 ],&out[0],s_len%3);
		printf("%s\n",&out[0]);
	}
	//fclose(p);

}

