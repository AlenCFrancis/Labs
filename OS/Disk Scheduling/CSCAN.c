#include <stdio.h>

int main() {
    int i, j, temp, n;
    int head, size, dir, total_movement = 0;
    int req[100];

    printf("Enter number of requests: ");
    scanf("%d", &n);

    printf("Enter requests sequence: ");
    for (i = 0; i < n; i++) {
        scanf("%d", &req[i]);
    }

    printf("Enter initial head position: ");
    scanf("%d", &head);

    printf("Enter total disk size: ");
    scanf("%d", &size);

    printf("Enter direction (1 for High, 0 for Low): ");
    scanf("%d", &dir);

    for (i = 0; i < n - 1; i++) {
        for (j = 0; j < n - i - 1; j++) {
            if (req[j] > req[j + 1]) {
                temp = req[j];
                req[j] = req[j + 1];
                req[j + 1] = temp;
            }
        }
    }

    
    if (dir == 1) {
        int break_point = 0;
        for(i = 0; i < n; i++) {
            if(req[i] > head) {
                break_point = i;
                break;
            }
        }

        total_movement = (size - 1 - head) + (size - 1) + (req[break_point - 1]);
    } 
    else {
        int break_point = 0;
        for(i = 0; i < n; i++) {
            if(req[i] > head) {
                break_point = i;
                break;
            }
        }
        total_movement = (head - 0) + (size - 1) + (size - 1 - req[break_point]);
    }

    printf("\nTotal Head Movement: %d\n", total_movement);

    return 0;
}
