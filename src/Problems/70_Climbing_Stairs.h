#ifndef PROBLEM_70_H
#define PROBLEM_70_H

/**
 * Problem 70: Climbing Stairs
 * Difficulty: Easy
 * Topics: Dynamic Programming
 * Companies: Amazon, Adobe
 */

#include <iostream>
#include <vector>
#include "../Base/TestUtils.h"

class Solution70
{
public:
    int ClimbStairs(int n)
    {
        if (n <= 2)
            return n;
        
        int prev2 = 1;
        int prev1 = 2;
        
        for (int i = 3; i <= n; i++)
        {
            int current = prev1 + prev2;
            prev2 = prev1;
            prev1 = current;
        }
        
        return prev1;
    }
};

void TestProblem70()
{
    Solution70 solution;
    TestRunner::Start("Climbing Stairs");
    
    ASSERT_EQ(solution.ClimbStairs(1), 1);
    ASSERT_EQ(solution.ClimbStairs(2), 2);
    ASSERT_EQ(solution.ClimbStairs(3), 3);
    ASSERT_EQ(solution.ClimbStairs(4), 5);
    ASSERT_EQ(solution.ClimbStairs(5), 8);
    
    TEST_CASE("Medium values");
    ASSERT_EQ(solution.ClimbStairs(10), 89);
    ASSERT_EQ(solution.ClimbStairs(15), 987);
    
    TEST_CASE("Large value");
    ASSERT_EQ(solution.ClimbStairs(45), 1836311903);
    
    TestRunner::PrintSummary();
}

REGISTER_SOLUTION_WITH_DIFFICULTY(70, "Climbing Stairs", TestProblem70, Difficulty::Easy);

#endif // PROBLEM_70_H
