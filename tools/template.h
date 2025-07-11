#ifndef PROBLEM_${number}_H
#define PROBLEM_${number}_H

/**
 * Problem ${number}: ${title}
 * Difficulty: ${difficulty}
 * Topics: ${topics}
 * Companies: ${companies}
 */

${includes}
#include "../Base/TestUtils.h"${test_helpers_include}

class Solution${number}
{
public:
    ${return_type} ${method_name}(${params})
    {
        // TODO: Implement solution
        ${default_return}
    }
};

void TestProblem${number}()
{
    Solution${number} solution;
    TestRunner::Start("${title}");
    
    ${test_cases}
    
    TestRunner::PrintSummary();
}

REGISTER_SOLUTION(${number}, "${title}", TestProblem${number});

#endif // PROBLEM_${number}_H
