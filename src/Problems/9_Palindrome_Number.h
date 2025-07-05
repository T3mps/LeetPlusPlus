#ifndef PROBLEM_9_H
#define PROBLEM_9_H

/**
 * Problem 9: Palindrome Number
 * Difficulty: Easy
 * Topics: Math
 * Companies: Amazon, Apple
 */

#include <iostream>
#include "../Base/TestUtils.h"

class Solution9
{
public:
    bool IsPalindrome(int x)
    {
        if (x < 0)
            return false;
        if (x < 10)
            return true;

        long long reversed = 0;
        int original = x;
        
        while (x > 0)
        {
            reversed = reversed * 10 + x % 10;
            x /= 10;
        }
        
        return original == reversed;
    }
};

void TestProblem9()
{
    Solution9 solution;
    TestRunner::Start("Palindrome Number");
    
    ASSERT_EQ(solution.IsPalindrome(121), true);
    ASSERT_EQ(solution.IsPalindrome(1221), true);
    ASSERT_EQ(solution.IsPalindrome(12321), true);
    ASSERT_EQ(solution.IsPalindrome(0), true);
    ASSERT_EQ(solution.IsPalindrome(1), true);
    ASSERT_EQ(solution.IsPalindrome(9), true);
    
    ASSERT_EQ(solution.IsPalindrome(123), false);
    ASSERT_EQ(solution.IsPalindrome(10), false);
    ASSERT_EQ(solution.IsPalindrome(-121), false);
    ASSERT_EQ(solution.IsPalindrome(-1), false);
    
    TEST_CASE("Large palindrome");
    ASSERT_EQ(solution.IsPalindrome(1234554321), true);
    ASSERT_EQ(solution.IsPalindrome(123454321), true);
    
    TEST_CASE("Numbers ending with zero");
    ASSERT_EQ(solution.IsPalindrome(1000), false);
    ASSERT_EQ(solution.IsPalindrome(10000), false);
    
    TEST_CASE("Maximum int palindrome");
    ASSERT_EQ(solution.IsPalindrome(2147447412), true);
    
    TestRunner::PrintSummary();
}

REGISTER_SOLUTION(9, "Palindrome Number", TestProblem9);

#endif // PROBLEM_9_H
