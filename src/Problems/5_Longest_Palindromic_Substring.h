#ifndef PROBLEM_5_H
#define PROBLEM_5_H

/**
 * Problem 5: Longest Palindromic Substring
 * Difficulty: Medium
 * Topics: Two Pointers, String, Dynamic Programming
 * Companies: Unknown
 */

#include <iostream>
#include <string>
#include <vector>
#include "../Base/TestUtils.h"

class Solution5
{
public:
    std::string LongestPalindrome(std::string s)
    {
        // TODO: Implement solution
        return "";
    }
};

void TestProblem5()
{
    Solution5 solution;
    TestRunner::Start("Longest Palindromic Substring");
    
        TEST_CASE("Example 1");
    std::string s1 = "&quot;babad&quot;";
    std::string expected1 = "&quot;bab&quot;";
    ASSERT_EQ(solution.LongestPalindrome(s1), expected1);

    TEST_CASE("Example 2");
    std::string s2 = "&quot;cbbd&quot;";
    std::string expected2 = "&quot;bb&quot;";
    ASSERT_EQ(solution.LongestPalindrome(s2), expected2);
    
    TestRunner::PrintSummary();
}

REGISTER_SOLUTION(5, "Longest Palindromic Substring", TestProblem5);

#endif // PROBLEM_5_H
