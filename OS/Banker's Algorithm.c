#include<stdio.h>

int max[10][10], alloc[10][10], need[10][10];
int avail[10];
int n, r;

void input();
void calculateNeed();
void display();
int safetyCheck();

int main()
{
    int i, p, req[15];
    char ch;
    
    printf("--Banker's Algorithm--\n");
    input();
    calculateNeed();
    display();
    
    if(safetyCheck())
    {
        printf("Safe state\n");
    }
    else
    {
        printf("Not Safe\n");
    }
    
    printf("\nNeed Resources ? y/n: ");
    scanf(" %c", &ch); 
    
    if(ch == 'y')
    {
        printf("Enter the Process NO: ");
        scanf("%d", &p);
        
        printf("Enter the request resources: ");
        for(i = 0; i < r; i++)
        {
            scanf("%d", &req[i]);
        }
        
        for(i = 0; i < r; i++)
        {
            alloc[p][i] += req[i];
            avail[i] -= req[i];
        }
        
        calculateNeed();
        display();
        
        if(safetyCheck()) {
            printf("Safe state\n");
        } else {
            printf("Not Safe\n");
        }
    }
    return 0;
}

void input()
{
    int i, j;
    printf("Enter the number of Process and Resources: ");
    scanf("%d %d", &n, &r);
    
    printf("Enter the Max Matrix:\n");
    for(i = 0; i < n; i++)
    {
        for(j = 0; j < r; j++)
        {
            scanf("%d", &max[i][j]);
        }
    }
    
    printf("Enter the Allocation Matrix:\n");
    for(i = 0; i < n; i++)
    {
        for(j = 0; j < r; j++)
        {
            scanf("%d", &alloc[i][j]);
        }
    }
    
    printf("Enter the Available Matrix:\n");
    for(i = 0; i < r; i++) 
    {
         scanf("%d", &avail[i]); 
    }
}

void calculateNeed()
{
    int i, j;
    for(i = 0; i < n; i++)
    {
        for(j = 0; j < r; j++)
        {
            need[i][j] = max[i][j] - alloc[i][j];
        }
    }
}

void display()
{
    int i, j;
    printf("\nProcess\tAlloc\t\tMax\t\tNeed\n");
    for(i = 0; i < n; i++)
    {
        printf("P%d\t", i);
        for(j = 0; j < r; j++)
        {
            printf("%d ", alloc[i][j]);
        }
        printf("\t\t");
        for(j = 0; j < r; j++)
        {
            printf("%d ", max[i][j]);
        }
        printf("\t\t");
        for(j = 0; j < r; j++)
        {
            printf("%d ", need[i][j]);
        }
        printf("\n");
    }
}

int safetyCheck()
{
    int work[10], finish[10] = {0}, safeseq[10];
    int i, j, count = 0;
    
    for(i = 0; i < r; i++) 
    {
        work[i] = avail[i];
    }
    
    while(count < n)
    {
        int found = 0;
        for(i = 0; i < n; i++)
        {
            if(!finish[i])
            {
                int possible = 1;
                for(j = 0; j < r; j++)
                {
                    if(need[i][j] > work[j])
                    {
                        possible = 0;
                        break;
                    }
                }
                if(possible)
                {
                    for(j = 0; j < r; j++)
                    {
                        work[j] += alloc[i][j];
                    }
                    safeseq[count++] = i;
                    finish[i] = 1;
                    found = 1;
                }
            }
        }
        if(!found) { 
            return 0; 
        }
    }
    
    printf("\nSafe Sequence = ");
    for(i = 0; i < n; i++)
    {
        printf("P%d ", safeseq[i]); 
    }
    printf("\n");
    
    return 1; 
}
