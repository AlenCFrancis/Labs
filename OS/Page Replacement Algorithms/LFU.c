#include <stdio.h>

int main()
{
    int pages[50], frames[10], freq[10];
    int n, f, i, j, k;
    int hit = 0, found, pos, min;

    printf("Enter number of pages: ");
    scanf("%d", &n);

    printf("Enter number of frames: ");
    scanf("%d", &f);

    printf("Enter page reference string:\n");
    for(i = 0; i < n; i++)
        scanf("%d", &pages[i]);

    // Initialize
    for(i = 0; i < f; i++)
    {
        frames[i] = -1;
        freq[i] = 0;
    }

    printf("\nPage\tFrames\t\tStatus\n");

    // Process pages
    for(i = 0; i < n; i++)
    {
        found = 0;

        // Check HIT
        for(j = 0; j < f; j++)
        {
            if(frames[j] == pages[i])
            {
                hit++;
                freq[j]++;   // increase frequency
                found = 1;
                break;
            }
        }

        // PAGE FAULT
        if(found == 0)
        {
            // Check empty frame first
            pos = -1;
            for(j = 0; j < f; j++)
            {
                if(frames[j] == -1)
                {
                    pos = j;
                    break;
                }
            }

            // If empty frame exists
            if(pos != -1)
            {
                frames[pos] = pages[i];
                freq[pos] = 1;
            }
            else
            {
                // Find least frequency
                min = freq[0];
                pos = 0;

                for(j = 1; j < f; j++)
                {
                    if(freq[j] < min)
                    {
                        min = freq[j];
                        pos = j;
                    }
                }

                // Replace
                frames[pos] = pages[i];
                freq[pos] = 1;
            }
        }

        // Print frames
        printf("%d\t", pages[i]);
        for(k = 0; k < f; k++)
        {
            if(frames[k] == -1)
                printf("- ");
            else
                printf("%d ", frames[k]);
        }

        if(found)
            printf("\tHIT");
        else
            printf("\tFAULT");

        printf("\n");
    }

    printf("\nTotal Hits = %d", hit);
    printf("\nTotal Page Faults = %d\n", n - hit);

    return 0;
}
