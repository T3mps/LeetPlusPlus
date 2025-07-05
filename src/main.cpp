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