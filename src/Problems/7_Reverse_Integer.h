#ifndef PROBLEM_7_H
#define PROBLEM_7_H

/**
 * Problem 7: Reverse Integer
 * Difficulty: Medium
 * Topics: Math
 * Companies: Unknown
 */

#include <iostream>
#include "../Base/TestUtils.h"

class Solution7
{
public:
    int Reverse(int x)
    {
        // TODO: Implement solution
        return 0;
    }
};

void TestProblem7()
{
    Solution7 solution;
    TestRunner::Start("Reverse Integer");
    
        TEST_CASE("Example 1");
    int x1 = 123;
    ASSERT_EQ(solution.Reverse(x1), 321);

    TEST_CASE("Example 2");
    int x2 = -123;
    ASSERT_EQ(solution.Reverse(x2), -321);

    TEST_CASE("Example 3");
    int x3 = 120;
    ASSERT_EQ(solution.Reverse(x3), 21);
    
    TestRunner::PrintSummary();
}

REGISTER_SOLUTION(7, "Reverse Integer", TestProblem7);

#endif // PROBLEM_7_H
