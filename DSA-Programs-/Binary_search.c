#include <stdio.h>

// Function to sort the array (Bubble Sort)
void sortArray(int arr[], int n) {
    int i, j, temp;
    for(i = 0; i < n-1; i++) {
        for(j = 0; j < n-i-1; j++) {
            if(arr[j] > arr[j+1]) {
                temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
    }
}

// Function for Binary Search
int binarySearch(int arr[], int n, int key) {
    int low = 0, high = n - 1, mid;

    while(low <= high) {
        mid = (low + high) / 2;

        if(arr[mid] == key)
            return mid;  // Found
        else if(arr[mid] < key)
            low = mid + 1;
        else
            high = mid - 1;
    }
    return -1;  // Not found
}

int main() {
    int n, i, key, result;

    // Input size of array
    printf("Enter number of elements: ");
    scanf("%d", &n);

    int arr[n];

    // Input elements
    printf("Enter %d elements:\n", n);
    for(i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    // Sort the array
    sortArray(arr, n);

    // Display sorted array
    printf("\nSorted Array: ");
    for(i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    // Input element to search
    printf("Enter the element to search: ");
    scanf("%d", &key);

    // Perform Binary Search
    result = binarySearch(arr, n, key);

    if(result != -1)
        printf("Element %d found at position %d in the sorted array.\n", key, result + 1);
    else
        printf("Element %d not found in the array.\n", key);

    return 0;
}
