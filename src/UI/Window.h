#pragma once

#include <curses.h>
#include <panel.h>
#include <string>
#include <vector>
#include <memory>

namespace UI
{
    class Window
    {
    public:
        Window(int height, int width, int y, int x, bool hasBorder = true);
        virtual ~Window();

        virtual void Draw();
        virtual void Clear();
        virtual void Refresh();
        
        void Show();
        void Hide();
        bool IsVisible() const { return m_visible; }
        
        void MoveTo(int y, int x);
        void Resize(int height, int width);
        
        void SetTitle(const std::string& title);
        const std::string& GetTitle() const { return m_title; }
        
        WINDOW* GetWindowHandle() { return m_window; }
        
        int GetHeight() const { return m_height; }
        int GetWidth() const { return m_width; }
        int GetY() const { return m_y; }
        int GetX() const { return m_x; }
        
    protected:
        void DrawBorder();
        void DrawTitle();

        WINDOW* m_window;
        PANEL* m_panel;
        int m_height;
        int m_width;
        int m_y;
        int m_x;
        std::string m_title;
        bool m_hasBorder;
        bool m_visible;
    };

    class ScrollableWindow : public Window
    {
    public:
        ScrollableWindow(int height, int width, int y, int x, bool hasBorder = true);
        
        virtual void Draw() override;
        
        void SetContent(const std::vector<std::string>& content);
        void AddLine(const std::string& line);
        void ClearContent();
        
        void ScrollUp(int lines = 1);
        void ScrollDown(int lines = 1);
        void ScrollToTop();
        void ScrollToBottom();
        
        bool CanScrollUp() const { return m_scrollOffset > 0; }
        bool CanScrollDown() const;
        
    protected:
        void DrawScrollIndicators();
    
        int m_scrollOffset;
        int m_contentHeight;
        std::vector<std::string> m_content;
    };
}