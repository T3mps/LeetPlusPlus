#include <iostream>
#include <string>
#include <limits>

#include "Base/SolutionRegistry.h"
#include "Problems/9_Palindrome_Number.h"
#include "Problems/70_Climbing_Stairs.h"
#include "Problems/88_Merge_Sorted_Array.h"
#include "Problems/125_Valid_Palindrome.h"

#include "UI/Application.h"

int main(int argc, char* argv[])
{
    auto& registry = SolutionRegistry::GetInstance();
    
    if (registry.Count() == 0)
    {
        std::cout << "No solutions registered. Please add some LeetCode problems.\n";
        return 0;
    }

    for (int i = 1; i < argc; ++i)
    {
        std::string arg = argv[i];if (arg == "--help" || arg == "-h")
        {
            std::cout << "LeetCode Practice Framework\n";
            std::cout << "Usage: " << argv[0] << " [options]\n";
            std::cout << "Options:\n";
            std::cout << "  --no-tui, -t    Use console mode instead of TUI\n";
            std::cout << "  --help, -h      Show this help message\n";
            return 0;
        }
    }

    
    UI::Application app;
    if (app.Initialize())
    {
        app.Run();
    }
    else
    {
        return 1;
    }

    return 0;
}