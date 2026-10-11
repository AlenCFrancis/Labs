#include <stdio.h>

#define BUFFER_SIZE 3

int mutex = 1;
int full = 0;
int empty = BUFFER_SIZE;

int buffer[BUFFER_SIZE];
int in = 0;
int out = 0;
int item = 1;

void producer();
void consumer();
int wait(int s);
int signal(int s);

int main()
{
    int choice;

    printf("\n1. Producer\n2. Consumer\n3. Exit");

    while (1)
    {
        printf("\nEnter your choice: ");
        scanf("%d", &choice);

        switch (choice)
        {
        case 1:
            if ((mutex == 1) && (empty != 0))
                producer();
            else
                printf("Buffer is full!!\n");
            break;

        case 2:
            if ((mutex == 1) && (full != 0))
                consumer();
            else
                printf("Buffer is empty!!\n");
            break;

        case 3:
            return 0;
        }
    }
}

void producer()
{
    mutex = wait(mutex);
    empty = wait(empty);

    buffer[in] = item;
    printf("Produced item: %d at position %d\n", item, in);

    in = (in + 1) % BUFFER_SIZE;
    item++;

    mutex = signal(mutex);
    full = signal(full);
}

void consumer()
{
    mutex = wait(mutex);
    full = wait(full);

    int consumed = buffer[out];
    printf("Consumed item: %d from position %d\n", consumed, out);

    out = (out + 1) % BUFFER_SIZE;

    mutex = signal(mutex);
    empty = signal(empty);
}

int wait(int s)
{
    return (--s);
}

int signal(int s)
{
    return (++s);
}
