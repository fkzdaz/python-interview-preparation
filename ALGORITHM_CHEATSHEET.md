# 🚀 外企算法面试速查卡

## 📋 核心解题模式

### 🔸 双指针模式 (Two Pointers)
```python
# 对撞指针 - 有序数组
left, right = 0, len(arr) - 1
while left < right:
    if condition:
        # 处理逻辑
        left += 1
    else:
        right -= 1

# 快慢指针 - 链表环检测
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast:
        return True  # 有环
```

### 🔸 滑动窗口模式 (Sliding Window)
```python
# 可变窗口
left = 0
for right in range(len(s)):
    # 扩展窗口
    window[s[right]] += 1
    
    # 收缩窗口
    while window_invalid:
        window[s[left]] -= 1
        left += 1
    
    # 更新结果
    max_len = max(max_len, right - left + 1)
```

### 🔸 DFS/BFS 模式
```python
# DFS递归
def dfs(node):
    if not node or visited[node]:
        return
    
    visited[node] = True
    # 处理当前节点
    
    for neighbor in graph[node]:
        dfs(neighbor)

# BFS队列
from collections import deque
queue = deque([start])
visited = {start}

while queue:
    node = queue.popleft()
    # 处理当前节点
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            visited.add(neighbor)
            queue.append(neighbor)
```

### 🔸 动态规划模式
```python
# 1D DP
dp = [0] * (n + 1)
dp[0] = base_case

for i in range(1, n + 1):
    dp[i] = min/max(dp[i-1] + cost, other_options)

# 2D DP
dp = [[0] * (m + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, m + 1):
        dp[i][j] = function(dp[i-1][j], dp[i][j-1])
```

### 🔸 分治模式
```python
def divide_conquer(arr, left, right):
    if left >= right:
        return base_case
    
    mid = (left + right) // 2
    left_result = divide_conquer(arr, left, mid)
    right_result = divide_conquer(arr, mid + 1, right)
    
    return merge(left_result, right_result)
```

## 🎯 常见数据结构操作复杂度

| 数据结构 | 访问 | 搜索 | 插入 | 删除 | 空间 |
|---------|------|------|------|------|------|
| 数组 | O(1) | O(n) | O(n) | O(n) | O(n) |
| 链表 | O(n) | O(n) | O(1) | O(1) | O(n) |
| 哈希表 | O(1) | O(1) | O(1) | O(1) | O(n) |
| 二叉搜索树 | O(log n) | O(log n) | O(log n) | O(log n) | O(n) |
| 堆 | O(1) | O(n) | O(log n) | O(log n) | O(n) |

## 🔥 高频面试题快速识别

### 数组/字符串
- **Two Sum** → 哈希表
- **3Sum** → 排序 + 双指针
- **最长子串** → 滑动窗口
- **旋转数组** → 二分搜索

### 链表
- **反转链表** → 三指针法
- **环检测** → Floyd快慢指针
- **合并链表** → 双指针比较

### 树
- **遍历** → DFS递归/迭代，BFS队列
- **路径问题** → DFS + 回溯
- **层次问题** → BFS

### 图
- **连通性** → DFS/BFS
- **最短路径** → BFS/Dijkstra
- **拓扑排序** → 入度 + BFS

## ⚡ 面试技巧

### 1. 解题步骤
1. **理解题意** - 复述问题，确认边界条件
2. **分析数据规模** - 确定时间复杂度要求
3. **选择算法** - 匹配解题模式
4. **编码实现** - 从简单到复杂
5. **测试验证** - 边界条件和常规案例

### 2. 时间管理
- **5分钟** - 理解题意和分析
- **15分钟** - 编码实现
- **5分钟** - 测试和优化

### 3. 沟通要点
```
"我的思路是..."
"这种方法的时间复杂度是..."
"让我考虑边界情况..."
"我觉得可以这样优化..."
"让我测试几个例子..."
```

### 4. 常见陷阱
- ❌ 整数溢出
- ❌ 空指针/空数组
- ❌ 重复元素处理
- ❌ 索引越界
- ❌ 时间复杂度过高

## 🎨 代码模板

### 二分搜索
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

### 快速排序
```python
def quicksort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quicksort(arr, low, pi - 1)
        quicksort(arr, pi + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

### 回溯模板
```python
def backtrack(path, choices):
    if 满足结束条件:
        result.append(path[:])
        return
    
    for choice in choices:
        # 做选择
        path.append(choice)
        
        # 进入下一层
        backtrack(path, new_choices)
        
        # 撤销选择
        path.pop()
```

## 🏆 最后冲刺清单

### 必刷题目 (15道)
1. ✅ Two Sum
2. ✅ 3Sum  
3. ✅ Container With Most Water
4. ✅ Valid Parentheses
5. ✅ Merge Two Sorted Lists
6. ✅ Reverse Linked List
7. ✅ Maximum Depth of Binary Tree
8. ✅ Validate Binary Search Tree
9. ✅ Climbing Stairs
10. ✅ Coin Change
11. ✅ Number of Islands
12. ✅ Course Schedule
13. ✅ Kth Largest Element
14. 🔲 Merge Intervals
15. 🔲 Word Break

### 系统设计准备
- 缓存策略 (LRU, LFU)
- 数据库设计 (索引, 分片)
- 分布式系统 (一致性, 可用性)
- 消息队列 (Kafka, RabbitMQ)

### 行为问题准备
- 项目经历描述 (STAR方法)
- 技术挑战和解决方案
- 团队合作经验
- 学习能力展示

**记住：Practice makes perfect! 🌟**
