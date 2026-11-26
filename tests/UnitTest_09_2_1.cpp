// UnitTest_09_2_1.cpp
// Єфіменко Софія
// Модульний тест для Лабораторної роботи № 9.2.1
// Варіант 8

#if defined(_MSC_VER)
#include "pch.h"
#include "CppUnitTest.h"
#include "../PR_9.2_1/macros.h"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace UnitTest0921
{
    TEST_CLASS(UnitTest0921)
    {
    public:
        TEST_METHOD(TestBasicMacros)
        {
            Assert::AreEqual(9, SQR(3));
            Assert::AreEqual(8, CUBE(2));
            Assert::AreEqual(10, MAX(5, 10));
            Assert::AreEqual(5, MIN(5, 10));
            Assert::AreEqual(7, ABS(-7));
            Assert::AreEqual(7, ABS(7));
        }

        TEST_METHOD(TestBranch1)
        {
            double x = 2.0, y = 1.0;
            Assert::AreEqual(9.0, CALC_W1(x, y), 1e-7);

            x = 3.0; y = 1.0;
            Assert::AreEqual(27.0, CALC_W1(x, y), 1e-7);
        }

        TEST_METHOD(TestBranch2)
        {
            double x = 5.0, z = 3.0;
            Assert::AreEqual(2.0, CALC_W2(x, z), 1e-7);

            x = 2.0; z = 8.0;
            Assert::AreEqual(6.0, CALC_W2(x, z), 1e-7);
        }
    };
}
#else
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"
#include "../PR_9.2_1/macros.h"

TEST_CASE("Test basic mathematical macros")
{
    CHECK(SQR(3) == 9);
    CHECK(CUBE(2) == 8);
    CHECK(MAX(5, 10) == 10);
    CHECK(MIN(5, 10) == 5);
    CHECK(ABS(-7) == 7);
    CHECK(ABS(7) == 7);
}

TEST_CASE("Test Branch 1 (Z > 10): w = max(x^3, (x + y)^2)")
{
    double x = 2.0;
    double y = 1.0;
    CHECK(CALC_W1(x, y) == doctest::Approx(9.0));

    x = 3.0;
    y = 1.0;
    CHECK(CALC_W1(x, y) == doctest::Approx(27.0));
}

TEST_CASE("Test Branch 2 (Z <= 10): w = min(|x - z|, |x + z|)")
{
    double x = 5.0;
    double z = 3.0;
    CHECK(CALC_W2(x, z) == doctest::Approx(2.0));

    x = 2.0;
    z = 8.0;
    CHECK(CALC_W2(x, z) == doctest::Approx(6.0));
}
#endif
