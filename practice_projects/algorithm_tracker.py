"""
外企面试算法学习进度跟踪器
Progress Tracker for Foreign Company Interview Preparation
"""

import json
import datetime
from typing import Dict, List, Any
from pathlib import Path


class AlgorithmTracker:
    """算法学习进度跟踪器"""
    
    def __init__(self, data_file: str = "progress.json"):
        self.data_file = Path(data_file)
        self.progress_data = self.load_progress()
        
        # 外企高频算法题分类
        self.algorithm_categories = {
            "数组和字符串": [
                "Two Sum", "3Sum", "Container With Most Water",
                "Longest Substring Without Repeating", "Group Anagrams",
                "Valid Anagram", "Merge Intervals", "Product of Array Except Self"
            ],
            "链表": [
                "Reverse Linked List", "Merge Two Sorted Lists",
                "Linked List Cycle", "Remove Nth Node From End",
                "Add Two Numbers", "Copy List with Random Pointer"
            ],
            "栈和队列": [
                "Valid Parentheses", "Daily Temperatures",
                "Min Stack", "Evaluate RPN", "Sliding Window Maximum"
            ],
            "树和图": [
                "Inorder Traversal", "Level Order Traversal",
                "Validate Binary Search Tree", "Maximum Depth",
                "Lowest Common Ancestor", "Number of Islands",
                "Course Schedule", "Clone Graph"
            ],
            "动态规划": [
                "Climbing Stairs", "House Robber", "Coin Change",
                "Longest Increasing Subsequence", "Edit Distance",
                "Maximum Subarray", "Unique Paths"
            ],
            "排序和搜索": [
                "Binary Search", "Search in Rotated Sorted Array",
                "Find First and Last Position", "Merge Sort",
                "Quick Sort", "Kth Largest Element"
            ],
            "双指针和滑动窗口": [
                "Two Pointers", "Sliding Window Maximum",
                "Minimum Window Substring", "Longest Palindromic Substring"
            ]
        }
        
        # 难度等级
        self.difficulty_levels = {
            "Easy": ["Two Sum", "Valid Parentheses", "Merge Two Sorted Lists", 
                    "Maximum Depth", "Climbing Stairs"],
            "Medium": ["3Sum", "Container With Most Water", "Add Two Numbers",
                      "Coin Change", "Course Schedule", "Daily Temperatures"],
            "Hard": ["Merge k Sorted Lists", "Trapping Rain Water",
                    "Edit Distance", "Word Ladder", "Minimum Window Substring"]
        }
    
    def load_progress(self) -> Dict[str, Any]:
        """加载学习进度"""
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "start_date": str(datetime.date.today()),
                "completed_problems": {},
                "study_sessions": [],
                "weekly_goals": {},
                "notes": {}
            }
    
    def save_progress(self):
        """保存学习进度"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress_data, f, indent=2, ensure_ascii=False)
    
    def mark_completed(self, problem_name: str, difficulty: str, 
                      time_taken: int, notes: str = ""):
        """标记题目完成"""
        today = str(datetime.date.today())
        
        self.progress_data["completed_problems"][problem_name] = {
            "difficulty": difficulty,
            "completed_date": today,
            "time_taken_minutes": time_taken,
            "notes": notes,
            "review_dates": []
        }
        
        # 添加到学习记录
        self.progress_data["study_sessions"].append({
            "date": today,
            "problem": problem_name,
            "time_spent": time_taken,
            "type": "first_solve"
        })
        
        self.save_progress()
        print(f"✅ 已完成: {problem_name} ({difficulty}) - 用时 {time_taken} 分钟")
    
    def add_review(self, problem_name: str, time_taken: int, notes: str = ""):
        """添加复习记录"""
        today = str(datetime.date.today())
        
        if problem_name in self.progress_data["completed_problems"]:
            self.progress_data["completed_problems"][problem_name]["review_dates"].append({
                "date": today,
                "time_taken": time_taken,
                "notes": notes
            })
            
            self.progress_data["study_sessions"].append({
                "date": today,
                "problem": problem_name,
                "time_spent": time_taken,
                "type": "review"
            })
            
            self.save_progress()
            print(f"📝 已复习: {problem_name} - 用时 {time_taken} 分钟")
        else:
            print(f"❌ 题目 {problem_name} 尚未完成首次解题")
    
    def set_weekly_goal(self, week_start: str, goal_problems: int):
        """设置周学习目标"""
        self.progress_data["weekly_goals"][week_start] = {
            "target_problems": goal_problems,
            "completed_problems": 0
        }
        self.save_progress()
        print(f"🎯 设置周目标: {week_start} 周完成 {goal_problems} 道题")
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """获取学习进度总结"""
        completed = self.progress_data["completed_problems"]
        total_problems = sum(len(problems) for problems in self.algorithm_categories.values())
        
        # 按分类统计
        category_progress = {}
        for category, problems in self.algorithm_categories.items():
            completed_in_category = sum(1 for p in problems if p in completed)
            category_progress[category] = {
                "completed": completed_in_category,
                "total": len(problems),
                "percentage": round(completed_in_category / len(problems) * 100, 1)
            }
        
        # 按难度统计
        difficulty_progress = {}
        for difficulty, problems in self.difficulty_levels.items():
            completed_in_difficulty = sum(1 for p in problems if p in completed)
            difficulty_progress[difficulty] = {
                "completed": completed_in_difficulty,
                "total": len(problems),
                "percentage": round(completed_in_difficulty / len(problems) * 100, 1)
            }
        
        # 最近一周的学习情况
        today = datetime.date.today()
        week_ago = today - datetime.timedelta(days=7)
        recent_sessions = [
            s for s in self.progress_data["study_sessions"]
            if datetime.datetime.strptime(s["date"], "%Y-%m-%d").date() >= week_ago
        ]
        
        return {
            "总体进度": {
                "已完成": len(completed),
                "总计": total_problems,
                "完成率": round(len(completed) / total_problems * 100, 1)
            },
            "分类进度": category_progress,
            "难度进度": difficulty_progress,
            "本周学习": {
                "学习天数": len(set(s["date"] for s in recent_sessions)),
                "解题数量": len([s for s in recent_sessions if s["type"] == "first_solve"]),
                "复习数量": len([s for s in recent_sessions if s["type"] == "review"]),
                "总时间": sum(s["time_spent"] for s in recent_sessions)
            }
        }
    
    def get_recommendations(self) -> List[str]:
        """获取学习建议"""
        completed = set(self.progress_data["completed_problems"].keys())
        recommendations = []
        
        # 检查每个分类的进度
        for category, problems in self.algorithm_categories.items():
            completed_in_category = [p for p in problems if p in completed]
            if len(completed_in_category) < len(problems) * 0.5:
                uncompleted = [p for p in problems if p not in completed]
                recommendations.append(
                    f"📚 重点关注 {category}: 还有 {len(uncompleted)} 道题未完成"
                )
        
        # 复习建议
        need_review = []
        today = datetime.date.today()
        for problem, data in self.progress_data["completed_problems"].items():
            completed_date = datetime.datetime.strptime(data["completed_date"], "%Y-%m-%d").date()
            days_since = (today - completed_date).days
            
            last_review = None
            if data["review_dates"]:
                last_review_date = max(data["review_dates"], key=lambda x: x["date"])["date"]
                last_review = datetime.datetime.strptime(last_review_date, "%Y-%m-%d").date()
                days_since = (today - last_review).days
            
            # 复习策略：1天后、3天后、1周后、2周后、1个月后
            if days_since in [1, 3, 7, 14, 30]:
                need_review.append(problem)
        
        if need_review:
            recommendations.append(f"🔄 建议复习: {', '.join(need_review[:3])}")
        
        return recommendations
    
    def display_dashboard(self):
        """显示学习仪表板"""
        summary = self.get_progress_summary()
        recommendations = self.get_recommendations()
        
        print("🚀 外企面试算法学习仪表板")
        print("=" * 60)
        
        # 总体进度
        total = summary["总体进度"]
        print(f"\n📊 总体进度: {total['已完成']}/{total['总计']} ({total['完成率']}%)")
        
        # 进度条
        progress_bar_length = 30
        filled_length = int(progress_bar_length * total['已完成'] / total['总计'])
        bar = '█' * filled_length + '░' * (progress_bar_length - filled_length)
        print(f"[{bar}] {total['完成率']}%")
        
        # 分类进度
        print(f"\n📚 分类进度:")
        for category, progress in summary["分类进度"].items():
            print(f"  {category}: {progress['completed']}/{progress['total']} ({progress['percentage']}%)")
        
        # 难度进度
        print(f"\n⭐ 难度进度:")
        for difficulty, progress in summary["难度进度"].items():
            print(f"  {difficulty}: {progress['completed']}/{progress['total']} ({progress['percentage']}%)")
        
        # 本周学习情况
        week = summary["本周学习"]
        print(f"\n📅 本周学习:")
        print(f"  学习天数: {week['学习天数']} 天")
        print(f"  新题目: {week['解题数量']} 道")
        print(f"  复习: {week['复习数量']} 道")
        print(f"  总时间: {week['总时间']} 分钟")
        
        # 学习建议
        if recommendations:
            print(f"\n💡 学习建议:")
            for rec in recommendations:
                print(f"  {rec}")
        
        print(f"\n🎯 继续加油，向外企offer冲刺！")


def demo_usage():
    """演示用法"""
    print("🎮 算法学习进度跟踪器演示")
    print("=" * 50)
    
    tracker = AlgorithmTracker()
    
    # 模拟学习记录
    tracker.mark_completed("Two Sum", "Easy", 15, "使用哈希表，一次遍历解决")
    tracker.mark_completed("3Sum", "Medium", 45, "排序+双指针，注意去重")
    tracker.mark_completed("Valid Parentheses", "Easy", 20, "栈的经典应用")
    
    # 设置周目标
    today = datetime.date.today()
    week_start = (today - datetime.timedelta(days=today.weekday())).strftime("%Y-%m-%d")
    tracker.set_weekly_goal(week_start, 5)
    
    # 添加复习记录
    tracker.add_review("Two Sum", 8, "复习很快，已熟练掌握")
    
    # 显示仪表板
    print("\n")
    tracker.display_dashboard()
    
    return tracker


if __name__ == "__main__":
    # 运行演示
    tracker = demo_usage()
    
    print(f"\n📝 使用说明:")
    print(f"1. tracker.mark_completed('题目名', '难度', 用时分钟, '笔记')")
    print(f"2. tracker.add_review('题目名', 用时分钟, '复习笔记')")
    print(f"3. tracker.set_weekly_goal('周开始日期', 目标题数)")
    print(f"4. tracker.display_dashboard()  # 查看进度")
    print(f"5. 进度自动保存到 progress.json 文件")
