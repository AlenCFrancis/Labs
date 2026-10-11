#include <stdio.h>

int main()
{
    int process[30], burstTime[30], priority[30];
    int waitingTime[30], turnAroundTime[30];
    int n, i, j, temp;
    int totalWT = 0, totalTAT = 0;
    float avgWT, avgTAT;

    printf("Enter the number of processes: ");
    scanf("%d", &n);

    for(i = 0; i < n; i++)
    {
        process[i] = i + 1;
        printf("Enter burst time and priority of process %d: ", i + 1);
        scanf("%d %d", &burstTime[i], &priority[i]);
    }

    // Sort processes based on priority
    for(i = 0; i < n - 1; i++)
    {
        for(j = i + 1; j < n; j++)
        {
            if(priority[i] > priority[j])
            {
                temp = priority[i];
                priority[i] = priority[j];
                priority[j] = temp;

                temp = burstTime[i];
                burstTime[i] = burstTime[j];
                burstTime[j] = temp;

                temp = process[i];
                process[i] = process[j];
                process[j] = temp;
            }
        }
    }

    // Waiting time calculation
    waitingTime[0] = 0;

    for(i = 1; i < n; i++)
    {
        waitingTime[i] = waitingTime[i-1] + burstTime[i-1];
    }

    // Turnaround time calculation
    for(i = 0; i < n; i++)
    {
        turnAroundTime[i] = waitingTime[i] + burstTime[i];

        totalWT += waitingTime[i];
        totalTAT += turnAroundTime[i];
    }

    avgWT = (float)totalWT / n;
    avgTAT = (float)totalTAT / n;

    printf("\nProcess\tBurst Time\tPriority\tWaiting Time\tTurnaround Time\n");

    for(i = 0; i < n; i++)
    {
        printf("P%d\t%d\t\t%d\t\t%d\t\t%d\n",
               process[i], burstTime[i], priority[i], waitingTime[i], turnAroundTime[i]);
    }

    printf("\nTotal Turnaround Time: %d", totalTAT);
    printf("\nAverage Turnaround Time: %.2f", avgTAT);
    printf("\nTotal Waiting Time: %d", totalWT);
    printf("\nAverage Waiting Time: %.2f\n", avgWT);

    return 0;
}
