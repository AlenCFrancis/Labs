#include <stdio.h>

#define MAX 100

char stack[MAX];
int top = -1;

void push(char c) {
    if (top < MAX - 1)
        stack[++top] = c;
}

char pop() {
    if (top >= 0)
        return stack[top--];
    return '\0';
}

char peek() {
    if (top >= 0)
        return stack[top];
    return '\0';
}

int precedence(char op) {
    if (op == '+' || op == '-') return 1;
    if (op == '*' || op == '/') return 2;
    return 0;
}

int isOperator(char c) {
    return (c == '+' || c == '-' || c == '*' || c == '/');
}

void infixToPostfix(char infix[], char postfix[]) {
    int i = 0, j = 0;
    char c;
    while ((c = infix[i++]) != '\0') {
        if (c >= '0' && c <= '9')
            postfix[j++] = c;
        else if (c == '(')
            push(c);
        else if (c == ')') {
            while (top >= 0 && peek() != '(')
                postfix[j++] = pop();
            pop(); // remove '('
        } else if (isOperator(c)) {
            while (top >= 0 && precedence(peek()) >= precedence(c))
                postfix[j++] = pop();
            push(c);
        }
    }
    while (top >= 0)
        postfix[j++] = pop();
    postfix[j] = '\0';
}

int evalPostfix(char postfix[]) {
    int valStack[MAX], valTop = -1, i = 0;
    char c;
    while ((c = postfix[i++]) != '\0') {
        if (c >= '0' && c <= '9')
            valStack[++valTop] = c - '0';
        else if (isOperator(c)) {
            int b = valStack[valTop--];
            int a = valStack[valTop--];
            switch (c) {
                case '+': valStack[++valTop] = a + b; break;
                case '-': valStack[++valTop] = a - b; break;
                case '*': valStack[++valTop] = a * b; break;
                case '/': valStack[++valTop] = a / b; break;
            }
        }
    }
    return valStack[valTop];
}

int main() {
    char infix[MAX], postfix[MAX];
    printf("Enter infix expression: ");
    scanf("%s", infix);

    infixToPostfix(infix, postfix);
    printf("Postfix: %s\n", postfix);
    printf("Result: %d\n", evalPostfix(postfix));
    return 0;
}
