#pragma once

#include "Structures.h"
#include <vector>
#include <queue>
#include <algorithm>
#include <climits>
#include <sstream>

namespace TestHelpers {

    // ============== Linked List Helpers ==============
    
    /**
     * Create a linked list from a vector of values
     * @param values Vector of integers to create the list from
     * @return Head of the created linked list
     */
    inline ListNode* CreateLinkedList(const std::vector<int>& values) {
        if (values.empty()) return nullptr;
        
        ListNode* head = new ListNode(values[0]);
        ListNode* current = head;
        
        for (size_t i = 1; i < values.size(); ++i) {
            current->next = new ListNode(values[i]);
            current = current->next;
        }
        
        return head;
    }
    
    /**
     * Convert a linked list to a vector
     * @param head Head of the linked list
     * @return Vector containing all values from the list
     */
    inline std::vector<int> LinkedListToVector(ListNode* head) {
        std::vector<int> result;
        ListNode* current = head;
        
        while (current) {
            result.push_back(current->val);
            current = current->next;
        }
        
        return result;
    }
    
    /**
     * Compare two linked lists for equality
     * @param l1 First linked list
     * @param l2 Second linked list
     * @return true if lists are equal, false otherwise
     */
    inline bool CompareLinkedLists(ListNode* l1, ListNode* l2) {
        while (l1 && l2) {
            if (l1->val != l2->val) return false;
            l1 = l1->next;
            l2 = l2->next;
        }
        return l1 == nullptr && l2 == nullptr;
    }
    
    /**
     * Delete a linked list and free memory
     * @param head Head of the linked list to delete
     */
    inline void DeleteLinkedList(ListNode* head) {
        while (head) {
            ListNode* temp = head;
            head = head->next;
            delete temp;
        }
    }
    
    /**
     * Print a linked list for debugging
     * @param head Head of the linked list
     * @return String representation of the list
     */
    inline std::string LinkedListToString(ListNode* head) {
        std::stringstream ss;
        ss << "[";
        bool first = true;
        while (head) {
            if (!first) ss << ",";
            ss << head->val;
            first = false;
            head = head->next;
        }
        ss << "]";
        return ss.str();
    }
    
    // ============== Binary Tree Helpers ==============
    
    /**
     * Create a binary tree from a vector using level-order traversal
     * @param values Vector of integers (INT_MIN represents null)
     * @return Root of the created binary tree
     */
    inline TreeNode* CreateBinaryTree(const std::vector<int>& values) {
        if (values.empty() || values[0] == INT_MIN) return nullptr;
        
        TreeNode* root = new TreeNode(values[0]);
        std::queue<TreeNode*> queue;
        queue.push(root);
        
        size_t i = 1;
        while (!queue.empty() && i < values.size()) {
            TreeNode* node = queue.front();
            queue.pop();
            
            // Process left child
            if (i < values.size() && values[i] != INT_MIN) {
                node->left = new TreeNode(values[i]);
                queue.push(node->left);
            }
            i++;
            
            // Process right child
            if (i < values.size() && values[i] != INT_MIN) {
                node->right = new TreeNode(values[i]);
                queue.push(node->right);
            }
            i++;
        }
        
        return root;
    }
    
    /**
     * Convert a binary tree to vector using level-order traversal
     * @param root Root of the binary tree
     * @return Vector representation (INT_MIN for null nodes)
     */
    inline std::vector<int> TreeToVector(TreeNode* root) {
        if (!root) return {};
        
        std::vector<int> result;
        std::queue<TreeNode*> queue;
        queue.push(root);
        
        while (!queue.empty()) {
            TreeNode* node = queue.front();
            queue.pop();
            
            if (node) {
                result.push_back(node->val);
                queue.push(node->left);
                queue.push(node->right);
            } else {
                result.push_back(INT_MIN);
            }
        }
        
        // Remove trailing INT_MIN values
        while (!result.empty() && result.back() == INT_MIN) {
            result.pop_back();
        }
        
        return result;
    }
    
    /**
     * Compare two binary trees for structural equality
     * @param t1 First tree
     * @param t2 Second tree
     * @return true if trees are equal, false otherwise
     */
    inline bool CompareTrees(TreeNode* t1, TreeNode* t2) {
        if (!t1 && !t2) return true;
        if (!t1 || !t2) return false;
        
        return t1->val == t2->val &&
               CompareTrees(t1->left, t2->left) &&
               CompareTrees(t1->right, t2->right);
    }
    
    /**
     * Delete a binary tree and free memory
     * @param root Root of the tree to delete
     */
    inline void DeleteTree(TreeNode* root) {
        if (!root) return;
        DeleteTree(root->left);
        DeleteTree(root->right);
        delete root;
    }
    
    /**
     * Print a binary tree for debugging (level-order)
     * @param root Root of the tree
     * @return String representation
     */
    inline std::string TreeToString(TreeNode* root) {
        auto vec = TreeToVector(root);
        std::stringstream ss;
        ss << "[";
        for (size_t i = 0; i < vec.size(); ++i) {
            if (i > 0) ss << ",";
            if (vec[i] == INT_MIN) {
                ss << "null";
            } else {
                ss << vec[i];
            }
        }
        ss << "]";
        return ss.str();
    }
    
    // ============== Comparison Helpers ==============
    
    /**
     * Compare two vectors regardless of order
     * @param v1 First vector
     * @param v2 Second vector
     * @return true if vectors contain same elements (any order), false otherwise
     */
    template<typename T>
    inline bool CompareUnorderedVectors(const std::vector<T>& v1, const std::vector<T>& v2) {
        if (v1.size() != v2.size()) return false;
        
        std::vector<T> sorted1 = v1;
        std::vector<T> sorted2 = v2;
        std::sort(sorted1.begin(), sorted1.end());
        std::sort(sorted2.begin(), sorted2.end());
        
        return sorted1 == sorted2;
    }
    
    /**
     * Compare floating-point numbers with epsilon tolerance
     * @param a First number
     * @param b Second number
     * @param epsilon Tolerance (default 1e-6)
     * @return true if numbers are equal within tolerance
     */
    inline bool CompareFloats(double a, double b, double epsilon = 1e-6) {
        return std::abs(a - b) < epsilon;
    }
    
    /**
     * Compare vectors of floating-point numbers
     * @param v1 First vector
     * @param v2 Second vector
     * @param epsilon Tolerance for each element
     * @return true if vectors are equal within tolerance
     */
    inline bool CompareFloatVectors(const std::vector<double>& v1, 
                                   const std::vector<double>& v2, 
                                   double epsilon = 1e-6) {
        if (v1.size() != v2.size()) return false;
        
        for (size_t i = 0; i < v1.size(); ++i) {
            if (!CompareFloats(v1[i], v2[i], epsilon)) {
                return false;
            }
        }
        return true;
    }
    
    // ============== String Helpers ==============
    
    /**
     * Convert a vector to string for debugging
     * @param vec Vector to convert
     * @return String representation
     */
    template<typename T>
    inline std::string VectorToString(const std::vector<T>& vec) {
        std::stringstream ss;
        ss << "[";
        for (size_t i = 0; i < vec.size(); ++i) {
            if (i > 0) ss << ", ";
            ss << vec[i];
        }
        ss << "]";
        return ss.str();
    }
    
    /**
     * Convert a 2D vector to string for debugging
     * @param matrix 2D vector to convert
     * @return String representation
     */
    template<typename T>
    inline std::string MatrixToString(const std::vector<std::vector<T>>& matrix) {
        std::stringstream ss;
        ss << "[\n";
        for (const auto& row : matrix) {
            ss << "  " << VectorToString(row) << "\n";
        }
        ss << "]";
        return ss.str();
    }
}

// ============== Specialized ASSERT Macros ==============

#define ASSERT_LINKED_LISTS_EQ(actual, expected) \
    do { \
        if (!TestHelpers::CompareLinkedLists(actual, expected)) { \
            std::cout << "[FAIL] Line " << __LINE__ << ": Linked lists not equal\n"; \
            std::cout << "       Expected: " << TestHelpers::LinkedListToString(expected) << "\n"; \
            std::cout << "       Actual:   " << TestHelpers::LinkedListToString(actual) << "\n"; \
            TestRunner::m_total++; \
        } else { \
            std::cout << "[PASS] Line " << __LINE__ << ": Linked lists match\n"; \
            TestRunner::m_passed++; \
            TestRunner::m_total++; \
        } \
    } while(0)

#define ASSERT_TREES_EQ(actual, expected) \
    do { \
        if (!TestHelpers::CompareTrees(actual, expected)) { \
            std::cout << "[FAIL] Line " << __LINE__ << ": Trees not equal\n"; \
            std::cout << "       Expected: " << TestHelpers::TreeToString(expected) << "\n"; \
            std::cout << "       Actual:   " << TestHelpers::TreeToString(actual) << "\n"; \
            TestRunner::m_total++; \
        } else { \
            std::cout << "[PASS] Line " << __LINE__ << ": Trees match\n"; \
            TestRunner::m_passed++; \
            TestRunner::m_total++; \
        } \
    } while(0)

#define ASSERT_UNORDERED_EQ(actual, expected) \
    do { \
        if (!TestHelpers::CompareUnorderedVectors(actual, expected)) { \
            std::cout << "[FAIL] Line " << __LINE__ << ": Vectors not equal (unordered)\n"; \
            std::cout << "       Expected: " << TestHelpers::VectorToString(expected) << "\n"; \
            std::cout << "       Actual:   " << TestHelpers::VectorToString(actual) << "\n"; \
            TestRunner::m_total++; \
        } else { \
            std::cout << "[PASS] Line " << __LINE__ << ": Vectors match (unordered)\n"; \
            TestRunner::m_passed++; \
            TestRunner::m_total++; \
        } \
    } while(0)

#define ASSERT_FLOAT_EQ(actual, expected, epsilon) \
    do { \
        if (!TestHelpers::CompareFloats(actual, expected, epsilon)) { \
            std::cout << "[FAIL] Line " << __LINE__ << ": Floats not equal\n"; \
            std::cout << "       Expected: " << expected << " (±" << epsilon << ")\n"; \
            std::cout << "       Actual:   " << actual << "\n"; \
            TestRunner::m_total++; \
        } else { \
            std::cout << "[PASS] Line " << __LINE__ << ": Floats match\n"; \
            TestRunner::m_passed++; \
            TestRunner::m_total++; \
        } \
    } while(0)