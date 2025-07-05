#include "Application.h"
#include "Window.h"
#include "Menu.h"
#include "Base/SolutionRegistry.h"
#include <algorithm>
#include <sstream>
#include <iomanip>

namespace UI
{
    Application::Application()
        : m_running(false), m_initialized(false), m_activeWindow(nullptr),
          m_screenHeight(0), m_screenWidth(0)
    {
        s_Instance = this;
    }

    Application::~Application()
    {
        if (m_initialized)
        {
            Shutdown();
        }
        s_Instance = nullptr;
    }

    Application& Application::GetInstance()
    {
        return *s_Instance;
    }

    bool Application::Initialize()
    {
        if (m_initialized) return true;
        
        initscr();
        
        if (has_colors())
        {
            start_color();
            InitializeColors();
        }
        
        cbreak();
        noecho();
        keypad(stdscr, TRUE);
        curs_set(0);
        
        UpdateScreenSize();
        
        m_initialized = true;
        
        OnInitialize();
        
        return true;
    }

    void Application::Shutdown()
    {
        if (!m_initialized) return;
        
        OnShutdown();
        
        m_windows.clear();
        
        endwin();
        m_initialized = false;
    }

    void Application::Run()
    {
        if (!m_initialized) return;
        
        m_running = true;
        
        while (m_running)
        {
            DrawWindows();
            
            // Draw managed UI components
            if (m_mainMenu && m_mainMenu->IsVisible())
            {
                m_mainMenu->Draw();
                DrawLegend();
            }
            if (m_problemRunner && m_problemRunner->IsVisible())
            {
                m_problemRunner->Draw();
            }
            
            RefreshScreen();
            
            int ch = getch();
            
            if (ch == KEY_RESIZE)
            {
                ResizeHandler();
            }
            else if (!OnKeyPress(ch))
            {
                if (ch == 27 || ch == 'q' || ch == 'Q')
                {
                    if (ShowConfirmation("Are you sure you want to exit?"))
                    {
                        m_running = false;
                    }
                }
            }
            
            OnUpdate();
        }
    }

    void Application::AddWindow(std::unique_ptr<Window> window)
    {
        m_windows.push_back(std::move(window));
    }

    void Application::RemoveWindow(Window* window)
    {
        auto it = std::find_if(m_windows.begin(), m_windows.end(),
            [window](const std::unique_ptr<Window>& w) { return w.get() == window; });
            
        if (it != m_windows.end())
        {
            if (m_activeWindow == window)
            {
                m_activeWindow = nullptr;
            }
            m_windows.erase(it);
        }
    }

    void Application::SetActiveWindow(Window* window)
    {
        m_activeWindow = window;
    }

    void Application::RefreshScreen()
    {
        update_panels();
        doupdate();
    }

    void Application::ResizeHandler()
    {
        endwin();
        refresh();
        UpdateScreenSize();
        
        for (auto& window : m_windows)
        {
            window->Draw();
        }
    }

    void Application::ShowMessage(const std::string& message, bool waitForKey)
    {
        int msgWidth = std::min((int)message.length() + 4, m_screenWidth - 10);
        int msgHeight = 5;
        int y = (m_screenHeight - msgHeight) / 2;
        int x = (m_screenWidth - msgWidth) / 2;
        
        auto msgWindow = std::make_unique<Window>(msgHeight, msgWidth, y, x);
        msgWindow->SetTitle("Message");
        msgWindow->Draw();
        
        mvwprintw(msgWindow->GetWindowHandle(), 2, 2, "%s", message.c_str());
        
        if (waitForKey)
        {
            mvwprintw(msgWindow->GetWindowHandle(), msgHeight - 2, 2, "Press any key to continue...");
        }
        
        msgWindow->Refresh();
        
        if (waitForKey)
        {
            getch();
        }
    }

    void Application::ShowError(const std::string& error, bool waitForKey)
    {
        ShowMessage("ERROR: " + error, waitForKey);
    }

    bool Application::ShowConfirmation(const std::string& message)
    {
        int msgWidth = std::min((int)message.length() + 4, m_screenWidth - 10);
        int msgHeight = 6;
        int y = (m_screenHeight - msgHeight) / 2;
        int x = (m_screenWidth - msgWidth) / 2;
        
        auto msgWindow = std::make_unique<Window>(msgHeight, msgWidth, y, x);
        msgWindow->SetTitle("Confirm");
        msgWindow->Draw();
        
        mvwprintw(msgWindow->GetWindowHandle(), 2, 2, "%s", message.c_str());
        mvwprintw(msgWindow->GetWindowHandle(), msgHeight - 2, 2, "[Y]es / [N]o");
        
        msgWindow->Refresh();
        
        while (true)
        {
            int ch = getch();
            if (ch == 'y' || ch == 'Y') return true;
            if (ch == 'n' || ch == 'N' || ch == 27) return false;
        }
    }

    void Application::InitializeColors()
    {
        init_pair(static_cast<int>(ColorPair::Default), COLOR_WHITE, COLOR_BLACK);
        init_pair(static_cast<int>(ColorPair::MenuHighlight), COLOR_BLACK, COLOR_WHITE);
        init_pair(static_cast<int>(ColorPair::Success), COLOR_GREEN, COLOR_BLACK);
        init_pair(static_cast<int>(ColorPair::Error), COLOR_RED, COLOR_BLACK);
        init_pair(static_cast<int>(ColorPair::Warning), COLOR_YELLOW, COLOR_BLACK);
        init_pair(static_cast<int>(ColorPair::Info), COLOR_CYAN, COLOR_BLACK);
        init_pair(static_cast<int>(ColorPair::StatusBar), COLOR_WHITE, COLOR_BLUE);
        init_pair(static_cast<int>(ColorPair::TitleBar), COLOR_WHITE, COLOR_BLUE);
        init_pair(static_cast<int>(ColorPair::Easy), COLOR_GREEN, COLOR_BLACK);
        init_pair(static_cast<int>(ColorPair::Medium), COLOR_YELLOW, COLOR_BLACK);
        init_pair(static_cast<int>(ColorPair::Hard), COLOR_RED, COLOR_BLACK);
    }

    void Application::UpdateScreenSize()
    {
        getmaxyx(stdscr, m_screenHeight, m_screenWidth);
    }

    void Application::DrawWindows()
    {
        for (auto& window : m_windows)
        {
            if (window->IsVisible())
            {
                window->Draw();
            }
        }
    }

    // Custom ProblemRunner window class
    class ProblemRunner : public Window
    {
    private:
        std::vector<std::string> m_Output;
        
    public:
        ProblemRunner(int height, int width, int y, int x) : Window(height, width, y, x) {}
        
        void AddOutput(const std::string& line)
        {
            m_Output.push_back(line);
        }
        
        void ClearOutput()
        {
            m_Output.clear();
        }
        
        virtual void Draw() override
        {
            Window::Draw();
            
            int startY = m_hasBorder ? 1 : 0;
            int startX = m_hasBorder ? 1 : 0;
            int maxLines = m_hasBorder ? m_height - 2 : m_height;
            
            int startLine = std::max(0, (int)m_Output.size() - maxLines);
            
            for (int i = 0; i < maxLines && (startLine + i) < m_Output.size(); ++i)
            {
                mvwprintw(m_window, startY + i, startX, "%s", m_Output[startLine + i].c_str());
            }
        }
    };

    void Application::OnInitialize()
    {
        ShowMainMenu();
    }

    void Application::OnShutdown()
    {
    }
    
    void Application::OnUpdate()
    {
    }

    bool Application::OnKeyPress(int key)
    {
        if (m_mainMenu && m_mainMenu->IsVisible())
        {
            switch (key)
            {
                case KEY_UP:
                    m_mainMenu->SelectPrevious();
                    return true;
                    
                case KEY_DOWN:
                    m_mainMenu->SelectNext();
                    return true;
                    
                case '\n':
                case KEY_ENTER:
                    m_mainMenu->ExecuteSelected();
                    return true;
            }
        }
        
        return false;
    }

    void Application::ShowMainMenu()
    {
        if (m_problemRunner) m_problemRunner->Hide();
        
        if (!m_mainMenu)
        {
            auto& registry = SolutionRegistry::GetInstance();
            auto problems = registry.GetProblemList();
            
            // Calculate menu dimensions based on content
            int maxMenuHeight = GetScreenHeight() - 4;  // Leave room for legend
            int menuHeight = std::min((int)problems.size() + 3, maxMenuHeight);  // +3 for title, separator, exit
            
            // Make the menu taller if there's room
            if (menuHeight < maxMenuHeight)
            {
                menuHeight = std::min(menuHeight + 10, maxMenuHeight);  // Add up to 10 extra lines for better appearance
            }
            
            int menuWidth = 70;
            int y = (GetScreenHeight() - menuHeight) / 2 - 1;  // Center vertically with slight offset for legend
            int x = (GetScreenWidth() - menuWidth) / 2;
            
            m_mainMenu = std::make_unique<Menu>(menuHeight, menuWidth, y, x);
            m_mainMenu->SetTitle("LeetCode Solutions - Select Problem");
            
            // Add all problems to the menu
            for (const auto& problem : problems)
            {
                // Determine color based on difficulty
                int colorPair = 0;
                switch (problem.difficulty)
                {
                    case Difficulty::Easy:
                        colorPair = static_cast<int>(ColorPair::Easy);
                        break;
                    case Difficulty::Medium:
                        colorPair = static_cast<int>(ColorPair::Medium);
                        break;
                    case Difficulty::Hard:
                        colorPair = static_cast<int>(ColorPair::Hard);
                        break;
                }
                
                m_mainMenu->AddProblemItem(problem.number, problem.title, colorPair, 
                    [this, problemNumber = problem.number]() {
                        RunProblem(problemNumber);
                    });
            }
            
            m_mainMenu->AddSeparator();
            m_mainMenu->AddItem("Exit [esc]", [this]() { Stop(); });
            
            // Set the last 2 items (separator and Exit) as fixed at bottom
            m_mainMenu->SetFixedBottomItems(2);
            
            // Main menu is managed separately, don't add to windows vector
        }
        
        m_mainMenu->Show();
        SetActiveWindow(m_mainMenu.get());
    }


    void Application::RunProblem(int problemNumber)
    {
        if (!m_problemRunner)
        {
            int runnerHeight = GetScreenHeight() - 4;
            int runnerWidth = GetScreenWidth() - 10;
            int y = 2;
            int x = 5;
            
            m_problemRunner = std::make_unique<ProblemRunner>(runnerHeight, runnerWidth, y, x);
            m_problemRunner->SetTitle("Problem Runner");
            
            // Problem runner is managed separately, don't add to windows vector
        }
        
        static_cast<ProblemRunner*>(m_problemRunner.get())->ClearOutput();
        m_problemRunner->SetTitle("Running Problem #" + std::to_string(problemNumber));
        
        if (m_mainMenu) m_mainMenu->Hide();
        m_problemRunner->Show();
        
        auto& registry = SolutionRegistry::GetInstance();
        auto* runner = static_cast<ProblemRunner*>(m_problemRunner.get());
        
        runner->AddOutput("Running problem " + std::to_string(problemNumber) + "...");
        runner->AddOutput("");
        runner->Draw();
        runner->Refresh();
        
        std::stringstream output;
        auto oldBuf = std::cout.rdbuf(output.rdbuf());
        
        registry.RunByNumber(problemNumber);
        
        std::cout.rdbuf(oldBuf);
        
        std::string line;
        while (std::getline(output, line))
        {
            runner->AddOutput(line);
        }
        
        runner->AddOutput("");
        runner->AddOutput("Press any key to continue...");
        runner->Draw();
        runner->Refresh();
        
        getch();
        ShowMainMenu();
    }
    
    void Application::DrawLegend()
    {
        // Draw legend in bottom-right corner
        int legendY = m_screenHeight - 4;
        int legendX = m_screenWidth - 30;
        
        // Draw a small box for the legend
        mvprintw(legendY, legendX, "Legend:");
        
        attron(COLOR_PAIR(static_cast<int>(ColorPair::Easy)));
        mvprintw(legendY + 1, legendX + 2, "Easy");
        attroff(COLOR_PAIR(static_cast<int>(ColorPair::Easy)));
        
        attron(COLOR_PAIR(static_cast<int>(ColorPair::Medium)));
        mvprintw(legendY + 1, legendX + 9, "Medium");
        attroff(COLOR_PAIR(static_cast<int>(ColorPair::Medium)));
        
        attron(COLOR_PAIR(static_cast<int>(ColorPair::Hard)));
        mvprintw(legendY + 1, legendX + 18, "Hard");
        attroff(COLOR_PAIR(static_cast<int>(ColorPair::Hard)));
    }

}