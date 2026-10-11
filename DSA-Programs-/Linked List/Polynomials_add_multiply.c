#include <stdio.h>
#include <stdlib.h>

struct Node 
{
    int coeff, pow;
    struct Node *next;
};

struct Node* newNode(int c, int p) 
{
    struct Node* n = (struct Node*)malloc(sizeof(struct Node));
    n->coeff = c; 
    n->pow = p; 
    n->next = NULL;
    return n;
}

struct Node* insert(struct Node* head, int c, int p) 
{
    if (c == 0) return head;
    struct Node *n = newNode(c, p), *cur = head, *prev = NULL;

    if (!head || p > head->pow) 
    { 
        n->next = head; return n; 
    }

    while (cur && cur->pow > p) 
    { 
        prev = cur; cur = cur->next;
    }
    if (cur && cur->pow == p) 
    { 
        cur->coeff += c; 
        free(n); 
        return head; 
    }

    n->next = cur;
    prev->next = n;
    return head;
}

struct Node* create() 
{
    int n, c, p; 
    struct Node* head = NULL;
    printf("Enter number of terms: "); 
    scanf("%d", &n);
    for (int i = 0; i < n; i++) 
    {
        printf("Enter coeff and power of term %d: ", i + 1);
        scanf("%d%d", &c, &p);
        head = insert(head, c, p);
    }
    return head;
}

void display(struct Node* h) 
{
    if (!h) 
    { 
    printf("0"); 
    return; 
    }
    while (h) 
    {
        printf("%dx^%d", h->coeff, h->pow);
        if (h->next) printf(" + ");
        h = h->next;
    }
}

struct Node* add(struct Node* a, struct Node* b)
{
    struct Node* r = NULL;
    while (a) 
    { 
        r = insert(r, a->coeff, a->pow); 
        a = a->next; 
    }
    while (b) 
    {
        r = insert(r, b->coeff, b->pow); 
        b = b->next;
    }
    return r;
}

struct Node* multiply(struct Node* a, struct Node* b) 
{
    struct Node *r = NULL, *t;
    while (a) 
    {
        t = b;
        while (t) 
        {
            r = insert(r, a->coeff * t->coeff, a->pow + t->pow);
            t = t->next;
        }
        a = a->next;
    }
    return r;
}

int main() {
    struct Node *P1, *P2, *sum, *prod;
    printf("Enter Polynomial P1:\n"); P1 = create();
    printf("\nEnter Polynomial P2:\n"); P2 = create();

    printf("\nP1(x) = "); display(P1);
    printf("\nP2(x) = "); display(P2);

    sum = add(P1, P2);
    prod = multiply(P1, P2);

    printf("\n\nP1(x) + P2(x) = "); display(sum);
    printf("\nP1(x) × P2(x) = "); display(prod);
    printf("\n");
    return 0;
}
