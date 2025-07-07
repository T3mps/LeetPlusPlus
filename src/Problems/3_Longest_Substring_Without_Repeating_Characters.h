#ifndef PROBLEM_3_H
#define PROBLEM_3_H

/**
 * Problem 3: Longest Substring Without Repeating Characters
 * Difficulty: Medium
 * Topics: Hash Table, String, Sliding Window
 * Companies: Unknown
 */

#include <iostream>
#include <string>
#include <unordered_map>
#include "../Base/TestUtils.h"

class Solution3
{
public:
    int LengthOfLongestSubstring(std::string s)
    {
        // TODO: Implement solution
        return 0;
    }
};

void TestProblem3()
{
    Solution3 solution;
    TestRunner::Start("Longest Substring Without Repeating Characters");
    
        TEST_CASE("Example 1");
    std::string s1 = "&quot;abcabcbb&quot;";
    ASSERT_EQ(solution.LengthOfLongestSubstring(s1), 3);

    TEST_CASE("Example 2");
    std::string s2 = "&quot;bbbbb&quot;";
    ASSERT_EQ(solution.LengthOfLongestSubstring(s2), 1);

    TEST_CASE("Example 3");
    std::string s3 = "&quot;pwwkew&quot;";
    ASSERT_EQ(solution.LengthOfLongestSubstring(s3), 3);
    
    TestRunner::PrintSummary();
}

REGISTER_SOLUTION(3, "Longest Substring Without Repeating Characters", TestProblem3);

#endif // PROBLEM_3_H
