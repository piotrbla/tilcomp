#include <stdio.h>

int main(void)
{
    int tabA[10][10];
    int tabB[10][10];
    int tabResult[10][10];
    int n=10;
    int m=10;


    for (i=0 ; i<n ; i++)
    {
        for (j=0 ; j<m ; j++)
        {
            tabResult [i][j]=0;
            for(k=0 ; k< n ; k++)
            {
                tabResult [i][j] += tabA[i][k] * tabB [k][j];
            }
        }
    }
    return 0;
}