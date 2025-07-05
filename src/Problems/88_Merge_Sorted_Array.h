#ifndef PROBLEM_88_H
#define PROBLEM_88_H

/**
 * Problem 88: Merge Sorted Array
 * Difficulty: Easy
 * Topics: Array, Two Pointers
 * Companies: Microsoft, Facebook
 */

#include <iostream>
#include <vector>
#include "../Base/TestUtils.h"

class Solution88
{
public:
    void Merge(std::vector<int>& nums1, int m, std::vector<int>& nums2, int n)
    {
        int i = m - 1;
        int j = n - 1;
        int k = m + n - 1;
        
        while (i >= 0 && j >= 0)
        {
            if (nums1[i] > nums2[j])
            {
                nums1[k--] = nums1[i--];
            }
            else
            {
                nums1[k--] = nums2[j--];
            }
        }
        
        while (j >= 0)
        {
            nums1[k--] = nums2[j--];
        }
    }
};

void TestProblem88()
{
    Solution88 solution;
    TestRunner::Start("Merge Sorted Array");
    
    TEST_CASE("Standard merge");
    std::vector<int> nums1 = {1,2,3,0,0,0};
    std::vector<int> nums2 = {2,5,6};
    solution.Merge(nums1, 3, nums2, 3);
    ASSERT_EQ(nums1, std::vector<int>({1,2,2,3,5,6}));
    
    TEST_CASE("Empty second array");
    nums1 = {1};
    nums2 = {};
    solution.Merge(nums1, 1, nums2, 0);
    ASSERT_EQ(nums1, std::vector<int>({1}));
    
    TEST_CASE("Empty first array");
    nums1 = {0};
    nums2 = {1};
    solution.Merge(nums1, 0, nums2, 1);
    ASSERT_EQ(nums1, std::vector<int>({1}));
    
    TEST_CASE("Second array elements all smaller");
    nums1 = {4,5,6,0,0,0};
    nums2 = {1,2,3};
    solution.Merge(nums1, 3, nums2, 3);
    ASSERT_EQ(nums1, std::vector<int>({1,2,3,4,5,6}));
    
    TEST_CASE("Interleaved elements");
    nums1 = {1,3,5,0,0,0};
    nums2 = {2,4,6};
    solution.Merge(nums1, 3, nums2, 3);
    ASSERT_EQ(nums1, std::vector<int>({1,2,3,4,5,6}));
    
    TestRunner::PrintSummary();
}

REGISTER_SOLUTION(88, "Merge Sorted Array", TestProblem88);

#endif // PROBLEM_88_H
