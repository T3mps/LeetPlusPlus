#include <iostream>
#include <string>
#include <limits>

#include "Base/SolutionRegistry.h"
#include "Problems/9_Palindrome_Number.h"
#include "Problems/70_Climbing_Stairs.h"
#include "Problems/88_Merge_Sorted_Array.h"
#include "Problems/125_Valid_Palindrome.h"

void PrintMenu()
{
    std::cout << "\n========================================\n";
    std::cout << "      LeetCode Practice Framework\n";
    std::cout << "========================================\n";
    std::cout << "1. List all problems\n";
    std::cout << "2. Run specific problem by number\n";
    std::cout << "3. Run all problems\n";
    std::cout << "4. Exit\n";
    std::cout << "========================================\n";
    std::cout << "Enter your choice: ";
}

void ClearInput()
{
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

int main()
{
    auto& registry = SolutionRegistry::GetInstance();
    
    if (registry.Count() == 0)
    {
        std::cout << "No solutions registered. Please add some LeetCode problems.\n";
        return 0;
    }
    
    int choice;
    bool running = true;
    
    while (running)
    {
        PrintMenu();
        
        if (!(std::cin >> choice))
        {
            std::cout << "\nInvalid input. Please enter a number.\n";
            ClearInput();
            continue;
        }
        
        switch (choice)
        {
            case 1:
                registry.ListAll();
                break;
                
            case 2:
            {
                std::cout << "Enter problem number: ";
                int problemNumber;
                if (std::cin >> problemNumber)
                {
                    registry.RunByNumber(problemNumber);
                }
                else
                {
                    std::cout << "\nInvalid problem number.\n";
                    ClearInput();
                }
                break;
            }
            
            case 3:
                registry.RunAll();
                break;
                
            case 4:
                running = false;
                std::cout << "\nExiting... Thank you for practicing!\n";
                break;
                
            default:
                std::cout << "\nInvalid choice. Please try again.\n";
                break;
        }
        
        if (running && choice != 4)
        {
            std::cout << "\nPress Enter to continue...";
            ClearInput();
            std::cin.get();
        }
    }
    
    return 0;
}