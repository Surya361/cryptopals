#include<stdio.h>
#include<stdlib.h>
#include<string.h>


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

void twoxor(char *one, char *two, char *exor, int len)
{
	int i = 0;
	while(i < len)
	{
		exor[i] = one[i] ^ two[i%3];
		i++;
	}
}

void ascii_to_hex(char *in, char *out, int len)
{
	int i = 0,j=0;
	while(i < len)
	{
		out[j] = (in[i] & 0xF0) >> 4;
		out[j+1] = (in[i] & 0x0F);
		i++;
		j = j+2;
	}
}

void main()
{
	unsigned char buf1[] = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal";
	unsigned char in1[200],final[200],pri[200];
	int s_len = strlen(buf1);
	//printf("%s\n",buf1);
    unsigned char key[] = "ICE";
    twoxor(buf1,key,final,s_len);
    ascii_to_hex(final,pri,s_len);

    int i=0;
    while(i < 2*s_len)
    {
    	printf("%x",pri[i]);
    	i++;
	}
}

