"""
LeetCode 经典题目解析与Python实现
专为外企面试准备的算法题库
"""

# ====================== 1. 数组与字符串 ======================

def two_sum(nums, target):
    """
    Two Sum (Easy) - 最经典的入门题
    给定一个整数数组 nums 和一个目标值 target，
    请你在该数组中找出和为目标值的那两个整数，并返回他们的数组下标。
    
    Time: O(n), Space: O(n)
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []


def three_sum(nums):
    """
    3Sum (Medium) - 三数之和
    给你一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c，
    使得 a + b + c = 0？请找出所有满足条件且不重复的三元组。
    
    Time: O(n²), Space: O(1)
    """
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # 跳过重复元素
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        
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


def length_of_longest_substring(s):
    """
    Longest Substring Without Repeating Characters (Medium)
    给定一个字符串，请你找出其中不含有重复字符的最长子串的长度。
    
    滑动窗口算法
    Time: O(n), Space: O(min(m, n))
    """
    char_map = {}
    left = 0
    max_length = 0
    
    for right, char in enumerate(s):
        if char in char_map and char_map[char] >= left:
            left = char_map[char] + 1
        
        char_map[char] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length


def max_area(height):
    """
    盛最多水的容器 (Medium)
    给你 n 个非负整数，每个数代表坐标中的一个点。
    找出其中的两条线，使得它们与 x 轴共同构成的容器能够容纳最多的水。
    
    双指针算法
    Time: O(n), Space: O(1)
    """
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        # 计算当前容量
        width = right - left
        current_water = min(height[left], height[right]) * width
        max_water = max(max_water, current_water)
        
        # 移动较短的指针
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_water


# ====================== 2. 链表操作 ======================

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def __repr__(self):
        result = []
        current = self
        while current:
            result.append(str(current.val))
            current = current.next
        return " -> ".join(result)


def reverse_list(head):
    """
    反转链表 (Easy)
    反转一个单链表
    
    Time: O(n), Space: O(1)
    """
    prev = None
    current = head
    
    while current:
        next_temp = current.next
        current.next = prev
        prev = current
        current = next_temp
    
    return prev


def reverse_list_recursive(head):
    """反转链表的递归解法"""
    if not head or not head.next:
        return head
    
    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    
    return new_head


def merge_two_lists(l1, l2):
    """
    合并两个有序链表 (Easy)
    将两个升序链表合并为一个新的升序链表并返回
    
    Time: O(n + m), Space: O(1)
    """
    dummy = ListNode()
    current = dummy
    
    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next
    
    # 连接剩余部分
    current.next = l1 or l2
    
    return dummy.next


def has_cycle(head):
    """
    环形链表 (Easy)
    给定一个链表，判断链表中是否有环
    
    Floyd判圈算法（快慢指针）
    Time: O(n), Space: O(1)
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


def detect_cycle(head):
    """
    环形链表 II (Medium)
    返回链表开始入环的第一个节点
    """
    if not head or not head.next:
        return None
    
    # 第一步：检测是否有环
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # 无环
    
    # 第二步：找到环的起始点
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow


# ====================== 3. 树的遍历 ======================

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def inorder_traversal(root):
    """
    中序遍历：左 -> 根 -> 右
    """
    result = []
    
    def dfs(node):
        if node:
            dfs(node.left)
            result.append(node.val)
            dfs(node.right)
    
    dfs(root)
    return result


def inorder_iterative(root):
    """中序遍历的迭代实现"""
    result = []
    stack = []
    current = root
    
    while stack or current:
        # 走到最左边
        while current:
            stack.append(current)
            current = current.left
        
        # 处理当前节点
        current = stack.pop()
        result.append(current.val)
        
        # 转向右子树
        current = current.right
    
    return result


def level_order_traversal(root):
    """层序遍历（BFS）"""
    if not root:
        return []
    
    from collections import deque
    
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


def is_valid_bst(root):
    """
    验证二叉搜索树 (Medium)
    给定一个二叉树，判断其是否是一个有效的二叉搜索树
    
    Time: O(n), Space: O(n)
    """
    def validate(node, min_val, max_val):
        if not node:
            return True
        
        if node.val <= min_val or node.val >= max_val:
            return False
        
        return (validate(node.left, min_val, node.val) and 
                validate(node.right, node.val, max_val))
    
    return validate(root, float('-inf'), float('inf'))


# ====================== 4. 动态规划 ======================

def climb_stairs(n):
    """
    爬楼梯 (Easy)
    假设你正在爬楼梯。需要 n 阶你才能到达楼顶。
    每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？
    
    Time: O(n), Space: O(1)
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


def max_subarray(nums):
    """
    最大子序和 (Easy)
    给定一个整数数组 nums，找到一个具有最大和的连续子数组
    （子数组最少包含一个元素），返回其最大和。
    
    Kadane算法
    Time: O(n), Space: O(1)
    """
    max_ending_here = max_so_far = nums[0]
    
    for i in range(1, len(nums)):
        max_ending_here = max(nums[i], max_ending_here + nums[i])
        max_so_far = max(max_so_far, max_ending_here)
    
    return max_so_far


def max_profit(prices):
    """
    买卖股票的最佳时机 (Easy)
    给定一个数组，它的第 i 个元素是一支给定股票第 i 天的价格。
    如果你最多只允许完成一笔交易，设计一个算法来计算你所能获取的最大利润。
    
    Time: O(n), Space: O(1)
    """
    if not prices:
        return 0
    
    min_price = prices[0]
    max_profit = 0
    
    for price in prices[1:]:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    
    return max_profit


def longest_palindrome(s):
    """
    最长回文子串 (Medium)
    给定一个字符串 s，找到 s 中最长的回文子串。
    
    中心扩展算法
    Time: O(n²), Space: O(1)
    """
    if not s:
        return ""
    
    start = 0
    max_len = 1
    
    def expand_around_center(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1
    
    for i in range(len(s)):
        # 奇数长度回文串
        len1 = expand_around_center(i, i)
        # 偶数长度回文串
        len2 = expand_around_center(i, i + 1)
        
        current_max = max(len1, len2)
        if current_max > max_len:
            max_len = current_max
            start = i - (current_max - 1) // 2
    
    return s[start:start + max_len]


# ====================== 5. 字符串处理 ======================

def is_valid(s):
    """
    有效的括号 (Easy)
    给定一个只包括 '(',')','{','}','[',']' 的字符串，判断字符串是否有效。
    
    Time: O(n), Space: O(n)
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


def my_atoi(s):
    """
    字符串转换整数 (Medium)
    实现 atoi 函数，将字符串转换为整数。
    
    Time: O(n), Space: O(1)
    """
    if not s:
        return 0
    
    # 去除前导空格
    s = s.lstrip()
    if not s:
        return 0
    
    # 检查符号
    sign = 1
    i = 0
    if s[0] in ['+', '-']:
        sign = -1 if s[0] == '-' else 1
        i = 1
    
    # 转换数字
    result = 0
    INT_MAX = 2**31 - 1
    INT_MIN = -2**31
    
    while i < len(s) and s[i].isdigit():
        digit = int(s[i])
        
        # 检查溢出
        if result > (INT_MAX - digit) // 10:
            return INT_MAX if sign == 1 else INT_MIN
        
        result = result * 10 + digit
        i += 1
    
    return result * sign


# ====================== 6. 测试用例 ======================

def test_algorithms():
    """测试所有算法"""
    print("=== 测试开始 ===")
    
    # 测试 Two Sum
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    print("✓ Two Sum 测试通过")
    
    # 测试 3Sum
    result = three_sum([-1, 0, 1, 2, -1, -4])
    print(f"✓ 3Sum 结果: {result}")
    
    # 测试最长无重复字符子串
    assert length_of_longest_substring("abcabcbb") == 3
    assert length_of_longest_substring("pwwkew") == 3
    print("✓ 最长无重复字符子串测试通过")
    
    # 测试盛水容器
    assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    print("✓ 盛水容器测试通过")
    
    # 测试爬楼梯
    assert climb_stairs(3) == 3
    assert climb_stairs(4) == 5
    print("✓ 爬楼梯测试通过")
    
    # 测试最大子序和
    assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    print("✓ 最大子序和测试通过")
    
    # 测试买卖股票
    assert max_profit([7, 1, 5, 3, 6, 4]) == 5
    print("✓ 买卖股票测试通过")
    
    # 测试有效括号
    assert is_valid("()") == True
    assert is_valid("()[]{}") == True
    assert is_valid("(]") == False
    print("✓ 有效括号测试通过")
    
    # 测试最长回文子串
    assert longest_palindrome("babad") in ["bab", "aba"]
    print("✓ 最长回文子串测试通过")
    
    print("=== 所有测试通过！===")


if __name__ == "__main__":
    test_algorithms()
