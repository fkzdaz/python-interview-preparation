"""
Python高级特性练习 - 外企面试必备
包含装饰器、生成器、上下文管理器、元类等高级概念
"""

import time
import functools
import threading
from contextlib import contextmanager
from abc import ABC, abstractmethod
import weakref
from collections import defaultdict
import asyncio


# ====================== 1. 装饰器 ======================

def timing_decorator(func):
    """计时装饰器 - 测量函数执行时间"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 执行时间: {end - start:.4f} 秒")
        return result
    return wrapper


def retry(max_attempts=3, delay=1):
    """重试装饰器 - 自动重试失败的函数"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        print(f"第 {attempt + 1} 次尝试失败: {e}, {delay}秒后重试...")
                        time.sleep(delay)
                    else:
                        print(f"所有 {max_attempts} 次尝试都失败了")
            
            raise last_exception
        return wrapper
    return decorator


def cache(func):
    """简单的缓存装饰器"""
    cached_results = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 创建缓存键
        key = str(args) + str(sorted(kwargs.items()))
        
        if key in cached_results:
            print(f"缓存命中: {func.__name__}")
            return cached_results[key]
        
        result = func(*args, **kwargs)
        cached_results[key] = result
        print(f"缓存存储: {func.__name__}")
        return result
    
    return wrapper


def rate_limit(calls_per_second=1):
    """限流装饰器"""
    def decorator(func):
        last_called = [0.0]
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            time_since_last_call = now - last_called[0]
            min_interval = 1.0 / calls_per_second
            
            if time_since_last_call < min_interval:
                sleep_time = min_interval - time_since_last_call
                time.sleep(sleep_time)
            
            last_called[0] = time.time()
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


class classproperty:
    """类属性装饰器"""
    def __init__(self, func):
        self.func = func
    
    def __get__(self, obj, owner):
        return self.func(owner)


# ====================== 2. 生成器和迭代器 ======================

def fibonacci_generator():
    """斐波那契数列生成器"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def range_generator(start, end, step=1):
    """自定义range生成器"""
    current = start
    while current < end:
        yield current
        current += step


def batch_generator(iterable, batch_size):
    """批处理生成器 - 将大数据集分批处理"""
    iterator = iter(iterable)
    while True:
        batch = []
        for _ in range(batch_size):
            try:
                batch.append(next(iterator))
            except StopIteration:
                if batch:
                    yield batch
                return
        yield batch


def file_reader_generator(filename):
    """文件读取生成器 - 逐行读取大文件"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                yield line_number, line.strip()
    except FileNotFoundError:
        print(f"文件 {filename} 不存在")


class NumberRange:
    """自定义迭代器类"""
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        
        current = self.current
        self.current += 1
        return current


# ====================== 3. 上下文管理器 ======================

class DatabaseConnection:
    """数据库连接上下文管理器"""
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None
    
    def __enter__(self):
        print(f"连接数据库: {self.connection_string}")
        self.connection = f"连接到 {self.connection_string}"
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("关闭数据库连接")
        if exc_type:
            print(f"发生异常: {exc_val}")
            return False  # 不抑制异常
        return True


@contextmanager
def temporary_file(filename, content=""):
    """临时文件上下文管理器"""
    print(f"创建临时文件: {filename}")
    
    try:
        with open(filename, 'w') as f:
            f.write(content)
        yield filename
    finally:
        import os
        if os.path.exists(filename):
            os.remove(filename)
            print(f"删除临时文件: {filename}")


@contextmanager
def timer_context(name):
    """计时上下文管理器"""
    start = time.time()
    print(f"开始执行: {name}")
    
    try:
        yield
    finally:
        end = time.time()
        print(f"{name} 完成，耗时: {end - start:.4f} 秒")


class ThreadLock:
    """线程锁上下文管理器"""
    def __init__(self):
        self._lock = threading.Lock()
    
    def __enter__(self):
        self._lock.acquire()
        print("获取线程锁")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()
        print("释放线程锁")


# ====================== 4. 元类编程 ======================

class SingletonMeta(type):
    """单例模式元类"""
    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    """使用单例元类的数据库类"""
    def __init__(self):
        self.connection = "数据库连接"
        print("创建数据库实例")


class AttributeValidatorMeta(type):
    """属性验证元类"""
    def __new__(mcs, name, bases, attrs):
        # 为所有方法添加验证
        for key, value in attrs.items():
            if callable(value) and not key.startswith('_'):
                attrs[key] = mcs.validate_method(value)
        
        return super().__new__(mcs, name, bases, attrs)
    
    @staticmethod
    def validate_method(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            print(f"验证方法 {method.__name__} 的调用")
            return method(self, *args, **kwargs)
        return wrapper


def create_model_class(name, fields):
    """动态创建模型类"""
    def __init__(self, **kwargs):
        for field in fields:
            setattr(self, field, kwargs.get(field))
    
    def __repr__(self):
        field_values = ', '.join(f'{k}={v}' for k, v in self.__dict__.items())
        return f"{name}({field_values})"
    
    def to_dict(self):
        return {field: getattr(self, field, None) for field in fields}
    
    # 动态创建类
    return type(name, (), {
        '__init__': __init__,
        '__repr__': __repr__,
        'to_dict': to_dict,
        'fields': fields
    })


# ====================== 5. 设计模式 ======================

class Observer(ABC):
    """观察者模式 - 观察者接口"""
    @abstractmethod
    def update(self, message):
        pass


class Subject:
    """观察者模式 - 主题类"""
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)
    
    def notify(self, message):
        for observer in self._observers:
            observer.update(message)


class EmailNotifier(Observer):
    """具体观察者 - 邮件通知"""
    def __init__(self, email):
        self.email = email
    
    def update(self, message):
        print(f"发送邮件到 {self.email}: {message}")


class SMSNotifier(Observer):
    """具体观察者 - 短信通知"""
    def __init__(self, phone):
        self.phone = phone
    
    def update(self, message):
        print(f"发送短信到 {self.phone}: {message}")


class Factory(ABC):
    """工厂模式 - 抽象工厂"""
    @abstractmethod
    def create_product(self):
        pass


class ConcreteFactory(Factory):
    """具体工厂"""
    def create_product(self, product_type):
        if product_type == "A":
            return ProductA()
        elif product_type == "B":
            return ProductB()
        else:
            raise ValueError(f"未知产品类型: {product_type}")


class Product:
    """产品基类"""
    def operation(self):
        pass


class ProductA(Product):
    def operation(self):
        return "产品A的操作"


class ProductB(Product):
    def operation(self):
        return "产品B的操作"


# ====================== 6. 内存管理和性能优化 ======================

class MemoryPool:
    """简单的内存池实现"""
    def __init__(self, size=100):
        self._pool = [None] * size
        self._free_indices = list(range(size))
    
    def allocate(self):
        if not self._free_indices:
            raise RuntimeError("内存池已满")
        
        index = self._free_indices.pop()
        self._pool[index] = {}
        return index, self._pool[index]
    
    def deallocate(self, index):
        if 0 <= index < len(self._pool) and self._pool[index] is not None:
            self._pool[index] = None
            self._free_indices.append(index)


class WeakReferenceCache:
    """使用弱引用的缓存"""
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()
    
    def get(self, key):
        return self._cache.get(key)
    
    def set(self, key, value):
        self._cache[key] = value
    
    def size(self):
        return len(self._cache)


# ====================== 7. 异步编程 ======================

async def async_fetch_data(url, delay=1):
    """模拟异步获取数据"""
    print(f"开始获取数据: {url}")
    await asyncio.sleep(delay)
    print(f"完成获取数据: {url}")
    return f"数据来自 {url}"


async def async_batch_process(urls):
    """批量异步处理"""
    tasks = [async_fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results


class AsyncContextManager:
    """异步上下文管理器"""
    async def __aenter__(self):
        print("异步进入上下文")
        await asyncio.sleep(0.1)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("异步退出上下文")
        await asyncio.sleep(0.1)


# ====================== 8. 实践示例和测试 ======================

@timing_decorator
@cache
def expensive_function(n):
    """模拟耗时的计算函数"""
    time.sleep(0.1)
    return sum(i ** 2 for i in range(n))


@retry(max_attempts=3)
def unreliable_function():
    """模拟不稳定的函数"""
    import random
    if random.random() < 0.7:
        raise Exception("随机失败")
    return "成功"


class User(metaclass=AttributeValidatorMeta):
    """使用验证元类的用户类"""
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def get_info(self):
        return f"用户: {self.name}, 邮箱: {self.email}"


def demonstrate_generators():
    """演示生成器的使用"""
    print("\n=== 生成器演示 ===")
    
    # 斐波那契数列
    fib = fibonacci_generator()
    print("前10个斐波那契数:")
    for i, num in enumerate(fib):
        if i >= 10:
            break
        print(num, end=" ")
    print()
    
    # 批处理生成器
    data = list(range(23))
    print(f"\n原始数据: {data}")
    print("批处理结果:")
    for batch in batch_generator(data, 5):
        print(batch)


def demonstrate_context_managers():
    """演示上下文管理器的使用"""
    print("\n=== 上下文管理器演示 ===")
    
    # 数据库连接
    with DatabaseConnection("mysql://localhost") as conn:
        print(f"使用连接: {conn}")
    
    # 计时器
    with timer_context("复杂计算"):
        time.sleep(0.5)
        result = sum(i ** 2 for i in range(1000))
        print(f"计算结果: {result}")


def demonstrate_design_patterns():
    """演示设计模式的使用"""
    print("\n=== 设计模式演示 ===")
    
    # 观察者模式
    subject = Subject()
    email_notifier = EmailNotifier("user@example.com")
    sms_notifier = SMSNotifier("123-456-7890")
    
    subject.attach(email_notifier)
    subject.attach(sms_notifier)
    subject.notify("系统维护通知")
    
    # 单例模式
    db1 = Database()
    db2 = Database()
    print(f"数据库实例是否相同: {db1 is db2}")
    
    # 工厂模式
    factory = ConcreteFactory()
    product_a = factory.create_product("A")
    print(f"产品A操作: {product_a.operation()}")


async def demonstrate_async():
    """演示异步编程"""
    print("\n=== 异步编程演示 ===")
    
    urls = ["http://api1.com", "http://api2.com", "http://api3.com"]
    results = await async_batch_process(urls)
    print("异步处理结果:")
    for result in results:
        print(f"  {result}")
    
    # 异步上下文管理器
    async with AsyncContextManager():
        await asyncio.sleep(0.1)
        print("在异步上下文中执行操作")


def main():
    """主演示函数"""
    print("🐍 Python高级特性演示")
    print("=" * 50)
    
    # 装饰器演示
    print("\n=== 装饰器演示 ===")
    result1 = expensive_function(100)
    result2 = expensive_function(100)  # 应该从缓存获取
    
    try:
        result = unreliable_function()
        print(f"不稳定函数结果: {result}")
    except Exception as e:
        print(f"函数最终失败: {e}")
    
    # 元类演示
    print("\n=== 元类演示 ===")
    user = User("张三", "zhangsan@example.com")
    print(user.get_info())
    
    # 动态类创建
    Student = create_model_class("Student", ["name", "age", "grade"])
    student = Student(name="李四", age=20, grade="A")
    print(f"动态创建的学生类: {student}")
    print(f"学生信息字典: {student.to_dict()}")
    
    # 其他演示
    demonstrate_generators()
    demonstrate_context_managers()
    demonstrate_design_patterns()
    
    # 异步演示
    print("\n运行异步演示...")
    asyncio.run(demonstrate_async())
    
    print("\n🎉 所有演示完成！")


if __name__ == "__main__":
    main()
