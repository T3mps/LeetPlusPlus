#pragma once

#include "Window.h"
#include <functional>
#include <vector>

namespace UI
{
    struct MenuItem
    {
        std::string label;
        std::string description;
        std::function<void()> action;
        bool enabled;
        int colorPair;  // Color pair to use for this item
        
        // For problem items
        int problemNumber;
        std::string problemTitle;
        bool isProblem;
        
        MenuItem(const std::string& lbl, const std::string& desc = "", 
                std::function<void()> act = nullptr, bool en = true, int color = 0)
            : label(lbl), description(desc), action(act), enabled(en), colorPair(color),
              problemNumber(0), problemTitle(""), isProblem(false) {}
              
        MenuItem(int number, const std::string& title, int color, std::function<void()> act)
            : label(""), description(""), action(act), enabled(true), colorPair(color),
              problemNumber(number), problemTitle(title), isProblem(true) {}
    };

    class Menu : public Window
    {
    public:
        Menu(int height, int width, int y, int x, bool hasBorder = true);
        
        void AddItem(const MenuItem& item);
        void AddItem(const std::string& label, std::function<void()> action = nullptr);
        void AddColoredItem(const std::string& label, int colorPair, std::function<void()> action = nullptr);
        void AddProblemItem(int number, const std::string& title, int colorPair, std::function<void()> action);
        void AddSeparator();
        
        void RemoveItem(int index);
        void ClearItems();
        
        virtual void Draw() override;
        
        void SelectNext();
        void SelectPrevious();
        void SelectItem(int index);
        void ExecuteSelected();
        
        int GetSelectedIndex() const { return m_selectedIndex; }
        const MenuItem* GetSelectedItem() const;
        
        void SetShowDescriptions(bool show) { m_showDescriptions = show; }
        void SetFixedBottomItems(int count) { m_fixedBottomItems = count; }
        
    private:
        void DrawMenuItem(int index, int y);
        bool IsSelectableIndex(int index) const;
        int GetNextSelectableIndex(int current) const;
        int GetPreviousSelectableIndex(int current) const;

    protected:
        std::vector<MenuItem> m_items;
        int m_selectedIndex;
        int m_highlightColor;
        bool m_showDescriptions;
        int m_scrollOffset;
        int m_fixedBottomItems;
    };

    class HorizontalMenu : public Menu
    {
    public:
        HorizontalMenu(int height, int width, int y, int x, bool hasBorder = false);
        
        virtual void Draw() override;
        
    private:
        void DrawHorizontalMenuItem(int index, int x);
    };
}