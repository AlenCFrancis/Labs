#include <stdio.h>

int main()
{
    int referenceString[50], frame[50];
    int pageFaults = 0, pages, frames;
    int i, j, k, m, found, pos = 0;

    printf("\nEnter the number of Pages: ");
    scanf("%d", &pages);

    printf("\nEnter reference string values:\n");
    for(i = 0; i < pages; i++)
    {
        scanf("%d", &referenceString[i]);
    }

    printf("\nEnter the number of Frames: ");
    scanf("%d", &frames);

    
    for(i = 0; i < frames; i++)
    {
        frame[i] = -1;
    }

    for(i = 0; i < pages; i++)
    {
        found = 0;


        for(j = 0; j < frames; j++)
        {
            if(frame[j] == referenceString[i])
            {
                found = 1;
                break;
            }
        }

        if(found == 0)
        {
            frame[pos] = referenceString[i];
            pos = (pos + 1) % frames; 
            pageFaults++;
        }


        printf("\nFrame status: ");
        for(j = 0; j < frames; j++)
        {
            if(frame[j] != -1)
                printf("%d ", frame[j]);
            else
                printf("- ");
        }
    }

    printf("\n\nTotal Page Faults: %d\n", pageFaults);

    return 0;
}
