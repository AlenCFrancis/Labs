#include <stdio.h>

int main() {
    int size;
    printf("Enter the size of the queue: ");
    scanf("%d", &size);

    int queue[size];
    int front = -1, rear = -1;

    int choice, value;

    printf("\n--- Circular Queue Menu ---");
    printf("\n1. Enqueue");
    printf("\n2. Dequeue");
    printf("\n3. Display");
    printf("\n4. Exit");

    while (1) {
        printf("\n\nEnter your choice: ");
        scanf("%d", &choice);

        if (choice == 1) {  // Enqueue
            if ((front == 0 && rear == size - 1) || (rear + 1) % size == front) {
                printf("Queue is Full!");
            } else {
                printf("Enter value to insert: ");
                scanf("%d", &value);
                if (front == -1) front = 0;
                rear = (rear + 1) % size;
                queue[rear] = value;
                printf("%d inserted.", value);
            }
        } 
        else if (choice == 2) {  // Dequeue
            if (front == -1) {
                printf("Queue is Empty!");
            } else {
                printf("Deleted element: %d", queue[front]);
                if (front == rear)
                    front = rear = -1;
                else
                    front = (front + 1) % size;
            }
        } 
        else if (choice == 3) {  // Display
            if (front == -1) {
                printf("Queue is Empty!");
            } else {
                int i = front;
                printf("Queue elements: ");
                while (1) {
                    printf("%d ", queue[i]);
                    if (i == rear) break;
                    i = (i + 1) % size;
                }
            }
        } 
        else if (choice == 4) {  // Exit
            printf("Exiting...");
            break;
        } 
        else {
            printf("Invalid choice!");
        }
    }
    return 0;
}
