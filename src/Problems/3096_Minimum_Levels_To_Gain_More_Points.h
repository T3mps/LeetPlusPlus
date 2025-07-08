#ifndef PROBLEM_3096_H
#define PROBLEM_3096_H

/**
 * Problem 3096: Minimum Levels to Gain More Points
 * Difficulty: Medium
 * Topics: Array, Prefix Sum
 * Companies: Unknown
 */

#include <iostream>
#include <vector>
#include "../Base/TestUtils.h"

class Solution3096
{
public:
    int MinimumLevels(std::vector<int>& possible)
    {
        // TODO: Implement solution
        return 0;
    }
};

void TestProblem3096()
{
    Solution3096 solution;
    TestRunner::Start("Minimum Levels to Gain More Points");
    
        TEST_CASE("Example 1");
    std::vector<int> possible1 = {1,0,1,0};
    auto result1 = solution.MinimumLevels(possible1);
    // TODO: Add expected result for example 1

    TEST_CASE("Example 2");
    std::vector<int> possible2 = {1,1,1,1,1};
    auto result2 = solution.MinimumLevels(possible2);
    // TODO: Add expected result for example 2

    TEST_CASE("Example 3");
    std::vector<int> possible3 = {0,0};
    auto result3 = solution.MinimumLevels(possible3);
    // TODO: Add expected result for example 3
    
    TestRunner::PrintSummary();
}

REGISTER_SOLUTION(3096, "Minimum Levels to Gain More Points", TestProblem3096);

#endif // PROBLEM_3096_H
