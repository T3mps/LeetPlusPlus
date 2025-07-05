
--[[
    DEPENDENCY MANAGEMENT GUIDE
    
    To add a new dependency, simply define it in the Dependencies table below.
    
    Example dependency definition:
    
    MyDependency = {
        LibName = "...",         -- Base name of the library file (no .lib/.a extension)
        LibDir = "...",          -- Directory containing the library file (can use %{cfg.buildcfg})
        IncludeDir = "...",      -- Directory for header files
        Windows = {              -- Platform-specific settings (can also use Linux)
            DebugLibName = "..." -- Alternative name for debug builds
        },
        Configurations = "Debug,Release" -- Comma-separated list of configurations
    }
    
    KEY CONCEPTS:
    
    - Property Scopes: Most properties can be defined globally or in platform-specific 
      scopes (Windows/Linux). The Configurations property must be global.
    
    - Header-Only Libraries: For header-only libraries, simply specify IncludeDir 
      and omit LibName.
    
    - Configurations: If omitted, the dependency will be used in all configurations.
    
    - Build Integration: Once defined here, dependencies are automatically included 
      and linked - no need to manually update "links" or "includedirs" elsewhere.
    
    For best results, examine existing dependency definitions when adding new ones.
]]--

Dependencies = {
    PDCurses = {
        IncludeDir = "%{wks.location}/vendor/PDCurses",
        Windows = {
            LibDir = "%{wks.location}/vendor/PDCurses/wincon",
            LibName = "pdcurses",
        },
        Linux = {
            LibDir = "%{wks.location}/vendor/PDCurses/x11",
            LibName = "pdcurses",
        }
    }
}

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

function firstToUpper(str)
	return (str:gsub("^%l", string.upper))
end

function __genOrderedIndex( t )
    local orderedIndex = {}
    for key in pairs(t) do
        table.insert( orderedIndex, key )
    end
    table.sort( orderedIndex )
    return orderedIndex
end

function getTableSize(t)
    local count = 0
    for _, __ in pairs(t) do
        count = count + 1
    end
    return count
end

function orderedNext(t, state)
    -- Equivalent of the next function, but returns the keys in the alphabetic
    -- order. We use a temporary ordered key table that is stored in the
    -- table being iterated.

    local key = nil
    if state == nil then
        -- the first time, generate the index
        t.__orderedIndex = __genOrderedIndex( t )
        key = t.__orderedIndex[1]
    else
        -- fetch the next value
        for i = 1, getTableSize(t) do
            if t.__orderedIndex[i] == state then
                key = t.__orderedIndex[i+1]
            end
        end
    end

    if key then
        return key, t[key]
    end

    t.__orderedIndex = nil
    return
end

function orderedPairs(t)
    -- Equivalent of the pairs() function on tables. Allows to iterate
    -- in order
    return orderedNext, t, nil
end

function LinkDependency(table, is_debug, target)

	-- Setup library directory
	if table.LibDir ~= nil then
		libdirs { table.LibDir }
	end

	-- Try linking
	local libraryName = nil
	if table.LibName ~= nil then
		libraryName = table.LibName
	end

	if table.DebugLibName ~= nil and is_debug and target == "Windows" then
		libraryName = table.DebugLibName
	end

	if libraryName ~= nil then
		links { libraryName }
		return true
	end

	return false
end

function AddDependencyIncludes(table)
	if table.IncludeDir ~= nil then
		externalincludedirs { table.IncludeDir }
	end
end

function ProcessDependencies(config_name)
	local target = firstToUpper(os.target())

	for key, libraryData in orderedPairs(Dependencies) do

		-- Always match config_name if no Configurations list is specified
		local matchesConfiguration = true

		if config_name ~= nil and libraryData.Configurations ~= nil then
			matchesConfiguration = string.find(libraryData.Configurations, config_name)
		end

		local isDebug = config_name == "Debug"

		if matchesConfiguration then
			local continueLink = true

			-- Process Platform Scope
			if libraryData[target] ~= nil then
				continueLink = not LinkDependency(libraryData[target], isDebug, target)
				AddDependencyIncludes(libraryData[target])
			end

			-- Process Global Scope
			if continueLink then
				LinkDependency(libraryData, isDebug, target)
			end

			AddDependencyIncludes(libraryData)
		end

	end
end

function IncludeDependencies(config_name)
	local target = firstToUpper(os.target())

	for key, libraryData in orderedPairs(Dependencies) do

		-- Always match config_name if no Configurations list is specified
		local matchesConfiguration = true

		if config_name ~= nil and libraryData.Configurations ~= nil then
			matchesConfiguration = string.find(libraryData.Configurations, config_name)
		end

		if matchesConfiguration then
			-- Process Global Scope
			AddDependencyIncludes(libraryData)

			-- Process Platform Scope
			if libraryData[target] ~= nil then
				AddDependencyIncludes(libraryData[target])
			end
		end

	end
end
