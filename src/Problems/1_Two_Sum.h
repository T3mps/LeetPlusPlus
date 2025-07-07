#ifndef PROBLEM_1_H
#define PROBLEM_1_H

/**
 * Problem 1: Two Sum
 * Difficulty: Easy
 * Topics: Array, Hash Table
 * Companies: Unknown
 */

#include <iostream>
#include <unordered_map>
#include <vector>
#include "../Base/TestUtils.h"

class Solution1
{
public:
    std::vector<int> TwoSum(std::vector<int>& nums, int target)
    {
        std::unordered_map<int, int> hash_map;
        
        for (int i = 0; i < nums.size(); i++)
        {
            int complement = target - nums[i];
            
            if (hash_map.find(complement) != hash_map.end())
            {
                return {hash_map[complement], i};
            }
            
            hash_map[nums[i]] = i;
        }
        
        return {};
    }
};

void TestProblem1()
{
    Solution1 solution;
    TestRunner::Start("Two Sum");
    
    TEST_CASE("Example 1");
    std::vector<int> nums1 = {2,7,11,15};
    int target1 = 9;
    std::vector<int> expected1 = {0,1};
    // Note: If order doesn't matter, use ASSERT_UNORDERED_EQ instead
    ASSERT_EQ(solution.TwoSum(nums1, target1), expected1);

    TEST_CASE("Example 2");
    std::vector<int> nums2 = {3,2,4};
    int target2 = 6;
    std::vector<int> expected2 = {1,2};
    // Note: If order doesn't matter, use ASSERT_UNORDERED_EQ instead
    ASSERT_EQ(solution.TwoSum(nums2, target2), expected2);

    TEST_CASE("Example 3");
    std::vector<int> nums3 = {3,3};
    int target3 = 6;
    std::vector<int> expected3 = {0,1};
    // Note: If order doesn't matter, use ASSERT_UNORDERED_EQ instead
    ASSERT_EQ(solution.TwoSum(nums3, target3), expected3);
    
    TestRunner::PrintSummary();
}

REGISTER_SOLUTION(1, "Two Sum", TestProblem1);

#endif // PROBLEM_1_H
