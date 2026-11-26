// UnitTest_09_1.cpp
// Єфіменко Софія
// Модульний тест для Лабораторної роботи № 9.1
// Варіант 8

#if defined(_MSC_VER)
#include "pch.h"
#include "CppUnitTest.h"
#include "../PR_9.1/var.h"
#include "../PR_9.1/dod.h"
#include "../PR_9.1/sum.h"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;
using namespace nsVar;
using namespace nsDod;
using namespace nsSum;

namespace UnitTest091
{
    TEST_CLASS(UnitTest091)
    {
    public:
        TEST_METHOD(TestDod)
        {
            x = 2.0;
            n = 1;
            a = -1.0 / x;
            dod();
            Assert::AreEqual(1.0 / 24.0, a, 1e-7);
        }

        TEST_METHOD(TestSum)
        {
            x = 2.0;
            e = 1e-6;
            sum();
            Assert::AreEqual(atan(2.0), s, 1e-5);
            Assert::IsTrue(n > 0);
        }

        TEST_METHOD(TestSumX3)
        {
            x = 3.0;
            e = 1e-7;
            sum();
            Assert::AreEqual(atan(3.0), s, 1e-6);
        }
    };
}
#else
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"
#include <cmath>
#include "../PR_9.1/var.h"
#include "../PR_9.1/dod.h"
#include "../PR_9.1/sum.h"

using namespace nsVar;
using namespace nsDod;
using namespace nsSum;

TEST_CASE("Test nsDod::dod()")
{
    x = 2.0;
    n = 1;
    a = -1.0 / x;
    dod();
    CHECK(a == doctest::Approx(1.0 / 24.0).epsilon(1e-6));
}

TEST_CASE("Test nsSum::sum() for x = 2.0")
{
    x = 2.0;
    e = 1e-7;
    sum();
    CHECK(s == doctest::Approx(std::atan(2.0)).epsilon(1e-6));
    CHECK(n > 0);
}

TEST_CASE("Test nsSum::sum() for x = 3.0")
{
    x = 3.0;
    e = 1e-7;
    sum();
    CHECK(s == doctest::Approx(std::atan(3.0)).epsilon(1e-6));
}

TEST_CASE("Test nsSum::sum() for x = 5.0")
{
    x = 5.0;
    e = 1e-7;
    sum();
    CHECK(s == doctest::Approx(std::atan(5.0)).epsilon(1e-6));
}
#endif
