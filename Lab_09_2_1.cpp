// Lab_09_2_1.cpp
// Єфіменко Софія
// Лабораторна робота № 9.2.1
// Директиви препроцесора та макровизначення. Частина 1.
// Варіант 8

#include <iostream>
#include "macros.h"

// Значення Z для директив умовної компіляції препроцесора
#ifndef Z
#define Z 15
#endif

using namespace std;

int main()
{
    cout << "Lab 9.2.1. Macros and preprocessing directives. Variant 8." << endl;
    char ch;
    do {
#if Z > 10
        cout << "\n--- Branch 1: Z > 10 (Z = " << Z << ") ---" << endl;
        cout << "w = max(x^3, (x + y)^2)" << endl;
        double x, y, w;
        cout << "Input x: "; cin >> x;
        PRINTI(x);
        cout << "Input y: "; cin >> y;
        PRINTI(y);
        w = CALC_W1(x, y);
        PRINTR(w);
#else
        cout << "\n--- Branch 2: Z <= 10 (Z = " << Z << ") ---" << endl;
        cout << "w = min(|x - z|, |x + z|)" << endl;
        double x, z_val, w;
        cout << "Input x: "; cin >> x;
        PRINTI(x);
        z_val = Z;
        cout << "Constant Z = " << z_val << endl;
        w = CALC_W2(x, z_val);
        PRINTR(w);
#endif
        cout << "Repeat? (y/n): ";
        cin >> ch;
    } while (ch == 'y' || ch == 'Y');

    return 0;
}
