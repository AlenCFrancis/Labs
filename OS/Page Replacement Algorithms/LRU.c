#include <stdio.h>

int main()
{
    int pages[50], frames[10], time[10];
    int n, f, i, j;
    int hit, count = 0, pos, min;
    int page_faults = 0;

    printf("Enter number of pages: ");
    scanf("%d", &n);

    printf("Enter number of frames: ");
    scanf("%d", &f);

    printf("Enter page reference string:\n");
    for(i = 0; i < n; i++)
        scanf("%d", &pages[i]);
    
    for(i = 0; i < f; i++)
    {
        frames[i] = -1;
        time[i] = 0;
    }

    printf("\nPage\tFrames\t\tStatus\n");

    for(i = 0; i < n; i++)
    {
        hit = 0;

        
        for(j = 0; j < f; j++)
        {
            if(frames[j] == pages[i])
            {
                hit = 1;
                time[j] = count++;
                break;
            }
        }

        if(hit == 0)
        {
            page_faults++;

            pos = -1;
            for(j = 0; j < f; j++)
            {
                if(frames[j] == -1)
                {
                    pos = j;
                    break;
                }
            }

            if(pos != -1)
            {
                frames[pos] = pages[i];
                time[pos] = count++;
            }
            else
            {
                
                min = time[0];
                pos = 0;

                for(j = 1; j < f; j++)
                {
                    if(time[j] < min)
                    {
                        min = time[j];
                        pos = j;
                    }
                }

                frames[pos] = pages[i];
                time[pos] = count++;
            }
        }

        printf("%d\t", pages[i]);

        for(j = 0; j < f; j++)
        {
            if(frames[j] == -1)
                printf("- ");
            else
                printf("%d ", frames[j]);
        }

        if(hit)
            printf("\tHIT");
        else
            printf("\tFAULT");

        printf("\n");
    }

    printf("\nTotal Page Faults = %d\n", page_faults);
    printf("Total Hits = %d\n", n - page_faults);

    return 0;
}
