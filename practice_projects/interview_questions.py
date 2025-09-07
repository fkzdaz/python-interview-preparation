"""
Python面试题库 - 外企技术面试精选
涵盖基础到高级的所有重要面试题目
"""

import sys
import gc
import threading
import multiprocessing
import asyncio
from collections import defaultdict, Counter
import time


# ====================== 1. Python基础概念 ======================

def explain_python_features():
    """
    Q1: 解释Python的主要特性
    """
    features = {
        "解释型语言": "Python代码在运行时被逐行解释执行",
        "动态类型": "变量类型在运行时确定，不需要提前声明",
        "强类型": "不允许隐式类型转换，'1' + 1会报错",
        "面向对象": "支持类、继承、多态等面向对象特性",
        "跨平台": "一次编写，到处运行",
        "丰富的标准库": "内置大量模块和函数",
        "语法简洁": "接近自然语言，易读易写"
    }
    
    print("Python主要特性:")
    for feature, description in features.items():
        print(f"  • {feature}: {description}")


def mutable_vs_immutable():
    """
    Q2: 可变与不可变对象的区别
    """
    print("\n=== 可变 vs 不可变对象 ===")
    
    # 不可变对象 (immutable)
    print("不可变对象:")
    a = [1, 2, 3]
    b = a
    print(f"a = {a}, b = {b}, id相同: {id(a) == id(b)}")
    
    a.append(4)  # 修改列表
    print(f"修改后: a = {a}, b = {b}")
    print("结论: 列表是可变的，修改a也会影响b\n")
    
    # 不可变对象
    print("不可变对象:")
    x = "hello"
    y = x
    print(f"x = '{x}', y = '{y}', id相同: {id(x) == id(y)}")
    
    x += " world"  # 创建新字符串
    print(f"修改后: x = '{x}', y = '{y}', id相同: {id(x) == id(y)}")
    print("结论: 字符串是不可变的，修改x创建了新对象")
    
    return {
        "可变对象": ["list", "dict", "set", "自定义类实例"],
        "不可变对象": ["int", "float", "str", "tuple", "frozenset", "bool"]
    }


def explain_gil():
    """
    Q3: 解释Python的GIL（全局解释器锁）
    """
    print("\n=== GIL (Global Interpreter Lock) ===")
    
    print("GIL的特点:")
    print("1. 同一时刻只有一个线程可以执行Python字节码")
    print("2. 防止多线程同时修改对象导致的内存损坏")
    print("3. 简化了CPython的实现，但限制了真正的并行执行")
    
    # 演示GIL的影响
    def cpu_intensive_task():
        count = 0
        for i in range(1000000):
            count += i
        return count
    
    # 单线程执行
    start_time = time.time()
    result1 = cpu_intensive_task()
    single_thread_time = time.time() - start_time
    
    # 多线程执行
    start_time = time.time()
    threads = []
    for i in range(2):
        t = threading.Thread(target=cpu_intensive_task)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    multi_thread_time = time.time() - start_time
    
    print(f"\n单线程耗时: {single_thread_time:.4f}秒")
    print(f"双线程耗时: {multi_thread_time:.4f}秒")
    print("结论: 对于CPU密集型任务，多线程可能更慢")
    
    print("\n解决方案:")
    print("• CPU密集型: 使用multiprocessing")
    print("• I/O密集型: 使用threading或asyncio")
    print("• 其他Python实现: Jython, IronPython等没有GIL")


def memory_management():
    """
    Q4: Python内存管理机制
    """
    print("\n=== Python内存管理 ===")
    
    # 引用计数
    print("1. 引用计数:")
    a = [1, 2, 3]
    print(f"列表 {a} 的引用计数: {sys.getrefcount(a) - 1}")  # -1因为getrefcount也创建了引用
    
    b = a
    print(f"赋值给b后的引用计数: {sys.getrefcount(a) - 1}")
    
    del b
    print(f"删除b后的引用计数: {sys.getrefcount(a) - 1}")
    
    # 循环引用
    print("\n2. 循环引用问题:")
    class Node:
        def __init__(self, value):
            self.value = value
            self.ref = None
    
    node1 = Node(1)
    node2 = Node(2)
    node1.ref = node2
    node2.ref = node1  # 循环引用
    
    print("创建了循环引用，引用计数无法自动回收")
    
    # 垃圾回收
    print(f"垃圾回收前: {gc.get_count()}")
    collected = gc.collect()
    print(f"垃圾回收后: {gc.get_count()}, 回收了 {collected} 个对象")
    
    print("\n3. 内存池:")
    print("• 小整数池: -5到256的整数被缓存")
    print("• 字符串驻留: 短字符串和标识符被缓存")
    
    # 演示小整数池
    a = 100
    b = 100
    print(f"100 == 100: {a is b}")  # True
    
    a = 1000
    b = 1000
    print(f"1000 == 1000: {a is b}")  # 可能是False


# ====================== 2. 数据结构与算法 ======================

def list_vs_tuple_vs_set():
    """
    Q5: list、tuple、set的区别和使用场景
    """
    print("\n=== List vs Tuple vs Set ===")
    
    # 性能比较
    import timeit
    
    # 创建操作
    list_time = timeit.timeit('list(range(1000))', number=10000)
    tuple_time = timeit.timeit('tuple(range(1000))', number=10000)
    set_time = timeit.timeit('set(range(1000))', number=10000)
    
    print("创建1000个元素的性能对比:")
    print(f"List:  {list_time:.6f}秒")
    print(f"Tuple: {tuple_time:.6f}秒")
    print(f"Set:   {set_time:.6f}秒")
    
    # 查找操作
    data_list = list(range(10000))
    data_tuple = tuple(range(10000))
    data_set = set(range(10000))
    
    list_search = timeit.timeit(lambda: 9999 in data_list, number=1000)
    tuple_search = timeit.timeit(lambda: 9999 in data_tuple, number=1000)
    set_search = timeit.timeit(lambda: 9999 in data_set, number=1000)
    
    print("\n查找元素的性能对比:")
    print(f"List:  {list_search:.6f}秒")
    print(f"Tuple: {tuple_search:.6f}秒")
    print(f"Set:   {set_search:.6f}秒")
    
    print("\n使用场景:")
    print("List: 有序、可变、允许重复 - 适合存储序列数据")
    print("Tuple: 有序、不可变、允许重复 - 适合存储不变的记录")
    print("Set: 无序、可变、不允许重复 - 适合去重和集合运算")


def dict_implementation():
    """
    Q6: 字典的实现原理和时间复杂度
    """
    print("\n=== 字典实现原理 ===")
    
    print("1. 哈希表实现:")
    print("• 使用开放寻址法解决哈希冲突")
    print("• Python 3.7+保持插入顺序")
    print("• 动态扩容，负载因子约2/3")
    
    print("\n2. 时间复杂度:")
    operations = {
        "访问/查找": "O(1) 平均情况",
        "插入": "O(1) 平均情况",
        "删除": "O(1) 平均情况",
        "遍历": "O(n)"
    }
    
    for op, complexity in operations.items():
        print(f"• {op}: {complexity}")
    
    # 演示哈希冲突
    print("\n3. 哈希冲突演示:")
    
    class BadHash:
        def __init__(self, value):
            self.value = value
        
        def __hash__(self):
            return 1  # 故意返回相同的哈希值
        
        def __eq__(self, other):
            return isinstance(other, BadHash) and self.value == other.value
    
    bad_dict = {}
    start_time = time.time()
    
    for i in range(1000):
        bad_dict[BadHash(i)] = i
    
    bad_time = time.time() - start_time
    
    # 正常字典
    normal_dict = {}
    start_time = time.time()
    
    for i in range(1000):
        normal_dict[i] = i
    
    normal_time = time.time() - start_time
    
    print(f"哈希冲突字典插入时间: {bad_time:.6f}秒")
    print(f"正常字典插入时间: {normal_time:.6f}秒")
    print(f"性能差异: {bad_time / normal_time:.2f}倍")


# ====================== 3. 函数和作用域 ======================

def closure_example():
    """
    Q7: 解释闭包和作用域
    """
    print("\n=== 闭包和作用域 ===")
    
    # 经典的闭包陷阱
    print("1. 经典的闭包陷阱:")
    functions = []
    
    for i in range(5):
        functions.append(lambda: i)  # 错误的方式
    
    print("错误的闭包结果:")
    for f in functions:
        print(f(), end=" ")
    print()
    
    # 正确的闭包
    print("\n2. 正确的闭包:")
    functions = []
    
    for i in range(5):
        functions.append(lambda x=i: x)  # 使用默认参数
    
    print("正确的闭包结果:")
    for f in functions:
        print(f(), end=" ")
    print()
    
    # 另一种正确方式
    functions = []
    
    for i in range(5):
        functions.append((lambda i: lambda: i)(i))  # 立即执行函数
    
    print("另一种正确方式:")
    for f in functions:
        print(f(), end=" ")
    print()
    
    # 闭包的应用
    print("\n3. 闭包的实际应用:")
    
    def make_multiplier(factor):
        def multiply(number):
            return number * factor
        return multiply
    
    double = make_multiplier(2)
    triple = make_multiplier(3)
    
    print(f"double(5) = {double(5)}")
    print(f"triple(5) = {triple(5)}")
    
    # 检查闭包变量
    print(f"double的闭包变量: {double.__closure__[0].cell_contents}")


def decorator_deep_dive():
    """
    Q8: 装饰器的实现原理和高级用法
    """
    print("\n=== 装饰器深入理解 ===")
    
    # 基本装饰器
    def simple_decorator(func):
        def wrapper(*args, **kwargs):
            print(f"调用函数: {func.__name__}")
            result = func(*args, **kwargs)
            print(f"函数返回: {result}")
            return result
        return wrapper
    
    # 带参数的装饰器
    def repeat(times):
        def decorator(func):
            def wrapper(*args, **kwargs):
                results = []
                for _ in range(times):
                    result = func(*args, **kwargs)
                    results.append(result)
                return results
            return wrapper
        return decorator
    
    # 类装饰器
    class CountCalls:
        def __init__(self, func):
            self.func = func
            self.count = 0
        
        def __call__(self, *args, **kwargs):
            self.count += 1
            print(f"第 {self.count} 次调用 {self.func.__name__}")
            return self.func(*args, **kwargs)
    
    # 使用装饰器
    @simple_decorator
    def greet(name):
        return f"Hello, {name}!"
    
    @repeat(3)
    def get_random():
        import random
        return random.randint(1, 10)
    
    @CountCalls
    def say_hello():
        return "Hello!"
    
    print("1. 基本装饰器:")
    result = greet("Alice")
    
    print("\n2. 带参数的装饰器:")
    results = get_random()
    print(f"随机数结果: {results}")
    
    print("\n3. 类装饰器:")
    say_hello()
    say_hello()
    print(f"总调用次数: {say_hello.count}")


# ====================== 4. 并发编程 ======================

def threading_vs_multiprocessing():
    """
    Q9: threading、multiprocessing、asyncio的区别
    """
    print("\n=== 并发编程比较 ===")
    
    # CPU密集型任务
    def cpu_task(n):
        return sum(i * i for i in range(n))
    
    # I/O密集型任务模拟
    def io_task():
        time.sleep(0.1)
        return "I/O完成"
    
    # Threading测试
    print("1. Threading (适合I/O密集型):")
    start_time = time.time()
    
    threads = []
    for i in range(5):
        t = threading.Thread(target=io_task)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    threading_time = time.time() - start_time
    print(f"Threading完成5个I/O任务耗时: {threading_time:.4f}秒")
    
    # Multiprocessing测试
    print("\n2. Multiprocessing (适合CPU密集型):")
    
    if __name__ == '__main__':  # 避免在import时执行
        try:
            start_time = time.time()
            
            with multiprocessing.Pool(processes=2) as pool:
                results = pool.map(cpu_task, [100000, 100000])
            
            multiprocessing_time = time.time() - start_time
            print(f"Multiprocessing完成2个CPU任务耗时: {multiprocessing_time:.4f}秒")
        except:
            print("Multiprocessing需要在主模块中运行")
    
    print("\n3. 使用场景总结:")
    print("• Threading: I/O密集型任务 (文件读写、网络请求)")
    print("• Multiprocessing: CPU密集型任务 (数学计算、图像处理)")
    print("• AsyncIO: 大量I/O操作的异步处理")


async def asyncio_example():
    """
    Q10: AsyncIO的工作原理
    """
    print("\n=== AsyncIO异步编程 ===")
    
    async def fetch_data(name, delay):
        print(f"开始获取 {name}")
        await asyncio.sleep(delay)
        print(f"完成获取 {name}")
        return f"数据: {name}"
    
    async def main():
        # 并发执行多个异步任务
        tasks = [
            fetch_data("用户信息", 1),
            fetch_data("订单信息", 2),
            fetch_data("产品信息", 1.5)
        ]
        
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        print(f"异步执行结果: {results}")
        print(f"总耗时: {end_time - start_time:.2f}秒")
        
        return results
    
    # 如果在异步环境中，直接await main()
    # 否则使用 asyncio.run(main())
    print("AsyncIO特点:")
    print("• 单线程并发")
    print("• 事件循环驱动")
    print("• 适合I/O密集型任务")
    print("• 内存占用低")


# ====================== 5. 高级特性 ======================

def generator_vs_iterator():
    """
    Q11: 生成器和迭代器的区别
    """
    print("\n=== 生成器 vs 迭代器 ===")
    
    # 自定义迭代器
    class NumberIterator:
        def __init__(self, max_num):
            self.max_num = max_num
            self.current = 0
        
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.current < self.max_num:
                self.current += 1
                return self.current
            raise StopIteration
    
    # 生成器函数
    def number_generator(max_num):
        current = 0
        while current < max_num:
            current += 1
            yield current
    
    print("1. 迭代器类:")
    iterator = NumberIterator(5)
    for num in iterator:
        print(num, end=" ")
    print()
    
    print("\n2. 生成器函数:")
    generator = number_generator(5)
    for num in generator:
        print(num, end=" ")
    print()
    
    print("\n3. 内存使用对比:")
    
    # 列表 vs 生成器
    import sys
    
    big_list = list(range(10000))
    big_generator = (x for x in range(10000))
    
    print(f"列表内存占用: {sys.getsizeof(big_list)} 字节")
    print(f"生成器内存占用: {sys.getsizeof(big_generator)} 字节")
    
    print("\n4. 生成器的优势:")
    print("• 惰性计算，内存效率高")
    print("• 可以处理无限序列")
    print("• 代码更简洁")


def metaclass_example():
    """
    Q12: 元类的使用和原理
    """
    print("\n=== 元类编程 ===")
    
    # 简单的元类
    class SimpleMeta(type):
        def __new__(mcs, name, bases, attrs):
            # 为所有方法添加日志
            for key, value in attrs.items():
                if callable(value) and not key.startswith('_'):
                    attrs[key] = SimpleMeta.add_logging(value)
            
            return super().__new__(mcs, name, bases, attrs)
        
        @staticmethod
        def add_logging(method):
            def wrapper(*args, **kwargs):
                print(f"调用方法: {method.__name__}")
                return method(*args, **kwargs)
            return wrapper
    
    # 使用元类
    class MyClass(metaclass=SimpleMeta):
        def method1(self):
            return "方法1"
        
        def method2(self):
            return "方法2"
    
    print("使用元类创建的类:")
    obj = MyClass()
    obj.method1()
    obj.method2()
    
    # 动态创建类
    def dynamic_method(self):
        return "动态方法"
    
    DynamicClass = type('DynamicClass', (), {
        'dynamic_method': dynamic_method,
        'class_var': '类变量'
    })
    
    print("\n动态创建的类:")
    dynamic_obj = DynamicClass()
    print(f"动态方法调用: {dynamic_obj.dynamic_method()}")
    print(f"类变量: {dynamic_obj.class_var}")
    
    print("\n元类的作用:")
    print("• 控制类的创建过程")
    print("• 修改类的属性和方法")
    print("• 实现设计模式 (如单例)")
    print("• 框架开发中的应用")


# ====================== 6. 实际应用题目 ======================

def implement_lru_cache():
    """
    Q13: 实现LRU缓存
    """
    print("\n=== 实现LRU缓存 ===")
    
    class LRUCache:
        def __init__(self, capacity):
            self.capacity = capacity
            self.cache = {}
            self.order = []
        
        def get(self, key):
            if key in self.cache:
                # 移动到最近使用
                self.order.remove(key)
                self.order.append(key)
                return self.cache[key]
            return -1
        
        def put(self, key, value):
            if key in self.cache:
                # 更新值并移动到最近使用
                self.cache[key] = value
                self.order.remove(key)
                self.order.append(key)
            else:
                if len(self.cache) >= self.capacity:
                    # 移除最久未使用的
                    oldest = self.order.pop(0)
                    del self.cache[oldest]
                
                self.cache[key] = value
                self.order.append(key)
        
        def display(self):
            print(f"缓存内容: {self.cache}")
            print(f"使用顺序: {self.order}")
    
    # 测试LRU缓存
    lru = LRUCache(3)
    
    print("测试LRU缓存:")
    lru.put(1, "A")
    lru.put(2, "B")
    lru.put(3, "C")
    lru.display()
    
    print(f"\n获取key=2: {lru.get(2)}")
    lru.display()
    
    print("\n添加新元素 (4, 'D'):")
    lru.put(4, "D")
    lru.display()


def implement_singleton():
    """
    Q14: 实现单例模式的多种方法
    """
    print("\n=== 单例模式实现 ===")
    
    # 方法1: 使用__new__
    class Singleton1:
        _instance = None
        
        def __new__(cls):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance
        
        def __init__(self):
            if not hasattr(self, 'initialized'):
                self.value = 0
                self.initialized = True
    
    # 方法2: 使用装饰器
    def singleton(cls):
        instances = {}
        def get_instance(*args, **kwargs):
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]
        return get_instance
    
    @singleton
    class Singleton2:
        def __init__(self):
            self.value = 0
    
    # 方法3: 使用元类
    class SingletonMeta(type):
        _instances = {}
        def __call__(cls, *args, **kwargs):
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
            return cls._instances[cls]
    
    class Singleton3(metaclass=SingletonMeta):
        def __init__(self):
            self.value = 0
    
    # 测试所有实现
    print("测试单例模式:")
    
    s1_a = Singleton1()
    s1_b = Singleton1()
    print(f"Singleton1: {s1_a is s1_b}")
    
    s2_a = Singleton2()
    s2_b = Singleton2()
    print(f"Singleton2: {s2_a is s2_b}")
    
    s3_a = Singleton3()
    s3_b = Singleton3()
    print(f"Singleton3: {s3_a is s3_b}")


def optimize_performance():
    """
    Q15: Python性能优化技巧
    """
    print("\n=== Python性能优化 ===")
    
    import timeit
    
    # 1. 列表推导 vs 循环
    def use_loop():
        result = []
        for i in range(1000):
            if i % 2 == 0:
                result.append(i * 2)
        return result
    
    def use_comprehension():
        return [i * 2 for i in range(1000) if i % 2 == 0]
    
    loop_time = timeit.timeit(use_loop, number=1000)
    comp_time = timeit.timeit(use_comprehension, number=1000)
    
    print("1. 列表推导 vs 循环:")
    print(f"循环耗时: {loop_time:.6f}秒")
    print(f"列表推导耗时: {comp_time:.6f}秒")
    print(f"性能提升: {loop_time / comp_time:.2f}倍")
    
    # 2. 字符串拼接
    def concat_with_plus():
        result = ""
        for i in range(1000):
            result += str(i)
        return result
    
    def concat_with_join():
        return "".join(str(i) for i in range(1000))
    
    plus_time = timeit.timeit(concat_with_plus, number=100)
    join_time = timeit.timeit(concat_with_join, number=100)
    
    print("\n2. 字符串拼接:")
    print(f"+ 操作耗时: {plus_time:.6f}秒")
    print(f"join方法耗时: {join_time:.6f}秒")
    print(f"性能提升: {plus_time / join_time:.2f}倍")
    
    # 3. 局部变量 vs 全局变量
    global_var = range(1000)
    
    def use_global():
        return sum(global_var)
    
    def use_local():
        local_var = range(1000)
        return sum(local_var)
    
    global_time = timeit.timeit(use_global, number=10000)
    local_time = timeit.timeit(use_local, number=10000)
    
    print("\n3. 变量访问:")
    print(f"全局变量耗时: {global_time:.6f}秒")
    print(f"局部变量耗时: {local_time:.6f}秒")
    
    print("\n性能优化建议:")
    print("• 使用列表推导而不是循环")
    print("• 使用join()进行字符串拼接")
    print("• 尽量使用局部变量")
    print("• 避免在循环中进行重复计算")
    print("• 使用内置函数和标准库")
    print("• 考虑使用NumPy进行数值计算")


# ====================== 7. 主测试函数 ======================

def run_all_interviews():
    """运行所有面试题演示"""
    print("🎯 Python面试题库 - 外企技术面试精选")
    print("=" * 60)
    
    # 基础概念
    explain_python_features()
    mutable_vs_immutable()
    explain_gil()
    memory_management()
    
    # 数据结构
    list_vs_tuple_vs_set()
    dict_implementation()
    
    # 函数和作用域
    closure_example()
    decorator_deep_dive()
    
    # 并发编程
    threading_vs_multiprocessing()
    
    # 高级特性
    generator_vs_iterator()
    metaclass_example()
    
    # 实际应用
    implement_lru_cache()
    implement_singleton()
    optimize_performance()
    
    print("\n🎉 面试题演示完成！")
    print("\n📝 面试建议:")
    print("1. 深入理解每个概念的原理")
    print("2. 能够用简洁的语言解释复杂概念")
    print("3. 准备具体的代码示例")
    print("4. 了解实际应用场景")
    print("5. 关注性能和最佳实践")


def quick_reference():
    """面试快速参考"""
    print("\n📚 Python面试快速参考")
    print("=" * 40)
    
    reference = {
        "时间复杂度": {
            "list访问": "O(1)",
            "list查找": "O(n)", 
            "list插入": "O(n)",
            "dict访问": "O(1)",
            "set查找": "O(1)"
        },
        "内存管理": {
            "引用计数": "主要机制",
            "循环引用": "标记清除解决",
            "分代回收": "优化策略"
        },
        "并发编程": {
            "CPU密集": "multiprocessing",
            "I/O密集": "threading/asyncio",
            "GIL限制": "单线程执行Python字节码"
        },
        "常用装饰器": {
            "@property": "属性访问",
            "@staticmethod": "静态方法",
            "@classmethod": "类方法",
            "@functools.lru_cache": "缓存结果"
        }
    }
    
    for category, items in reference.items():
        print(f"\n{category}:")
        for key, value in items.items():
            print(f"  • {key}: {value}")


if __name__ == "__main__":
    run_all_interviews()
    quick_reference()
