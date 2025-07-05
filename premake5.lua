workspace "LeetPlusPlus"
    architecture "x64"
    startproject "LeetPlusPlus"

    configurations { 
        "Debug", 
        "Release", 
        "Distribution" 
    }
    
    flags { 
        "MultiProcessorCompile" 
    }

    outputdir = "%{cfg.buildcfg}-%{cfg.system}-%{cfg.architecture}"

    newaction {
        trigger = "new-problem",
        description = "Generate a new LeetCode problem solution",
        execute = function()
            local number = _ARGS[1]
            if not number then
                print("Usage: premake5 new-problem <number> [--title=\"Problem Title\"] [--signature=\"return_type method(params)\"]")
                print("Example: premake5 new-problem 42 --title=\"Trapping Rain Water\" --signature=\"int trap(vector<int>& height)\"")
                return
            end
            
            local cmd = "python tools\\generate_solution.py new " .. number
            
            if _OPTIONS["title"] then
                cmd = cmd .. " --title \"" .. _OPTIONS["title"] .. "\""
            end
            
            if _OPTIONS["signature"] then
                cmd = cmd .. " --signature \"" .. _OPTIONS["signature"] .. "\""
            end
            
            if _OPTIONS["difficulty"] then
                cmd = cmd .. " --difficulty " .. _OPTIONS["difficulty"]
            end
            
            if _OPTIONS["topics"] then
                cmd = cmd .. " --topics " .. _OPTIONS["topics"]
            end
            
            print("Generating solution for problem " .. number .. "...")
            local result = os.execute(cmd)
            
            if result == true or result == 0 then
                print("\nRegenerating Visual Studio project files...")
                os.execute("premake5 vs2022")
                print("\nSolution generated successfully!")
                print("Next steps:")
                print("1. Reload the solution in Visual Studio")
                print("2. Find your new file in the Problems folder")
                print("3. Implement the Solve method")
            else
                print("\nFailed to generate solution. Please check the error messages above.")
            end
        end
    }
    
    newaction {
        trigger = "new-problem-interactive",
        description = "Generate a new LeetCode problem solution interactively",
        execute = function()
            print("Starting interactive problem generator...\n")
            local result = os.execute("python tools\\generate_solution.py interactive")
            
            if result == true or result == 0 then
                print("\nRegenerating Visual Studio project files...")
                os.execute("premake5 vs2022")
            end
        end
    }
    
    newaction {
        trigger = "list-problems",
        description = "List all generated LeetCode problems",
        execute = function()
            os.execute("python tools\\generate_solution.py list")
        end
    }
    
    newaction {
        trigger = "quick-add",
        description = "Quickly add a common LeetCode problem",
        execute = function()
            local problem = _ARGS[1]
            if not problem then
                print("Usage: premake5 quick-add <problem-key>")
                print("Available problems: two-sum, 3sum, lru-cache")
                return
            end
            
            local quickProblems = {
                ["two-sum"] = "1",
                ["3sum"] = "15",
                ["lru-cache"] = "146"
            }
            
            local problemNumber = quickProblems[problem:lower()]
            if problemNumber then
                print("Adding problem from metadata: " .. problem)
                os.execute("python tools\\generate_solution.py new " .. problemNumber)
                os.execute("premake5 vs2022")
            else
                print("Unknown problem: " .. problem)
            end
        end
    }

    newoption {
        trigger = "title",
        value = "STRING",
        description = "Problem title for new-problem command"
    }
    
    newoption {
        trigger = "signature", 
        value = "STRING",
        description = "Method signature for new-problem command"
    }
    
    newoption {
        trigger = "difficulty",
        value = "STRING",
        description = "Problem difficulty (Easy/Medium/Hard)"
    }
    
    newoption {
        trigger = "topics",
        value = "STRING",
        description = "Comma-separated list of topics"
    }

    project "LeetPlusPlus"
        kind "ConsoleApp"
        language "C++"
        cppdialect "C++20"
        staticruntime "off"

        targetdir ("bin/" .. outputdir .. "/%{prj.name}")
        objdir ("bin-int/" .. outputdir .. "/%{prj.name}")

        files {
            "src/**.h",
            "src/**.c",
            "src/**.hpp",
            "src/**.cpp",
        }

        includedirs {
            "src"
        }

        filter "configurations:Debug"
            runtime "Debug"
            symbols "on"
            optimize "off"
        
        filter "configurations:Release"
            runtime "Release"
            optimize "on"
            symbols "on"
        
        filter "configurations:Distribution"
            runtime "Release"
            optimize "full"
            symbols "off"
            
        filter "system:windows"
            systemversion "latest"