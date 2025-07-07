#ifndef PROBLEM_66_H
#define PROBLEM_66_H

/**
 * Problem 66: Plus One
 * Difficulty: Easy
 * Topics: Array, Math
 * Companies: Unknown
 */

#include <iostream>
#include <vector>
#include "../Base/TestUtils.h"

class Solution66
{
public:
    std::vector<int> PlusOne(std::vector<int>& digits)
    {
        // TODO: Implement solution
        return {};
    }
};

void TestProblem66()
{
    Solution66 solution;
    TestRunner::Start("Plus One");
    
        TEST_CASE("Example 1");
    std::vector<int> digits1 = {1,2,3};
    std::vector<int> expected1 = {1,2,4};
    ASSERT_EQ(solution.PlusOne(digits1), expected1);

    TEST_CASE("Example 2");
    std::vector<int> digits2 = {4,3,2,1};
    std::vector<int> expected2 = {4,3,2,2};
    ASSERT_EQ(solution.PlusOne(digits2), expected2);

    TEST_CASE("Example 3");
    std::vector<int> digits3 = {9};
    std::vector<int> expected3 = {1,0};
    ASSERT_EQ(solution.PlusOne(digits3), expected3);
    
    TestRunner::PrintSummary();
}

REGISTER_SOLUTION(66, "Plus One", TestProblem66);

#endif // PROBLEM_66_H
