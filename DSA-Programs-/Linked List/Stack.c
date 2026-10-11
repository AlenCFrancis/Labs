#include <stdio.h>
#include <stdlib.h>

// Define node structure
struct node {
    int data;
    struct node* link;
};

struct node* top = NULL;  // Stack top pointer

// PUSH operation
void push(int x) {
    struct node* newNode = (struct node*)malloc(sizeof(struct node));
    if (newNode == NULL) {
        printf("\nStack Overflow (Memory not allocated)\n");
        return;
    }
    newNode->data = x;
    newNode->link = top;
    top = newNode;
    printf("\n%d pushed to stack\n", x);
}

// POP operation
void pop() {
    if (top == NULL) {
        printf("\nStack Underflow (Empty stack)\n");
    } else {
        struct node* temp = top;
        printf("\n%d popped from stack\n", temp->data);
        top = top->link;
        free(temp);
    }
}

// DISPLAY operation
void display() {
    if (top == NULL) {
        printf("\nStack is empty\n");
    } else {
        struct node* ptr = top;
        printf("\nStack elements are: ");
        while (ptr != NULL) {
            printf("%d ", ptr->data);
            ptr = ptr->link;
        }
        printf("\n");
    }
}

// MAIN FUNCTION
int main() {
    int choice, value;

    printf("\n--- Stack Menu ---\n");
    printf("1. Push\n");
    printf("2. Pop\n");
    printf("3. Display\n");
    printf("4. Exit\n");

    do {
        printf("\nEnter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter value to push: ");
                scanf("%d", &value);
                push(value);
                break;
            case 2:
                pop();
                break;
            case 3:
                display();
                break;
            case 4:
                printf("\nExiting program...\n");
                break;
            default:
                printf("\nInvalid choice! Try again.\n");
        }

    } while (choice != 4);

    return 0;
}
