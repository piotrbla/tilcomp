#include <stdio.h>

int main(void)
{
    int tabA[10][10];
    int tabB[10][10];
    int tabResult[10][10];
    int n=10;
    int m=10;
    int i, j, k;


    for (i=0 ; i<n ; i++)
    {
#pragma scop
        for (j=0 ; j<m ; j++)
        {
            tabResult [i][j]=0;
            for(k=0 ; k< n ; k++)
            {
                tabResult [i][j] += tabA[i][k] * tabB [k][j];
            }
#pragma endscop
        }
        printf("tabresult 22 value: %d", tabResult [2][2] )
    }
    printf("tabresult 00 value: %d", tabResult [0][0] )
    return 0;
}