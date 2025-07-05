#pragma once

#include <algorithm>
#include <functional>
#include <iostream>
#include <string>
#include <vector>

enum class Difficulty
{
    Easy,
    Medium,
    Hard
};

struct ProblemInfo
{
    int number;
    std::string name;
    std::string title;  // For display purposes
    Difficulty difficulty;
    std::function<void()> testFunction;
};

class SolutionRegistry
{
public:
    static SolutionRegistry& GetInstance()
    {
        static SolutionRegistry instance;
        return instance;
    }
    
    SolutionRegistry(const SolutionRegistry&) = delete;
    SolutionRegistry& operator=(const SolutionRegistry&) = delete;
    
    void RegisterProblem(int number, const std::string& name, std::function<void()> testFunc, Difficulty difficulty = Difficulty::Medium)
    {
        m_problems.push_back({number, name, name, difficulty, testFunc});  // Use name as title for now
    }
    
    void RunAll()
    {
        std::cout << "\nRunning all solutions...\n";
        for (const auto& problem : GetSortedProblems())
        {
            ExecuteProblem(problem);
            std::cout << "\n";
        }
    }
    
    void RunByNumber(int number)
    {
        for (const auto& problem : m_problems)
        {
            if (problem.number == number)
            {
                ExecuteProblem(problem);
                return;
            }
        }
        std::cout << "Problem #" << number << " not found.\n";
    }
    
    void ListAll()
    {
        std::cout << "\nAvailable Solutions:\n";
        std::cout << "===================\n";
        
        for (const auto& problem : GetSortedProblems())
        {
            std::cout << "#" << problem.number << ": " << problem.name << "\n";
        }
        std::cout << "\n";
    }
    
    size_t Count() const { return m_problems.size(); }
    
    std::vector<ProblemInfo> GetProblemList() const { return GetSortedProblems(); }

private:
    std::vector<ProblemInfo> m_problems;
    SolutionRegistry() = default;
    
    void ExecuteProblem(const ProblemInfo& problem)
    {
        std::cout << "\n========================================\n";
        std::cout << "Problem #" << problem.number << ": " << problem.name << "\n";
        std::cout << "========================================\n\n";
        
        problem.testFunction();
        
        std::cout << "========================================\n";
    }
    
    std::vector<ProblemInfo> GetSortedProblems() const
    {
        auto sorted = m_problems;
        std::sort(sorted.begin(), sorted.end(),
                [](const ProblemInfo& a, const ProblemInfo& b)
                { 
                    return a.number < b.number; 
                });
        return sorted;
    }
};

#define REGISTER_SOLUTION(number, name, testFunc) \
    namespace { \
        struct Problem##number##Registrar { \
            Problem##number##Registrar() { \
                SolutionRegistry::GetInstance().RegisterProblem(number, name, testFunc); \
            } \
        }; \
        static Problem##number##Registrar Problem##number##Instance; \
    }

#define REGISTER_SOLUTION_WITH_DIFFICULTY(number, name, testFunc, difficulty) \
    namespace { \
        struct Problem##number##Registrar { \
            Problem##number##Registrar() { \
                SolutionRegistry::GetInstance().RegisterProblem(number, name, testFunc, difficulty); \
            } \
        }; \
        static Problem##number##Registrar Problem##number##Instance; \
    }