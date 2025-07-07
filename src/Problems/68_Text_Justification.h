#ifndef PROBLEM_68_H
#define PROBLEM_68_H

/**
 * Problem 68: Text Justification
 * Difficulty: Hard
 * Topics: Array, String, Simulation
 * Companies: Unknown
 */

#include <iostream>
#include <string>
#include <vector>
#include "../Base/TestUtils.h"

class Solution68
{
public:
    std::vector<std::string> FullJustify(std::vector<std::string>& words, int maxWidth)
    {
        // TODO: Implement solution
        return {};
    }
};

void TestProblem68()
{
    Solution68 solution;
    TestRunner::Start("Text Justification");
    
        TEST_CASE("Example 1");
    std::vector<std::string> words1 = {&quot;This&quot;, &quot;is&quot;, &quot;an&quot;, &quot;example&quot;, &quot;of&quot;, &quot;text&quot;, &quot;justification.&quot;};
    int maxWidth1 = 16;
    std::vector<std::string> expected1 = [;
    ASSERT_EQ(solution.FullJustify(words1, maxWidth1), expected1);

    TEST_CASE("Example 2");
    std::vector<std::string> words2 = {&quot;What&quot;,&quot;must&quot;,&quot;be&quot;,&quot;acknowledgment&quot;,&quot;shall&quot;,&quot;be&quot;};
    int maxWidth2 = 16;
    std::vector<std::string> expected2 = [;
    ASSERT_EQ(solution.FullJustify(words2, maxWidth2), expected2);

    TEST_CASE("Example 3");
    std::vector<std::string> words3 = {&quot;Science&quot;,&quot;is&quot;,&quot;what&quot;,&quot;we&quot;,&quot;understand&quot;,&quot;well&quot;,&quot;enough&quot;,&quot;to&quot;,&quot;explain&quot;,&quot;to&quot;,&quot;a&quot;,&quot;computer.&quot;,&quot;Art&quot;,&quot;is&quot;,&quot;everything&quot;,&quot;else&quot;,&quot;we&quot;,&quot;do&quot;};
    int maxWidth3 = 20;
    std::vector<std::string> expected3 = [;
    ASSERT_EQ(solution.FullJustify(words3, maxWidth3), expected3);
    
    TestRunner::PrintSummary();
}

REGISTER_SOLUTION(68, "Text Justification", TestProblem68);

#endif // PROBLEM_68_H
