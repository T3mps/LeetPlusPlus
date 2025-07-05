#pragma once

#include <vector>
#include <queue>
#include <iostream>
#include <initializer_list>
#include <optional>

#include "Structures.h"

namespace TestHelpers
{
    TreeNode* CreateTree(const std::vector<std::optional<int>>& values)
    {
        if (values.empty() || !values[0].has_value())
            return nullptr;
        
        TreeNode* root = new TreeNode(values[0].value());
        std::queue<TreeNode*> queue;
        queue.push(root);
        
        size_t i = 1;
        while (!queue.empty() && i < values.size())
        {
            TreeNode* node = queue.front();
            queue.pop();
            
            if (i < values.size() && values[i].has_value())
            {
                node->left = new TreeNode(values[i].value());
                queue.push(node->left);
            }
            i++;
            
            if (i < values.size() && values[i].has_value())
            {
                node->right = new TreeNode(values[i].value());
                queue.push(node->right);
            }
            i++;
        }
        
        return root;
    }
    
    TreeNode* CreateTree(std::initializer_list<int> values)
    {
        std::vector<std::optional<int>> optValues;
        for (int val : values)
        {
            if (val == INT_MIN)
            {
                optValues.push_back(std::nullopt);
            }
            else
            {
                optValues.push_back(val);
            }
        }
        return CreateTree(optValues);
    }
    
    std::vector<std::optional<int>> TreeToVector(TreeNode* root)
    {
        std::vector<std::optional<int>> result;
        if (!root)
            return result;
        
        std::queue<TreeNode*> queue;
        queue.push(root);
        
        while (!queue.empty())
        {
            TreeNode* node = queue.front();
            queue.pop();
            
            if (node)
            {
                result.push_back(node->val);
                queue.push(node->left);
                queue.push(node->right);
            }
            else
            {
                result.push_back(std::nullopt);
            }
        }
        
        while (!result.empty() && !result.back().has_value())
        {
            result.pop_back();
        }
        
        return result;
    }
    
    void PrintTree(TreeNode* root)
    {
        auto values = TreeToVector(root);
        std::cout << "[";
        for (size_t i = 0; i < values.size(); ++i)
        {
            if (i > 0)
                std::cout << ", ";
            if (values[i].has_value())
            {
                std::cout << values[i].value();
            }
            else
            {
                std::cout << "null";
            }
        }
        std::cout << "]";
    }
    
    bool TreesEqual(TreeNode* p, TreeNode* q)
    {
        if (!p && !q)
            return true;
        if (!p || !q)
            return false;
        return p->val == q->val && TreesEqual(p->left, q->left) && TreesEqual(p->right, q->right);
    }
    
    void DeleteTree(TreeNode* root)
    {
        if (!root)
            return;
        DeleteTree(root->left);
        DeleteTree(root->right);
        delete root;
    }
    
    template<typename T>
    void PrintVector(const std::vector<T>& vec)
    {
        std::cout << "[";
        for (size_t i = 0; i < vec.size(); ++i)
        {
            if (i > 0) std::cout << ", ";
            std::cout << vec[i];
        }
        std::cout << "]";
    }
    
    ListNode* CreateLinkedList(const std::vector<int>& values)
    {
        if (values.empty())
            return nullptr;
        
        ListNode* head = new ListNode(values[0]);
        ListNode* current = head;
        
        for (size_t i = 1; i < values.size(); ++i)
        {
            current->next = new ListNode(values[i]);
            current = current->next;
        }
        
        return head;
    }
    
    std::vector<int> LinkedListToVector(ListNode* head)
    {
        std::vector<int> result;
        while (head)
        {
            result.push_back(head->val);
            head = head->next;
        }
        return result;
    }
    
    void PrintLinkedList(ListNode* head)
    {
        if (!head)
        {
            std::cout << "[]";
            return;
        }
        
        std::cout << "[";
        bool first = true;
        while (head)
        {
            if (!first)
                std::cout << " -> ";
            std::cout << head->val;
            head = head->next;
            first = false;
        }
        std::cout << "]";
    }
    
    void DeleteLinkedList(ListNode* head)
    {
        while (head)
        {
            ListNode* temp = head;
            head = head->next;
            delete temp;
        }
    }
}