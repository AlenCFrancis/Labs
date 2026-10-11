#include <stdio.h>

int main()
{
    int size, choice, value;
    int front = -1, rear = -1;

    printf("Enter the size of the Queue: ");
    scanf("%d", &size);
    int queue[size];

    printf("\nQueue operations:\n");
    printf("1. Enqueue\n");
    printf("2. Dequeue\n");
    printf("3. Display\n");
    printf("4. Exit\n");

    while (1)
    {
        printf("\nEnter your choice: ");
        scanf("%d", &choice);

        switch (choice)
        {
        case 1:
            if (rear == (size - 1))
            {
                printf("Queue Overflow!\n");
            }
            else
            {
                printf("Enter the value to Enqueue: ");
                scanf("%d", &value);

                if (front == -1)
                    front = 0;

                rear++;
                queue[rear] = value;
                printf("%d enqueued\n", value);
            }
            break;

        case 2:
            if (front == -1 || front > rear)
            {
                printf("Queue is empty\n");
            }
            else
            {
                printf("%d dequeued\n", queue[front]);
                front++;
            }
            break;

        case 3:
            if (front == -1 || front > rear)
            {
                printf("Queue is empty\n");
            }
            else
            {
                printf("Queue Elements: ");
                for (int i = front; i <= rear; i++)
                {
                    printf("%d ", queue[i]);
                }
                printf("\n");
            }
            break;

        case 4:
            printf("Exiting......\n");
            return 0;

        default:
            printf("Invalid choice\n");
        }
    }

    return 0;
}

