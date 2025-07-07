#ifndef PROBLEM_2_H
#define PROBLEM_2_H

/**
 * Problem 2: Add Two Numbers
 * Difficulty: Medium
 * Topics: Linked List, Math, Recursion
 * Companies: Unknown
 */

#include <iostream>
#include "../Common/Structures.h"
#include "../Base/TestUtils.h"
#include "../Common/TestHelpers.h"

class Solution2
{
public:
    ListNode* AddTwoNumbers(ListNode* l1, ListNode* l2)
    {
        // TODO: Implement solution
        return nullptr;
    }
};

void TestProblem2()
{
    Solution2 solution;
    TestRunner::Start("Add Two Numbers");
    
        TEST_CASE("Example 1");
    ListNode* l11 = TestHelpers::CreateLinkedList({2,4,3});
    ListNode* l21 = TestHelpers::CreateLinkedList({5,6,4});
    ListNode* expected1 = TestHelpers::CreateLinkedList({7,0,8});
    auto result1 = solution.AddTwoNumbers(l11, l21);
    ASSERT_LINKED_LISTS_EQ(result1, expected1);
    TestHelpers::DeleteLinkedList(expected1);
    TestHelpers::DeleteLinkedList(result1);
    TestHelpers::DeleteLinkedList(l11);
    TestHelpers::DeleteLinkedList(l21);

    TEST_CASE("Example 2");
    ListNode* l12 = TestHelpers::CreateLinkedList({0});
    ListNode* l22 = TestHelpers::CreateLinkedList({0});
    ListNode* expected2 = TestHelpers::CreateLinkedList({0});
    auto result2 = solution.AddTwoNumbers(l12, l22);
    ASSERT_LINKED_LISTS_EQ(result2, expected2);
    TestHelpers::DeleteLinkedList(expected2);
    TestHelpers::DeleteLinkedList(result2);
    TestHelpers::DeleteLinkedList(l12);
    TestHelpers::DeleteLinkedList(l22);

    TEST_CASE("Example 3");
    ListNode* l13 = TestHelpers::CreateLinkedList({9,9,9,9,9,9,9});
    ListNode* l23 = TestHelpers::CreateLinkedList({9,9,9,9});
    ListNode* expected3 = TestHelpers::CreateLinkedList({8,9,9,9,0,0,0,1});
    auto result3 = solution.AddTwoNumbers(l13, l23);
    ASSERT_LINKED_LISTS_EQ(result3, expected3);
    TestHelpers::DeleteLinkedList(expected3);
    TestHelpers::DeleteLinkedList(result3);
    TestHelpers::DeleteLinkedList(l13);
    TestHelpers::DeleteLinkedList(l23);
    
    TestRunner::PrintSummary();
}

REGISTER_SOLUTION(2, "Add Two Numbers", TestProblem2);

#endif // PROBLEM_2_H
