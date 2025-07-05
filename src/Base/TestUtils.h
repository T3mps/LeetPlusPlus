#pragma once

#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>

class TestRunner
{
private:
    static int passed;
    static int total;
    static std::string currentTest;
    
public:
    static void Start(const std::string& testName)
    {
        currentTest = testName;
        passed = 0;
        total = 0;
        std::cout << "Testing " << testName << "...\n\n";
    }
    
    template<typename T>
    static bool AssertEqual(const T& actual, const T& expected, const char* expr, int line)
    {
        total++;
        if (actual == expected)
        {
            passed++;
            std::cout << "[PASS] Line " << line << ": " << expr << " == " << expected << "\n";
            return true;
        }
        else
        {
            std::cout << "[FAIL] Line " << line << ": " << expr << "\n";
            std::cout << "       Expected: " << expected << "\n";
            std::cout << "       Actual:   " << actual << "\n";
            return false;
        }
    }
    
    // Specialization for vectors to print contents
    template<typename T>
    static bool AssertEqual(const std::vector<T>& actual, const std::vector<T>& expected, 
                          const char* expr, int line)
    {
        total++;
        if (actual == expected)
        {
            passed++;
            std::cout << "[PASS] Line " << line << ": " << expr << " matches expected\n";
            return true;
        }
        else
        {
            std::cout << "[FAIL] Line " << line << ": " << expr << "\n";
            std::cout << "       Expected: [";
            for (size_t i = 0; i < expected.size(); ++i)
            {
                if (i > 0) std::cout << ", ";
                std::cout << expected[i];
            }
            std::cout << "]\n       Actual:   [";
            for (size_t i = 0; i < actual.size(); ++i)
            {
                if (i > 0) std::cout << ", ";
                std::cout << actual[i];
            }
            std::cout << "]\n";
            return false;
        }
    }
    
    // Overload for pointer comparisons with nullptr
    template<typename T>
    static bool AssertEqual(T* actual, std::nullptr_t, const char* expr, int line)
    {
        total++;
        if (actual == nullptr)
        {
            passed++;
            std::cout << "[PASS] Line " << line << ": " << expr << " == nullptr\n";
            return true;
        }
        else
        {
            std::cout << "[FAIL] Line " << line << ": " << expr << "\n";
            std::cout << "       Expected: nullptr\n";
            std::cout << "       Actual:   " << actual << " (non-null pointer)\n";
            return false;
        }
    }
    
    // Overload for nullptr comparisons (reversed order)
    template<typename T>
    static bool AssertEqual(std::nullptr_t, T* expected, const char* expr, int line)
    {
        total++;
        if (expected == nullptr)
        {
            passed++;
            std::cout << "[PASS] Line " << line << ": " << expr << " == nullptr\n";
            return true;
        }
        else
        {
            std::cout << "[FAIL] Line " << line << ": " << expr << "\n";
            std::cout << "       Expected: " << expected << " (non-null pointer)\n";
            std::cout << "       Actual:   nullptr\n";
            return false;
        }
    }
    
    // Custom assertion with description
    static bool Assert(bool condition, const std::string& description)
    {
        total++;
        if (condition)
        {
            passed++;
            std::cout << "[PASS] " << description << "\n";
            return true;
        }
        else
        {
            std::cout << "[FAIL] " << description << "\n";
            return false;
        }
    }
    
    static void PrintSummary()
    {
        std::cout << "\nPassed " << passed << "/" << total << " tests";
        if (passed == total)
        {
            std::cout << " - All tests passed!\n";
        }
        else
        {
            std::cout << " - " << (total - passed) << " tests failed\n";
        }
    }
    
    static int GetPassed() { return passed; }
    static int GetTotal() { return total; }
    static int GetFailed() { return total - passed; }
};

// Initialize static members
int TestRunner::passed = 0;
int TestRunner::total = 0;
std::string TestRunner::currentTest = "";

// Convenience macros
#define ASSERT_EQ(actual, expected) \
    TestRunner::AssertEqual(actual, expected, #actual, __LINE__)

#define ASSERT_TRUE(condition) \
    TestRunner::Assert(condition, #condition " should be true")

#define ASSERT_FALSE(condition) \
    TestRunner::Assert(!(condition), #condition " should be false")

#define ASSERT(condition, description) \
    TestRunner::Assert(condition, description)

// For manual test cases where you want to show input/output
#define TEST_CASE(description) \
    std::cout << "\nTest Case: " << description << "\n";

// Check that a pointer is not null
#define ASSERT_NOT_NULL(ptr) \
    TestRunner::Assert((ptr) != nullptr, #ptr " should not be null")

// Check that a pointer is null  
#define ASSERT_NULL(ptr) \
    TestRunner::Assert((ptr) == nullptr, #ptr " should be null")