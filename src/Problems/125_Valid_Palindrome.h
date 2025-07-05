#ifndef PROBLEM_125_H
#define PROBLEM_125_H

/**
 * Problem 125: Valid Palindrome
 * Difficulty: Easy
 * Topics: Two Pointers, String
 * Companies: Facebook, Microsoft
 */

#include <iostream>
#include <string>
#include "../Base/TestUtils.h"

class Solution125
{
public:
    bool IsPalindrome(std::string s)
    {
        int left = 0;
        int right = static_cast<int>(s.length() - 1);
        
        while (left < right)
        {
            while (left < right && !std::isalnum(s[left]))
            {
                ++left;
            }
            
            while (left < right && !std::isalnum(s[right]))
            {
                --right;
            }
            
            if (std::tolower(s[left]) != std::tolower(s[right]))
            {
                return false;
            }
            
            ++left;
            --right;
        }
        
        return true;
    }
};

void TestProblem125()
{
    Solution125 solution;
    TestRunner::Start("Valid Palindrome");
    
    ASSERT_EQ(solution.IsPalindrome("A man, a plan, a canal: Panama"), true);
    ASSERT_EQ(solution.IsPalindrome("race a car"), false);
    
    ASSERT_EQ(solution.IsPalindrome(" "), true);
    ASSERT_EQ(solution.IsPalindrome(""), true);
    ASSERT_EQ(solution.IsPalindrome("a"), true);
    ASSERT_EQ(solution.IsPalindrome("aa"), true);
    ASSERT_EQ(solution.IsPalindrome("ab"), false);
    
    TEST_CASE("Complex palindromes");
    ASSERT_EQ(solution.IsPalindrome("Was it a car or a cat I saw?"), true);
    ASSERT_EQ(solution.IsPalindrome("Madam"), true);
    ASSERT_EQ(solution.IsPalindrome("A Santa at NASA"), true);
    
    TEST_CASE("Alphanumeric cases");
    ASSERT_EQ(solution.IsPalindrome("0P"), false);
    ASSERT_EQ(solution.IsPalindrome("12321"), true);
    ASSERT_EQ(solution.IsPalindrome("12345"), false);
    
    TestRunner::PrintSummary();
}

REGISTER_SOLUTION(125, "Valid Palindrome", TestProblem125);

#endif // PROBLEM_125_H
