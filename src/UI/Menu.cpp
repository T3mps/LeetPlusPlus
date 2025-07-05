#include "Menu.h"
#include <algorithm>
#include <cstdio>

namespace UI
{
    Menu::Menu(int height, int width, int y, int x, bool hasBorder)
        : Window(height, width, y, x, hasBorder), 
          m_selectedIndex(0), m_highlightColor(1), m_showDescriptions(false),
          m_scrollOffset(0), m_fixedBottomItems(0)
    {
    }

    void Menu::AddItem(const MenuItem& item)
    {
        m_items.push_back(item);
        
        if (m_selectedIndex == -1 && item.enabled)
        {
            m_selectedIndex = (int)m_items.size() - 1;
        }
    }

    void Menu::AddItem(const std::string& label, std::function<void()> action)
    {
        AddItem(MenuItem(label, "", action, true));
    }
    
    void Menu::AddColoredItem(const std::string& label, int colorPair, std::function<void()> action)
    {
        AddItem(MenuItem(label, "", action, true, colorPair));
    }
    
    void Menu::AddProblemItem(int number, const std::string& title, int colorPair, std::function<void()> action)
    {
        AddItem(MenuItem(number, title, colorPair, action));
    }

    void Menu::AddSeparator()
    {
        MenuItem separator("---", "", nullptr, false);
        m_items.push_back(separator);
    }

    void Menu::RemoveItem(int index)
    {
        if (index >= 0 && index < m_items.size())
        {
            m_items.erase(m_items.begin() + index);
            
            if (m_selectedIndex >= m_items.size())
            {
                m_selectedIndex = (int)m_items.size() - 1;
            }
            
            if (m_selectedIndex >= 0 && !IsSelectableIndex(m_selectedIndex))
            {
                m_selectedIndex = GetNextSelectableIndex(m_selectedIndex);
            }
            
            // Adjust scroll offset if needed
            if (m_scrollOffset > 0 && m_scrollOffset >= (int)m_items.size() - m_fixedBottomItems)
            {
                m_scrollOffset = std::max(0, (int)m_items.size() - m_fixedBottomItems - 1);
            }
        }
    }

    void Menu::ClearItems()
    {
        m_items.clear();
        m_selectedIndex = -1;
        m_scrollOffset = 0;
    }

    void Menu::Draw()
    {
        Window::Draw();
        
        if (!m_visible) return;
        
        int contentAreaHeight = m_hasBorder ? m_height - 2 : m_height;
        int startY = m_hasBorder ? 1 : 0;
        
        // Calculate space for scrollable items
        int scrollableItems = (int)m_items.size() - m_fixedBottomItems;
        int spaceForFixed = m_fixedBottomItems;
        int spaceForScrollable = contentAreaHeight - spaceForFixed;
        
        // Adjust scroll offset based on selected index
        if (m_selectedIndex < scrollableItems)
        {
            // Selected item is in scrollable area
            if (m_selectedIndex >= m_scrollOffset + spaceForScrollable)
            {
                m_scrollOffset = m_selectedIndex - spaceForScrollable + 1;
            }
            else if (m_selectedIndex < m_scrollOffset)
            {
                m_scrollOffset = m_selectedIndex;
            }
        }
        
        // Draw scrollable items
        int drawnLines = 0;
        for (int i = 0; i < spaceForScrollable && (i + m_scrollOffset) < scrollableItems; ++i)
        {
            DrawMenuItem(i + m_scrollOffset, startY + i);
            drawnLines++;
        }
        
        // Draw fixed bottom items
        int fixedStartY = startY + contentAreaHeight - m_fixedBottomItems;
        for (int i = 0; i < m_fixedBottomItems && (scrollableItems + i) < m_items.size(); ++i)
        {
            DrawMenuItem(scrollableItems + i, fixedStartY + i);
        }
        
        // Draw scroll indicators if needed
        if (m_hasBorder)
        {
            if (m_scrollOffset > 0)
            {
                mvwaddch(m_window, 0, m_width - 2, ACS_UARROW);
            }
            if (m_scrollOffset + spaceForScrollable < scrollableItems)
            {
                mvwaddch(m_window, startY + spaceForScrollable - 1, m_width - 2, ACS_DARROW);
            }
        }
    }

    void Menu::SelectNext()
    {
        if (m_items.empty()) return;
        
        int newIndex = GetNextSelectableIndex(m_selectedIndex);
        if (newIndex != -1)
        {
            m_selectedIndex = newIndex;
        }
    }

    void Menu::SelectPrevious()
    {
        if (m_items.empty()) return;
        
        int newIndex = GetPreviousSelectableIndex(m_selectedIndex);
        if (newIndex != -1)
        {
            m_selectedIndex = newIndex;
        }
    }

    void Menu::SelectItem(int index)
    {
        if (index >= 0 && index < m_items.size() && IsSelectableIndex(index))
        {
            m_selectedIndex = index;
        }
    }

    void Menu::ExecuteSelected()
    {
        if (m_selectedIndex >= 0 && m_selectedIndex < m_items.size())
        {
            const MenuItem& item = m_items[m_selectedIndex];
            if (item.enabled && item.action)
            {
                item.action();
            }
        }
    }

    const MenuItem* Menu::GetSelectedItem() const
    {
        if (m_selectedIndex >= 0 && m_selectedIndex < m_items.size())
        {
            return &m_items[m_selectedIndex];
        }
        return nullptr;
    }

    void Menu::DrawMenuItem(int index, int y)
    {
        if (index < 0 || index >= m_items.size()) return;
        
        const MenuItem& item = m_items[index];
        int x = m_hasBorder ? 2 : 1;
        int maxWidth = m_hasBorder ? m_width - 4 : m_width - 2;
        
        if (item.label == "---")
        {
            for (int i = 0; i < maxWidth; ++i)
            {
                mvwaddch(m_window, y, x + i, ACS_HLINE);
            }
            return;
        }
        
        bool isSelected = (index == m_selectedIndex && item.enabled);
        
        if (isSelected)
        {
            wattron(m_window, A_REVERSE);
        }
        
        if (!item.enabled)
        {
            wattron(m_window, A_DIM);
        }
        
        if (item.isProblem)
        {
            // Draw problem number in white
            char numberStr[10];
            snprintf(numberStr, sizeof(numberStr), "%4d. ", item.problemNumber);
            mvwprintw(m_window, y, x, "%s", numberStr);
            
            // Draw problem title in difficulty color (unless selected)
            if (!isSelected && item.colorPair > 0)
            {
                wattron(m_window, COLOR_PAIR(item.colorPair));
            }
            
            std::string displayTitle = item.problemTitle;
            int titleMaxWidth = maxWidth - 6;  // Account for number
            if ((int)displayTitle.length() > titleMaxWidth)
            {
                displayTitle = displayTitle.substr(0, titleMaxWidth - 3) + "...";
            }
            wprintw(m_window, "%s", displayTitle.c_str());
            
            // Pad the rest of the line for selection highlight
            int currentX = getcurx(m_window);
            for (int i = currentX - x; i < maxWidth; i++)
            {
                waddch(m_window, ' ');
            }
            
            if (!isSelected && item.colorPair > 0)
            {
                wattroff(m_window, COLOR_PAIR(item.colorPair));
            }
        }
        else
        {
            // Regular menu item
            if (item.colorPair > 0 && !isSelected)
            {
                wattron(m_window, COLOR_PAIR(item.colorPair));
            }
            
            std::string displayText = item.label;
            if (m_showDescriptions && !item.description.empty())
            {
                displayText += " - " + item.description;
            }
            
            if ((int)displayText.length() > maxWidth)
            {
                displayText = displayText.substr(0, maxWidth - 3) + "...";
            }
            
            mvwprintw(m_window, y, x, "%-*s", maxWidth, displayText.c_str());
            
            if (item.colorPair > 0 && !isSelected)
            {
                wattroff(m_window, COLOR_PAIR(item.colorPair));
            }
        }
        
        if (isSelected)
        {
            wattroff(m_window, A_REVERSE);
        }
        
        if (!item.enabled)
        {
            wattroff(m_window, A_DIM);
        }
    }

    bool Menu::IsSelectableIndex(int index) const
    {
        if (index < 0 || index >= (int)m_items.size()) return false;
        return m_items[index].enabled && m_items[index].label != "---";
    }

    int Menu::GetNextSelectableIndex(int current) const
    {
        for (int i = current + 1; i < (int)m_items.size(); ++i)
        {
            if (IsSelectableIndex(i)) return i;
        }
        
        for (int i = 0; i <= current; ++i)
        {
            if (IsSelectableIndex(i)) return i;
        }
        
        return -1;
    }

    int Menu::GetPreviousSelectableIndex(int current) const
    {
        for (int i = current - 1; i >= 0; --i)
        {
            if (IsSelectableIndex(i)) return i;
        }
        
        for (int i = (int)m_items.size() - 1; i >= current; --i)
        {
            if (IsSelectableIndex(i)) return i;
        }
        
        return -1;
    }

    HorizontalMenu::HorizontalMenu(int height, int width, int y, int x, bool hasBorder)
        : Menu(height, width, y, x, hasBorder)
    {
    }

    void HorizontalMenu::Draw()
    {
        Window::Draw();
        
        if (!m_visible) return;
        
        int currentX = m_hasBorder ? 1 : 0;
        int y = m_hasBorder ? 1 : 0;
        
        for (int i = 0; i < (int)m_items.size(); ++i)
        {
            DrawHorizontalMenuItem(i, currentX);
            currentX += (int)m_items[i].label.length() + 3;
        }
    }

    void HorizontalMenu::DrawHorizontalMenuItem(int index, int x)
    {
        if (index < 0 || index >= m_items.size()) return;
        
        const MenuItem& item = m_items[index];
        int y = m_hasBorder ? 1 : 0;
        
        if (index == m_selectedIndex && item.enabled)
        {
            wattron(m_window, A_REVERSE);
        }
        
        if (!item.enabled)
        {
            wattron(m_window, A_DIM);
        }
        
        mvwprintw(m_window, y, x, " %s ", item.label.c_str());
        
        if (index == m_selectedIndex && item.enabled)
        {
            wattroff(m_window, A_REVERSE);
        }
        
        if (!item.enabled)
        {
            wattroff(m_window, A_DIM);
        }
    }
}