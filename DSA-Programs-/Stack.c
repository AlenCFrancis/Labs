#include <stdio.h>

int main() {
    int n;
    
    printf("Enter the size of the array: ");
    scanf("%d", &n);
    
    int arr[n];
    int perform, x, top = -1;
    printf("\n1. PUSH\n2. POP\n3. DISPLAY\n4. EXIT\n");
    
    while(1) {
        printf("Enter choice: ");
        scanf("%d", &perform);
        
        if (perform == 1) {
            if (top == n - 1) {
                printf("Stack is overflow\n");
            } else {
                printf("Enter the value: ");
                scanf("%d", &x);
                top++;
                arr[top] = x;
            }
        } 
        
        else if (perform == 2) {
            if (top == -1) {
                printf("Stack is underflow\n");
            } else {
                printf("Deleted element is: %d\n", arr[top]);
                top--;
            }
        } 
        
        else if (perform == 3) {
            if (top == -1) {
                printf("Stack is underflow\n");
            } else {
                printf("Stack elements are\n");
                for (int i = top; i >= 0; i--) {
                    printf("%d\n", arr[i]);
                }
            }
        }
        
        else if (perform == 4) {
            break; 
        }
        
        else {
            printf("Invalid choice. Please enter 1, 2, 3, or 4.\n");
        }
    }
    
    return 0;
}
