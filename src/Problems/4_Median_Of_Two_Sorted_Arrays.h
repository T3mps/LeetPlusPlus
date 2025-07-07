#ifndef PROBLEM_4_H
#define PROBLEM_4_H

/**
 * Problem 4: Median of Two Sorted Arrays
 * Difficulty: Hard
 * Topics: Array, Binary Search, Divide and Conquer
 * Companies: Unknown
 */

#include <algorithm>
#include <iostream>
#include <vector>
#include "../Base/TestUtils.h"

class Solution4
{
public:
    double FindMedianSortedArrays(std::vector<int>& nums1, std::vector<int>& nums2)
    {
        // TODO: Implement solution
        return 0.0;
    }
};

void TestProblem4()
{
    Solution4 solution;
    TestRunner::Start("Median of Two Sorted Arrays");
    
        TEST_CASE("Example 1");
    std::vector<int> nums11 = {1,3};
    std::vector<int> nums21 = {2};
    ASSERT_EQ(solution.FindMedianSortedArrays(nums11, nums21), 2.00000);

    TEST_CASE("Example 2");
    std::vector<int> nums12 = {1,2};
    std::vector<int> nums22 = {3,4};
    ASSERT_EQ(solution.FindMedianSortedArrays(nums12, nums22), 2.50000);
    
    TestRunner::PrintSummary();
}

REGISTER_SOLUTION(4, "Median of Two Sorted Arrays", TestProblem4);

#endif // PROBLEM_4_H
