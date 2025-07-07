/**
* ██╗     ███████╗███████╗████████╗                                 
* ██║     ██╔════╝██╔════╝╚══██╔══╝                                 
* ██║     █████╗  █████╗     ██║                                    
* ██║     ██╔══╝  ██╔══╝     ██║                                    
* ███████╗███████╗███████╗   ██║                                    
* ╚══════╝╚══════╝╚══════╝   ╚═╝                                    
*                                                                   
* ██████╗ ██╗     ██╗   ██╗███████╗██████╗ ██╗     ██╗   ██╗███████╗
* ██╔══██╗██║     ██║   ██║██╔════╝██╔══██╗██║     ██║   ██║██╔════╝
* ██████╔╝██║     ██║   ██║███████╗██████╔╝██║     ██║   ██║███████╗
* ██╔═══╝ ██║     ██║   ██║╚════██║██╔═══╝ ██║     ██║   ██║╚════██║
* ██║     ███████╗╚██████╔╝███████║██║     ███████╗╚██████╔╝███████║
* ╚═╝     ╚══════╝ ╚═════╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚══════╝
*/

#include <iostream>
#include <string>
#include <limits>

#include "Base/SolutionRegistry.h"
#include "Problems/AllProblems.h"
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