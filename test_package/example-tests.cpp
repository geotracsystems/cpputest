#include <iostream>
#include <CppUTest/TestHarness.h>

TEST_GROUP(Example)
{
};

TEST(Example, test1Plus1)
{
	CHECK_EQUAL(1 + 1, 2);
}
