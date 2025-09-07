"""
LeetCode高频面试题精选 - 外企算法面试专用
按难度和类型分类的经典题目解析
"""

from typing import List, Optional
from collections import defaultdict, deque, Counter
import heapq


# ====================== 数组和字符串 ======================

def two_sum(nums: List[int], target: int) -> List[int]:
    """
    1. Two Sum (Easy)
    给定一个整数数组 nums 和一个目标值 target，
    请你在该数组中找出和为目标值的那两个整数，并返回他们的数组下标。
    
    时间复杂度: O(n)
    空间复杂度: O(n)
    """
    num_to_index = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_to_index:
            return [num_to_index[complement], i]
        num_to_index[num] = i
    
    return []


def three_sum(nums: List[int]) -> List[List[int]]:
    """
    15. 3Sum (Medium)
    给你一个包含 n 个整数的数组 nums，
    判断 nums 中是否存在三个元素 a，b，c 使得 a + b + c = 0
    
    时间复杂度: O(n²)
    空间复杂度: O(1)
    """
    nums.sort()
    result = []
    n = len(nums)
    
    for i in range(n - 2):
        # 跳过重复元素
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        left, right = i + 1, n - 1
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            
            if current_sum == 0:
                result.append([nums[i], nums[left], nums[right]])
                
                # 跳过重复元素
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < 0:
                left += 1
            else:
                right -= 1
    
    return result


def container_with_most_water(height: List[int]) -> int:
    """
    11. Container With Most Water (Medium)
    给你 n 个非负整数，每个数代表坐标中的一个点
    找出其中的两条线，使得它们与 x 轴共同构成的容器能够容纳最多的水
    
    时间复杂度: O(n)
    空间复杂度: O(1)
    """
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        # 计算当前面积
        width = right - left
        current_area = min(height[left], height[right]) * width
        max_area = max(max_area, current_area)
        
        # 移动较短的指针
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_area


def longest_substring_without_repeating(s: str) -> int:
    """
    3. Longest Substring Without Repeating Characters (Medium)
    给定一个字符串，请你找出其中不含有重复字符的最长子串的长度
    
    时间复杂度: O(n)
    空间复杂度: O(min(m,n))
    """
    char_index = {}
    max_length = 0
    start = 0
    
    for end, char in enumerate(s):
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1
        
        char_index[char] = end
        max_length = max(max_length, end - start + 1)
    
    return max_length


def group_anagrams(strs: List[str]) -> List[List[str]]:
    """
    49. Group Anagrams (Medium)
    给你一个字符串数组，请你将字母异位词组合在一起
    
    时间复杂度: O(N * K * log K) 其中 N 是strs的长度，K是字符串的最大长度
    空间复杂度: O(N * K)
    """
    groups = defaultdict(list)
    
    for s in strs:
        # 将字符串排序作为key
        key = ''.join(sorted(s))
        groups[key].append(s)
    
    return list(groups.values())


def valid_anagram(s: str, t: str) -> bool:
    """
    242. Valid Anagram (Easy)
    给定两个字符串 s 和 t ，编写一个函数来判断 t 是否是 s 的字母异位词
    
    时间复杂度: O(n)
    空间复杂度: O(1)
    """
    if len(s) != len(t):
        return False
    
    return Counter(s) == Counter(t)


# ====================== 链表 ======================

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def __repr__(self):
        """便于调试的字符串表示"""
        result = []
        current = self
        visited = set()
        
        while current and id(current) not in visited:
            visited.add(id(current))
            result.append(str(current.val))
            current = current.next
            
            if len(result) > 10:  # 防止无限循环
                result.append("...")
                break
        
        return " -> ".join(result)


def reverse_linked_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    206. Reverse Linked List (Easy)
    反转一个单链表
    
    时间复杂度: O(n)
    空间复杂度: O(1)
    """
    prev = None
    current = head
    
    while current:
        next_temp = current.next
        current.next = prev
        prev = current
        current = next_temp
    
    return prev


def merge_two_sorted_lists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
    """
    21. Merge Two Sorted Lists (Easy)
    将两个升序链表合并为一个新的升序链表并返回
    
    时间复杂度: O(n + m)
    空间复杂度: O(1)
    """
    dummy = ListNode()
    current = dummy
    
    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next
    
    # 连接剩余部分
    current.next = list1 or list2
    
    return dummy.next


def has_cycle(head: Optional[ListNode]) -> bool:
    """
    141. Linked List Cycle (Easy)
    给定一个链表，判断链表中是否有环
    
    Floyd判圈算法（快慢指针）
    时间复杂度: O(n)
    空间复杂度: O(1)
    """
    if not head or not head.next:
        return False
    
    slow = head
    fast = head.next
    
    while fast and fast.next:
        if slow == fast:
            return True
        slow = slow.next
        fast = fast.next.next
    
    return False


def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """
    19. Remove Nth Node From End of List (Medium)
    给你一个链表，删除链表的倒数第 n 个结点，并且返回链表的头结点
    
    时间复杂度: O(L) L是链表长度
    空间复杂度: O(1)
    """
    dummy = ListNode(0)
    dummy.next = head
    
    # 双指针，先让fast指针走n步
    slow = fast = dummy
    
    for _ in range(n + 1):
        fast = fast.next
    
    # 然后两个指针一起走，直到fast到达末尾
    while fast:
        slow = slow.next
        fast = fast.next
    
    # 删除slow的下一个节点
    slow.next = slow.next.next
    
    return dummy.next


# ====================== 栈和队列 ======================

def valid_parentheses(s: str) -> bool:
    """
    20. Valid Parentheses (Easy)
    给定一个只包括 '(',')','{','}','[',']' 的字符串，判断字符串是否有效
    
    时间复杂度: O(n)
    空间复杂度: O(n)
    """
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            # 右括号
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            # 左括号
            stack.append(char)
    
    return not stack


def daily_temperatures(temperatures: List[int]) -> List[int]:
    """
    739. Daily Temperatures (Medium)
    根据每日气温列表，请重新生成一个列表，
    对应位置的输出是需要再等待多少天温度才会升高超过该日的温度
    
    时间复杂度: O(n)
    空间复杂度: O(n)
    """
    result = [0] * len(temperatures)
    stack = []  # 存储索引
    
    for i, temp in enumerate(temperatures):
        # 当前温度比栈顶索引对应的温度高
        while stack and temperatures[stack[-1]] < temp:
            prev_index = stack.pop()
            result[prev_index] = i - prev_index
        
        stack.append(i)
    
    return result


# ====================== 树 ======================

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def inorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """
    94. Binary Tree Inorder Traversal (Easy)
    中序遍历：左 -> 根 -> 右
    
    时间复杂度: O(n)
    空间复杂度: O(n)
    """
    result = []
    
    def inorder(node):
        if node:
            inorder(node.left)
            result.append(node.val)
            inorder(node.right)
    
    inorder(root)
    return result


def level_order_traversal(root: Optional[TreeNode]) -> List[List[int]]:
    """
    102. Binary Tree Level Order Traversal (Medium)
    给你一个二叉树，请你返回其按层序遍历得到的节点值
    
    时间复杂度: O(n)
    空间复杂度: O(n)
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level_values = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level_values.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level_values)
    
    return result


def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """
    98. Validate Binary Search Tree (Medium)
    给定一个二叉树，判断其是否是一个有效的二叉搜索树
    
    时间复杂度: O(n)
    空间复杂度: O(n)
    """
    def validate(node, min_val, max_val):
        if not node:
            return True
        
        if node.val <= min_val or node.val >= max_val:
            return False
        
        return (validate(node.left, min_val, node.val) and 
                validate(node.right, node.val, max_val))
    
    return validate(root, float('-inf'), float('inf'))


def max_depth(root: Optional[TreeNode]) -> int:
    """
    104. Maximum Depth of Binary Tree (Easy)
    给定一个二叉树，找出其最大深度
    
    时间复杂度: O(n)
    空间复杂度: O(n)
    """
    if not root:
        return 0
    
    return 1 + max(max_depth(root.left), max_depth(root.right))


def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    236. Lowest Common Ancestor of a Binary Tree (Medium)
    给定一个二叉树, 找到该树中两个指定节点的最近公共祖先
    
    时间复杂度: O(n)
    空间复杂度: O(n)
    """
    if not root or root == p or root == q:
        return root
    
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    
    if left and right:
        return root
    
    return left or right


# ====================== 动态规划 ======================

def climbing_stairs(n: int) -> int:
    """
    70. Climbing Stairs (Easy)
    假设你正在爬楼梯。需要 n 阶你才能到达楼顶。
    每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？
    
    时间复杂度: O(n)
    空间复杂度: O(1)
    """
    if n <= 2:
        return n
    
    prev2 = 1  # f(1)
    prev1 = 2  # f(2)
    
    for i in range(3, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    
    return prev1


def house_robber(nums: List[int]) -> int:
    """
    198. House Robber (Medium)
    你是一个专业的小偷，沿着街道有一排房屋，每间房内都藏有一定的现金。
    相邻的房屋不能同时被偷窃。
    
    时间复杂度: O(n)
    空间复杂度: O(1)
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    
    prev2 = nums[0]
    prev1 = max(nums[0], nums[1])
    
    for i in range(2, len(nums)):
        current = max(prev1, prev2 + nums[i])
        prev2 = prev1
        prev1 = current
    
    return prev1


def coin_change(coins: List[int], amount: int) -> int:
    """
    322. Coin Change (Medium)
    给你一个整数数组 coins，表示不同面额的硬币；
    以及一个整数 amount，表示总金额。
    计算并返回可以凑成总金额所需的最少的硬币个数。
    
    时间复杂度: O(amount * len(coins))
    空间复杂度: O(amount)
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1


def longest_increasing_subsequence(nums: List[int]) -> int:
    """
    300. Longest Increasing Subsequence (Medium)
    给你一个整数数组 nums，找到其中最长严格递增子序列的长度。
    
    时间复杂度: O(n log n)
    空间复杂度: O(n)
    """
    if not nums:
        return 0
    
    # tails[i] 存储长度为 i+1 的递增子序列的最小尾部元素
    tails = []
    
    for num in nums:
        # 二分查找插入位置
        left, right = 0, len(tails)
        while left < right:
            mid = (left + right) // 2
            if tails[mid] < num:
                left = mid + 1
            else:
                right = mid
        
        # 如果需要扩展数组
        if left == len(tails):
            tails.append(num)
        else:
            tails[left] = num
    
    return len(tails)


# ====================== 图论和搜索 ======================

def number_of_islands(grid: List[List[str]]) -> int:
    """
    200. Number of Islands (Medium)
    给你一个由 '1'（陆地）和 '0'（水）组成的的二维网格，请你计算网格中岛屿的数量。
    
    时间复杂度: O(m * n)
    空间复杂度: O(m * n)
    """
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    islands = 0
    
    def dfs(r, c):
        if (r < 0 or r >= rows or c < 0 or c >= cols or 
            grid[r][c] != '1'):
            return
        
        grid[r][c] = '0'  # 标记为已访问
        
        # 访问四个方向
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc)
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                islands += 1
                dfs(r, c)
    
    return islands


def course_schedule(numCourses: int, prerequisites: List[List[int]]) -> bool:
    """
    207. Course Schedule (Medium)
    你这个学期必须选修 numCourses 门课程，记为 0 到 numCourses - 1。
    在选修某些课程之前需要一些先修课程。
    
    拓扑排序解决环检测问题
    时间复杂度: O(V + E)
    空间复杂度: O(V + E)
    """
    # 构建图和入度数组
    graph = defaultdict(list)
    in_degree = [0] * numCourses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    # BFS拓扑排序
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    taken = 0
    
    while queue:
        course = queue.popleft()
        taken += 1
        
        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    return taken == numCourses


# ====================== 堆和优先队列 ======================

def find_kth_largest(nums: List[int], k: int) -> int:
    """
    215. Kth Largest Element in an Array (Medium)
    找到数组中第k个最大的元素
    
    时间复杂度: O(n log k)
    空间复杂度: O(k)
    """
    # 使用最小堆，保持堆大小为k
    heap = []
    
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    
    return heap[0]


def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """
    347. Top K Frequent Elements (Medium)
    给你一个整数数组 nums 和一个整数 k，请你返回其中出现频率前 k 高的元素
    
    时间复杂度: O(n log k)
    空间复杂度: O(n + k)
    """
    count = Counter(nums)
    
    # 使用最小堆，存储 (频率, 数字) 对
    heap = []
    
    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)
    
    return [num for freq, num in heap]


# ====================== 测试用例 ======================

def run_tests():
    """运行所有测试用例"""
    print("🧪 LeetCode高频面试题测试")
    print("=" * 50)
    
    # 数组和字符串测试
    print("\n📊 数组和字符串测试:")
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    print("✅ Two Sum")
    
    assert three_sum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]
    print("✅ 3Sum")
    
    assert container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    print("✅ Container With Most Water")
    
    assert longest_substring_without_repeating("abcabcbb") == 3
    print("✅ Longest Substring Without Repeating Characters")
    
    # 链表测试
    print("\n🔗 链表测试:")
    # 创建测试链表: 1 -> 2 -> 3
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    
    reversed_head = reverse_linked_list(head)
    assert reversed_head.val == 3
    print("✅ Reverse Linked List")
    
    # 栈和队列测试
    print("\n📚 栈和队列测试:")
    assert valid_parentheses("()[]{}") == True
    assert valid_parentheses("([)]") == False
    print("✅ Valid Parentheses")
    
    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    print("✅ Daily Temperatures")
    
    # 动态规划测试
    print("\n🎯 动态规划测试:")
    assert climbing_stairs(3) == 3
    assert climbing_stairs(4) == 5
    print("✅ Climbing Stairs")
    
    assert house_robber([2, 7, 9, 3, 1]) == 12
    print("✅ House Robber")
    
    assert coin_change([1, 3, 4], 6) == 2
    print("✅ Coin Change")
    
    assert longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    print("✅ Longest Increasing Subsequence")
    
    # 图论测试
    print("\n🌐 图论测试:")
    grid = [
        ["1","1","1","1","0"],
        ["1","1","0","1","0"],
        ["1","1","0","0","0"],
        ["0","0","0","0","0"]
    ]
    assert number_of_islands(grid) == 1
    print("✅ Number of Islands")
    
    assert course_schedule(2, [[1, 0]]) == True
    assert course_schedule(2, [[1, 0], [0, 1]]) == False
    print("✅ Course Schedule")
    
    # 堆测试
    print("\n🏔️ 堆测试:")
    assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    print("✅ Kth Largest Element")
    
    result = top_k_frequent([1, 1, 1, 2, 2, 3], 2)
    assert set(result) == {1, 2}
    print("✅ Top K Frequent Elements")
    
    print("\n🎉 所有测试通过！")
    
    # 复杂度分析总结
    print("\n📈 复杂度分析总结:")
    complexities = [
        ("Two Sum", "O(n)", "O(n)"),
        ("3Sum", "O(n²)", "O(1)"),
        ("Valid BST", "O(n)", "O(n)"),
        ("Coin Change", "O(amount × coins)", "O(amount)"),
        ("Course Schedule", "O(V + E)", "O(V + E)"),
        ("Kth Largest", "O(n log k)", "O(k)")
    ]
    
    print(f"{'算法':<25} {'时间复杂度':<15} {'空间复杂度':<15}")
    print("-" * 55)
    for name, time_comp, space_comp in complexities:
        print(f"{name:<25} {time_comp:<15} {space_comp:<15}")


if __name__ == "__main__":
    run_tests()
