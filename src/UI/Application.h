#pragma once

#include <functional>
#include <memory>
#include <string>
#include <vector>

#include "curses.h"

namespace UI
{
    class Window;
    
    enum class ColorPair
    {
        Default = 1,
        MenuHighlight,
        Success,
        Error,
        Warning,
        Info,
        StatusBar,
        TitleBar,
        Easy,
        Medium,
        Hard
    };

    class Menu;
    class ScrollableWindow;
    
    class Application
    {
    public:
        Application();
        ~Application();
        
        static Application& GetInstance();
        
        bool Initialize();
        void Shutdown();
        
        void Run();
        void Stop() { m_running = false; }
        
        void AddWindow(std::unique_ptr<Window> window);
        void RemoveWindow(Window* window);
        void SetActiveWindow(Window* window);
        
        int GetScreenHeight() const { return m_screenHeight; }
        int GetScreenWidth() const { return m_screenWidth; }
        
        void RefreshScreen();
        void ResizeHandler();
        
        void ShowMessage(const std::string& message, bool waitForKey = true);
        void ShowError(const std::string& error, bool waitForKey = true);
        bool ShowConfirmation(const std::string& message);
        
    private:
        void OnInitialize();
        void OnShutdown();
        void OnUpdate();
        bool OnKeyPress(int key);
        
        void InitializeColors();
        void UpdateScreenSize();
        void DrawWindows();
        
        void ShowMainMenu();
        void RunProblem(int problemNumber);
        void DrawLegend();

        inline static Application* s_Instance = nullptr;

        bool m_running;
        bool m_initialized;
        std::vector<std::unique_ptr<Window>> m_windows;
        Window* m_activeWindow;

        int m_screenHeight;
        int m_screenWidth;
        
        std::unique_ptr<Menu> m_mainMenu;
        std::unique_ptr<Window> m_problemRunner;
    };

}