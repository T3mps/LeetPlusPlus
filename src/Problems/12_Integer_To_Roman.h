#ifndef PROBLEM_12_H
#define PROBLEM_12_H

/**
 * Problem 12: Integer to Roman
 * Difficulty: Medium
 * Topics: Hash Table, Math, String
 * Companies: Unknown
 */

#include <iostream>
#include <string>
#include <unordered_map>
#include "../Base/TestUtils.h"

class Solution12
{
public:
    std::string IntToRoman(int num)
    {
        // TODO: Implement solution
        return "";
    }
};

void TestProblem12()
{
    Solution12 solution;
    TestRunner::Start("Integer to Roman");
    
        TEST_CASE("Example 1");
    int num1 = 3749;
    auto result1 = solution.IntToRoman(num1);
    // TODO: Add expected result for example 1

    TEST_CASE("Example 2");
    int num2 = 58;
    auto result2 = solution.IntToRoman(num2);
    // TODO: Add expected result for example 2

    TEST_CASE("Example 3");
    int num3 = 1994;
    auto result3 = solution.IntToRoman(num3);
    // TODO: Add expected result for example 3
    
    TestRunner::PrintSummary();
}

REGISTER_SOLUTION(12, "Integer to Roman", TestProblem12);

#endif // PROBLEM_12_H
