// macros.h
// Єфіменко Софія
// Лабораторна робота № 9.2.1
// Заголовочний файл з макровизначеннями
// Варіант 8

#pragma once

#include <cstdio>

// Запобігання конфліктам із системними макросами
#ifdef SQR
#undef SQR
#endif
#define SQR(x)      ((x) * (x))

#ifdef CUBE
#undef CUBE
#endif
#define CUBE(x)     ((x) * (x) * (x))

#ifdef MAX
#undef MAX
#endif
#define MAX(y, z)   (((y) > (z)) ? (y) : (z))

#ifdef MIN
#undef MIN
#endif
#define MIN(y, z)   (((y) < (z)) ? (y) : (z))

#ifdef ABS
#undef ABS
#endif
#define ABS(x)      (((x) < 0) ? (-(x)) : (x))

// Макроси виведення результатів
#define PRINTI(w) puts("control output"); printf(#w " = %d\n", (int)(w))
#define PRINTR(w) puts("rezult :"); printf(#w " = %f\n", (float)(w))

// Макроси обчислення виразу варіанту 8
// Гілка 1 (z > 10): w = max(x^3, (x + y)^2)
#define CALC_W1(x, y) MAX(CUBE(x), SQR((x) + (y)))

// Гілка 2 (z <= 10): w = min(|x - z|, |x + z|)
#define CALC_W2(x, z) MIN(ABS((x) - (z)), ABS((x) + (z)))
