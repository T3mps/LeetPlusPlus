#include "Window.h"
#include <algorithm>

namespace UI
{
    Window::Window(int height, int width, int y, int x, bool hasBorder)
        : m_height(height), m_width(width), m_y(y), m_x(x), 
          m_hasBorder(hasBorder), m_visible(true)
    {
        m_window = newwin(height, width, y, x);
        m_panel = new_panel(m_window);
        
        if (m_hasBorder)
        {
            box(m_window, 0, 0);
        }
    }

    Window::~Window()
    {
        if (m_panel)
        {
            del_panel(m_panel);
        }
        if (m_window)
        {
            delwin(m_window);
        }
    }

    void Window::Draw()
    {
        if (!m_visible) return;
        
        werase(m_window);
        
        if (m_hasBorder)
        {
            DrawBorder();
        }
        
        if (!m_title.empty())
        {
            DrawTitle();
        }
    }

    void Window::Clear()
    {
        werase(m_window);
    }

    void Window::Refresh()
    {
        if (m_visible)
        {
            update_panels();
            doupdate();
        }
    }

    void Window::Show()
    {
        m_visible = true;
        show_panel(m_panel);
    }

    void Window::Hide()
    {
        m_visible = false;
        hide_panel(m_panel);
    }

    void Window::MoveTo(int y, int x)
    {
        m_y = y;
        m_x = x;
        move_panel(m_panel, y, x);
    }

    void Window::Resize(int height, int width)
    {
        m_height = height;
        m_width = width;
        
        WINDOW* newWindow = newwin(height, width, m_y, m_x);
        replace_panel(m_panel, newWindow);
        delwin(m_window);
        m_window = newWindow;
        
        Draw();
    }

    void Window::SetTitle(const std::string& title)
    {
        m_title = title;
    }

    void Window::DrawBorder()
    {
        box(m_window, 0, 0);
    }

    void Window::DrawTitle()
    {
        if (m_title.empty()) return;
        
        int maxTitleLen = m_width - 4;
        std::string displayTitle = m_title;
        
        if ((int)displayTitle.length() > maxTitleLen)
        {
            displayTitle = displayTitle.substr(0, maxTitleLen - 3) + "...";
        }
        
        int titleX = (m_width - (int)displayTitle.length()) / 2;
        mvwprintw(m_window, 0, titleX, " %s ", displayTitle.c_str());
    }

    ScrollableWindow::ScrollableWindow(int height, int width, int y, int x, bool hasBorder)
        : Window(height, width, y, x, hasBorder), m_scrollOffset(0), m_contentHeight(0)
    {
    }

    void ScrollableWindow::Draw()
    {
        Window::Draw();
        
        if (!m_visible) return;
        
        int contentAreaHeight = m_hasBorder ? m_height - 2 : m_height;
        int contentAreaWidth = m_hasBorder ? m_width - 2 : m_width;
        int startY = m_hasBorder ? 1 : 0;
        int startX = m_hasBorder ? 1 : 0;
        
        for (int i = 0; i < contentAreaHeight && (i + m_scrollOffset) < m_content.size(); ++i)
        {
            const std::string& line = m_content[i + m_scrollOffset];
            std::string displayLine = line;
            
            if ((int)displayLine.length() > contentAreaWidth)
            {
                displayLine = displayLine.substr(0, contentAreaWidth - 3) + "...";
            }
            
            mvwprintw(m_window, startY + i, startX, "%s", displayLine.c_str());
        }
        
        DrawScrollIndicators();
    }

    void ScrollableWindow::SetContent(const std::vector<std::string>& content)
    {
        m_content = content;
        m_contentHeight = (int)content.size();
        m_scrollOffset = 0;
    }

    void ScrollableWindow::AddLine(const std::string& line)
    {
        m_content.push_back(line);
        m_contentHeight = (int)m_content.size();
    }

    void ScrollableWindow::ClearContent()
    {
        m_content.clear();
        m_contentHeight = 0;
        m_scrollOffset = 0;
    }

    void ScrollableWindow::ScrollUp(int lines)
    {
        m_scrollOffset = std::max(0, m_scrollOffset - lines);
    }

    void ScrollableWindow::ScrollDown(int lines)
    {
        int contentAreaHeight = m_hasBorder ? m_height - 2 : m_height;
        int maxOffset = std::max(0, (int)m_content.size() - contentAreaHeight);
        m_scrollOffset = std::min(maxOffset, m_scrollOffset + lines);
    }

    void ScrollableWindow::ScrollToTop()
    {
        m_scrollOffset = 0;
    }

    void ScrollableWindow::ScrollToBottom()
    {
        int contentAreaHeight = m_hasBorder ? m_height - 2 : m_height;
        m_scrollOffset = std::max(0, (int)m_content.size() - contentAreaHeight);
    }

    bool ScrollableWindow::CanScrollDown() const
    {
        int contentAreaHeight = m_hasBorder ? m_height - 2 : m_height;
        return (m_scrollOffset + contentAreaHeight) < m_content.size();
    }

    void ScrollableWindow::DrawScrollIndicators()
    {
        if (!m_hasBorder) return;
        
        if (CanScrollUp())
        {
            mvwaddch(m_window, 0, m_width - 2, ACS_UARROW);
        }
        
        if (CanScrollDown())
        {
            mvwaddch(m_window, m_height - 1, m_width - 2, ACS_DARROW);
        }
    }
}