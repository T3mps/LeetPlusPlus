#pragma once

#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>

class TestRunner
{
public:
    static void Start(const std::string& testName)
    {
        m_currentTest = testName;
        m_passed = 0;
        m_total = 0;
        std::cout << "Testing " << testName << "...\n\n";
    }
    
    template<typename T>
    static bool AssertEqual(const T& actual, const T& expected, const char* expr, int line)
    {
        m_total++;
        if (actual == expected)
        {
            m_passed++;
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
    
    template<typename T>
    static bool AssertEqual(const std::vector<T>& actual, const std::vector<T>& expected, 
                          const char* expr, int line)
    {
        m_total++;
        if (actual == expected)
        {
            m_passed++;
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

    template<typename T>
    static bool AssertEqual(T* actual, std::nullptr_t, const char* expr, int line)
    {
        m_total++;
        if (actual == nullptr)
        {
            m_passed++;
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
    
    template<typename T>
    static bool AssertEqual(std::nullptr_t, T* expected, const char* expr, int line)
    {
        m_total++;
        if (expected == nullptr)
        {
            m_passed++;
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
        m_total++;
        if (condition)
        {
            m_passed++;
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
        std::cout << "\nPassed " << m_passed << "/" << m_total << " tests";
        if (m_passed == m_total)
        {
            std::cout << " - All tests passed!\n";
        }
        else
        {
            std::cout << " - " << (m_total - m_passed) << " tests failed\n";
        }
    }
    
    static int GetPassed() { return m_passed; }
    static int GetTotal() { return m_total; }
    static int GetFailed() { return m_total - m_passed; }

private:
    static int m_passed;
    static int m_total;
    static std::string m_currentTest;
};

int TestRunner::m_passed = 0;
int TestRunner::m_total = 0;
std::string TestRunner::m_currentTest = "";

#define ASSERT_EQ(actual, expected) TestRunner::AssertEqual(actual, expected, #actual, __LINE__)

#define ASSERT_TRUE(condition) TestRunner::Assert(condition, #condition " should be true")
#define ASSERT_FALSE(condition) TestRunner::Assert(!(condition), #condition " should be false")

#define ASSERT(condition, description) TestRunner::Assert(condition, description)

#define ASSERT_NOT_NULL(ptr) TestRunner::Assert((ptr) != nullptr, #ptr " should not be null")
#define ASSERT_NULL(ptr) TestRunner::Assert((ptr) == nullptr, #ptr " should be null")

#define TEST_CASE(description) std::cout << "\nTest Case: " << description << "\n";
