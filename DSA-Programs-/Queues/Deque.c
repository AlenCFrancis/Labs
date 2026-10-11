#include <stdio.h>
int main() {
    int size;
    printf("Enter the size of the Deque: ");
    scanf("%d", &size);

    int deque[size];
    int front = -1, rear = -1;
    int choice, value;

    // Menu displayed once
    printf("\n--- Double Ended Queue Menu ---");
    printf("\n1. Insert at Front");
    printf("\n2. Insert at Rear");
    printf("\n3. Delete from Front");
    printf("\n4. Delete from Rear");
    printf("\n5. Display");
    printf("\n6. Exit");

    while (1) {
        printf("\n\nEnter your choice: ");
        scanf("%d", &choice);
        //insert at FRONT
        if (choice == 1) { 
            if ((front == 0 && rear == size - 1) || (front == rear + 1)) {
                printf("Deque is Full!");
            } else {
                printf("Enter value to insert at front: ");
                scanf("%d", &value);
                if (front == -1) {
                    front = rear = 0;
                } else if (front == 0) {
                    front = size - 1;
                } else {
                    front--;
                }
                deque[front] = value;
                printf("%d inserted at front.", value);
            }
        }
        //Insert at REAR
        else if (choice == 2) {
            if ((front == 0 && rear == size - 1) || (front == rear + 1)) {
                printf("Deque is Full!");
            } else {
                printf("Enter value to insert at rear: ");
                scanf("%d", &value);
                if (front == -1) {
                    front = rear = 0;
                } else if (rear == size - 1) {
                    rear = 0;
                } else {
                    rear++;
                }
                deque[rear] = value;
                printf("%d inserted at rear.", value);
            }
        }
        //Delete at FRONT
        else if (choice == 3) {
            if (front == -1) {
                printf("Deque is Empty!");
            } else {
                printf("Deleted element from front: %d", deque[front]);
                if (front == rear) {
                    front = rear = -1;
                } else if (front == size - 1) {
                    front = 0;
                } else {
                    front++;
                }
            }
        }
        // Delete from REAR
        else if (choice == 4) {
            if (front == -1) {
                printf("Deque is Empty!");
            } else {
                printf("Deleted element from rear: %d", deque[rear]);
                if (front == rear) {
                    front = rear = -1;
                } else if (rear == 0) {
                    rear = size - 1;
                } else {
                    rear--;
                }
            }
        }

        else if (choice == 5) { 
            if (front == -1) {
                printf("Deque is Empty!");
            } else {
                printf("Deque elements: ");
                int i = front;
                while (1) {
                    printf("%d ", deque[i]);
                    if (i == rear)
                        break;
                    i = (i + 1) % size;
                }
            }
        }

        else if (choice == 6) { 
            printf("Exiting...");
            break;
        }

        else {
            printf("Invalid choice!");
        }
    }

    return 0;
}
