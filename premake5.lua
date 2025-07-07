include "Dependencies.lua"

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
        trigger = "fetch",
        description = "Fetch a LeetCode problem from the API",
        execute = function()
            local slug = _ARGS[1]
            local cmd = "python leetcode.py fetch"
            
            if slug then
                cmd = cmd .. " " .. slug
            end
            
            print("Fetching problem" .. (slug and (": " .. slug) or " (interactive)") .. "...")
            os.execute(cmd)
        end
    }
    
    newaction {
        trigger = "solve",
        description = "Fetch a problem and open it in your editor",
        execute = function()
            local slug = _ARGS[1]
            if not slug then
                print("Usage: premake5 solve <problem-slug>")
                print("Example: premake5 solve two-sum")
                return
            end
            
            print("Fetching problem: " .. slug)
            local result = os.execute("python leetcode.py fetch " .. slug)
            
            if result == true or result == 0 then
                -- Try to open in default editor
                local files = os.matchfiles("solutions/*_" .. slug:gsub("-", "_") .. ".hpp")
                if #files > 0 then
                    print("Opening " .. files[1])
                    os.execute("start " .. files[1])  -- Windows
                    -- os.execute("open " .. files[1])  -- macOS
                    -- os.execute("xdg-open " .. files[1])  -- Linux
                end
            end
        end
    }
    
    newaction {
        trigger = "test",
        description = "Run tests for LeetCode solutions",
        execute = function()
            local problem = _ARGS[1]
            local exe = "bin/" .. outputdir .. "/LeetCodeRunner/LeetCodeRunner"
            
            if os.host() == "windows" then
                exe = exe .. ".exe"
            end
            
            if not os.isfile(exe) then
                print("Error: LeetCodeRunner not built. Run 'premake5 build' first.")
                return
            end
            
            if problem then
                os.execute(exe .. " " .. problem)
            else
                os.execute(exe)
            end
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
        
        -- Auto-generate main includes file for all problems
        local problemFiles = os.matchfiles("src/Problems/*.h")
        if #problemFiles > 0 then
            local includesContent = "// Auto-generated includes for all problems\n"
            includesContent = includesContent .. "#pragma once\n\n"
            
            for _, file in ipairs(problemFiles) do
                local filename = path.getname(file)
                includesContent = includesContent .. '#include "Problems/' .. filename .. '"\n'
            end
            
            io.writefile("src/Problems/AllProblems.h", includesContent)
        end

        includedirs { "%{wks.location}/src", "%{wks.location}/vendor" }
        
        defines { "USE_TUI" }

        filter "configurations:Debug"
            runtime "Debug"
            symbols "on"
            optimize "off"
            ProcessDependencies("Debug")
        
        filter "configurations:Release"
            runtime "Release"
            optimize "on"
            symbols "on"
            ProcessDependencies("Release")
        
        filter "configurations:Distribution"
            runtime "Release"
            optimize "full"
            symbols "off"
            ProcessDependencies("Distribution")
            
        filter "system:windows"
            systemversion "latest"
    
    -- New project for the header-only solutions
    project "LeetCodeRunner"
        kind "ConsoleApp"
        language "C++"
        cppdialect "C++17"
        staticruntime "off"
        
        targetdir ("bin/" .. outputdir .. "/%{prj.name}")
        objdir ("bin-int/" .. outputdir .. "/%{prj.name}")
        
        files {
            "solutions/main.cpp",
            "solutions/*.hpp"
        }
        
        includedirs { 
            "%{wks.location}/include"
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
            defines { "_WIN32" }