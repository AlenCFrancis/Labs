#include <stdio.h>
#include <stdlib.h>

#define MAX 100   // maximum number of nodes

int tree[MAX];    // array to store tree nodes
int size = 0;     // number of nodes
// Function to insert a node
void insertNode(int val) {
    if (size >= MAX) {
        printf("Tree is full!\n");
        return;
    }
    tree[size + 1] = val;  // store at next available index (1-based indexing)
    size++;
    printf("Inserted %d\n", val);
}

// Function to delete a node at given index
void deleteNode(int index) {
    if (index > size || index <= 0) {
        printf("Invalid node position!\n");
        return;
    }
    printf("Deleted %d\n", tree[index]);
    // replace with last node
    tree[index] = tree[size];
    size--;
}

// Inorder traversal (Left, Root, Right)
void inorder(int i) {
    if (i > size) return;
    inorder(2 * i);          // left child
    printf("%d ", tree[i]);  // root
    inorder(2 * i + 1);      // right child
}

// Preorder traversal (Root, Left, Right)
void preorder(int i) {
    if (i > size) return;
    printf("%d ", tree[i]);
    preorder(2 * i);
    preorder(2 * i + 1);
}

// Postorder traversal (Left, Right, Root)
void postorder(int i) {
    if (i > size) return;
    postorder(2 * i);
    postorder(2 * i + 1);
    printf("%d ", tree[i]);
}

int main() {
    int choice, val, index;

    printf("---- Simple Binary Tree using Array ----\n");
    printf("1. Insert Node\n");
    printf("2. Delete Node (by index)\n");
    printf("3. Inorder Traversal\n");
    printf("4. Preorder Traversal\n");
    printf("5. Postorder Traversal\n");
    printf("6. Exit\n");

    while (1) {
        printf("\nEnter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter value to insert: ");
                scanf("%d", &val);
                insertNode(val);
                break;

            case 2:
                printf("Enter node index to delete: ");
                scanf("%d", &index);
                deleteNode(index);
                break;

            case 3:
                printf("Inorder Traversal: ");
                inorder(1);
                printf("\n");
                break;

            case 4:
                printf("Preorder Traversal: ");
                preorder(1);
                printf("\n");
                break;

            case 5:
                printf("Postorder Traversal: ");
                postorder(1);
                printf("\n");
                break;

            case 6:
                exit(0);

            default:
                printf("Invalid choice!\n");
        }
    }
    return 0;
}
