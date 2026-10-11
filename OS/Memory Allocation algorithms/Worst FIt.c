#include <stdio.h>

int main()
{
    int blockSize[25], originalBlockSize[25];
    int processSize[25], allocation[25], fragment[25];
    int numBlocks, numProcesses;
    int i, j;

    printf("Enter number of memory blocks: ");
    scanf("%d", &numBlocks);

    printf("Enter number of processes: ");
    scanf("%d", &numProcesses);

    printf("\nEnter sizes of memory blocks:\n");
    for(i = 0; i < numBlocks; i++)
    {
        printf("Block %d: ", i + 1);
        scanf("%d", &blockSize[i]);
        originalBlockSize[i] = blockSize[i];
    }

    printf("\nEnter sizes of processes:\n");
    for(i = 0; i < numProcesses; i++)
    {
        printf("Process %d: ", i + 1);
        scanf("%d", &processSize[i]);
        allocation[i] = -1;
        fragment[i] = 0;
    }

    for(i = 0; i < numProcesses; i++)
    {
        int worstIndex = -1;

        for(j = 0; j < numBlocks; j++)
        {
            if(blockSize[j] >= processSize[i])
            {
                if(worstIndex == -1 || blockSize[j] > blockSize[worstIndex])
                {
                    worstIndex = j;
                }
            }
        }

        if(worstIndex != -1)
        {
            allocation[i] = worstIndex;
            fragment[i] = blockSize[worstIndex] - processSize[i];
            blockSize[worstIndex] -= processSize[i];
        }
    }

    printf("\nPNo\tPSize\tBNo\tBSize\tFragment\n");
    for(i = 0; i < numProcesses; i++)
    {
        printf("%d\t%d\t", i+1, processSize[i]);

        if(allocation[i] != -1)
            printf("%d\t%d\t%d\n", allocation[i]+1, originalBlockSize[allocation[i]], fragment[i]);
        else
            printf("NA\tNA\tNA\n");
    }

    return 0;
}
