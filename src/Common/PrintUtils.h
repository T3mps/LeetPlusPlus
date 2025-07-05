#pragma once

#include <iostream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <map>
#include <set>
#include <queue>
#include <stack>
#include <string>
#include <sstream>
#include <iomanip>

#include "LeetCodeStructures.h"

class PrintUtils
{
public:
    template<typename T>
    static void Print(const std::string& label, const T& value)
    {
        std::cout << label << ": " << value << "\n";
    }
    
    template<typename T>
    static void Print(const std::string& label, const std::vector<T>& vec)
    {
        std::cout << label << ": [";
        for (size_t i = 0; i < vec.size(); ++i)
        {
            std::cout << vec[i];
            if (i < vec.size() - 1) std::cout << ", ";
        }
        std::cout << "]\n";
    }
    
    template<typename T>
    static void Print(const std::string& label, const std::vector<std::vector<T>>& matrix)
    {
        std::cout << label << ":\n";
        for (const auto& row : matrix)
        {
            std::cout << "  [";
            for (size_t i = 0; i < row.size(); ++i)
            {
                std::cout << std::setw(3) << row[i];
                if (i < row.size() - 1) std::cout << ", ";
            }
            std::cout << "]\n";
        }
    }
    
    template<typename K, typename V>
    static void Print(const std::string& label, const std::unordered_map<K, V>& map)
    {
        std::cout << label << ": {";
        bool first = true;
        for (const auto& [key, value] : map)
        {
            if (!first) std::cout << ", ";
            std::cout << key << ": " << value;
            first = false;
        }
        std::cout << "}\n";
    }
    
    template<typename K, typename V>
    static void Print(const std::string& label, const std::map<K, V>& map)
    {
        std::cout << label << ": {";
        bool first = true;
        for (const auto& [key, value] : map)
        {
            if (!first) std::cout << ", ";
            std::cout << key << ": " << value;
            first = false;
        }
        std::cout << "}\n";
    }
    
    template<typename T>
    static void Print(const std::string& label, const std::set<T>& set)
    {
        std::cout << label << ": {";
        bool first = true;
        for (const auto& item : set)
        {
            if (!first) std::cout << ", ";
            std::cout << item;
            first = false;
        }
        std::cout << "}\n";
    }
    
    template<typename T>
    static void Print(const std::string& label, const std::unordered_set<T>& set)
    {
        std::cout << label << ": {";
        bool first = true;
        for (const auto& item : set)
        {
            if (!first) std::cout << ", ";
            std::cout << item;
            first = false;
        }
        std::cout << "}\n";
    }
    
    static void PrintSeparator(char c = '=', int length = 40)
    {
        std::cout << std::string(length, c) << "\n";
    }
    
    static void PrintHeader(const std::string& title)
    {
        PrintSeparator();
        std::cout << title << "\n";
        PrintSeparator();
    }
    
    static void Print(const std::string& label, ListNode* head)
    {
        std::cout << label << ": ";
        if (!head)
        {
            std::cout << "null\n";
            return;
        }
        
        while (head)
        {
            std::cout << head->val;
            if (head->next) std::cout << " -> ";
            head = head->next;
        }
        std::cout << "\n";
    }
    
    static void Print(const std::string& label, TreeNode* root)
    {
        std::cout << label << ": ";
        if (!root)
        {
            std::cout << "null\n";
            return;
        }
        
        std::vector<std::string> result;
        std::queue<TreeNode*> q;
        q.push(root);
        
        while (!q.empty())
        {
            TreeNode* node = q.front();
            q.pop();
            
            if (node)
            {
                result.push_back(std::to_string(node->val));
                q.push(node->left);
                q.push(node->right);
            }
            else
            {
                result.push_back("null");
            }
        }
        
        while (!result.empty() && result.back() == "null")
        {
            result.pop_back();
        }
        
        std::cout << "[";
        for (size_t i = 0; i < result.size(); ++i)
        {
            std::cout << result[i];
            if (i < result.size() - 1) std::cout << ", ";
        }
        std::cout << "]\n";
    }
};