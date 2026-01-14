# 🏥 Hospital Emergency Room Management System

A comprehensive Hospital Emergency Room (ER) Management System built using **custom implementations** of fundamental Data Structures in Python. This project demonstrates practical applications of **Binary Search Tree (BST)**, **Min-Heap Priority Queue**, and **FIFO Queues** without using built-in library functions.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🆕 **Patient Registration** | Register patients with emergency levels (1-5) |
| 🚨 **Priority Treatment** | Treat patients based on emergency priority using Min-Heap |
| 🔍 **Patient Search** | Fast patient lookup using Binary Search Tree |
| 🏥 **Department Queues** | Assign patients to Lab, Pharmacy, or Radiology |
| 📊 **System Reports** | Generate comprehensive statistics and reports |
| 📋 **Patient Records** | View all patients sorted by ID |
| ⏱️ **Real-time Tracking** | Track arrival times and patient status |

---

## 🔧 Data Structures Used

### 1. Binary Search Tree (BST)
- **Purpose**: Store and retrieve patient records efficiently
- **Operations**: Insert, Search, Inorder Traversal, Find Min/Max
- **Time Complexity**: O(log n) average for search/insert

### 2. Min-Heap (Priority Queue)
- **Purpose**: Manage emergency patients by priority
- **Operations**: Insert (heapify-up), Extract-Min (heapify-down)
- **Time Complexity**: O(log n) for insert/extract

### 3. Queue (FIFO)
- **Purpose**: Manage department waiting lines
- **Operations**: Enqueue, Dequeue, Peek
- **Time Complexity**: O(1) for all operations
---

**Patient Flow**

┌─────────────────┐
│  Patient Arrives │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Registration   │ ──► BST (Patient Records)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Emergency Queue │ ──► Min-Heap (Priority)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Treatment     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Department Queue │ ──► FIFO Queue
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Discharge     │
└─────────────────┘

---

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher

### Steps

1. **Clone the repository**
git clone https://github.com/uzairnayyer/emergency-room-queue-system
