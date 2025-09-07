"""
Flask Web开发进阶示例 - 外企面试项目
包含认证、缓存、限流、错误处理等企业级特性
"""

from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import redis
import time
import logging
from datetime import datetime, timedelta
import json
from collections import defaultdict
import threading


# ====================== 1. 应用配置 ======================

class Config:
    """应用配置类"""
    SECRET_KEY = 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///enterprise_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRATION_DELTA = timedelta(hours=24)
    REDIS_URL = 'redis://localhost:6379/0'
    RATE_LIMIT_STORAGE_URL = 'redis://localhost:6379/1'


# ====================== 2. 应用初始化 ======================

app = Flask(__name__)
app.config.from_object(Config)

# 数据库
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Redis缓存
try:
    redis_client = redis.from_url(app.config['REDIS_URL'])
    redis_client.ping()
except:
    redis_client = None
    print("Redis未连接，将使用内存缓存")

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


# ====================== 3. 数据模型 ======================

class User(db.Model):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # 关系
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """设置密码哈希"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def generate_token(self):
        """生成JWT令牌"""
        payload = {
            'user_id': self.id,
            'username': self.username,
            'exp': datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']
        }
        return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_token(token):
        """验证JWT令牌"""
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            return User.query.get(payload['user_id'])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }


class Post(db.Model):
    """文章模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published = db.Column(db.Boolean, default=False)
    view_count = db.Column(db.Integer, default=0)
    
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'published': self.published,
            'view_count': self.view_count,
            'author': self.author.username
        }


# ====================== 4. 缓存系统 ======================

class CacheManager:
    """缓存管理器"""
    
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.memory_cache = {} if not redis_client else None
    
    def get(self, key):
        """获取缓存"""
        if self.redis:
            try:
                value = self.redis.get(key)
                return json.loads(value) if value else None
            except:
                return None
        else:
            return self.memory_cache.get(key)
    
    def set(self, key, value, expire=3600):
        """设置缓存"""
        if self.redis:
            try:
                self.redis.setex(key, expire, json.dumps(value))
            except:
                pass
        else:
            self.memory_cache[key] = value
    
    def delete(self, key):
        """删除缓存"""
        if self.redis:
            try:
                self.redis.delete(key)
            except:
                pass
        else:
            self.memory_cache.pop(key, None)
    
    def clear_pattern(self, pattern):
        """删除匹配模式的缓存"""
        if self.redis:
            try:
                keys = self.redis.keys(pattern)
                if keys:
                    self.redis.delete(*keys)
            except:
                pass
        else:
            keys_to_delete = [k for k in self.memory_cache.keys() if pattern.replace('*', '') in k]
            for key in keys_to_delete:
                del self.memory_cache[key]


cache_manager = CacheManager(redis_client)


# ====================== 5. 限流系统 ======================

class RateLimiter:
    """限流器"""
    
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.memory_store = defaultdict(list) if not redis_client else None
        self.lock = threading.Lock() if not redis_client else None
    
    def is_allowed(self, key, limit, window):
        """检查是否允许请求"""
        now = time.time()
        
        if self.redis:
            return self._redis_check(key, limit, window, now)
        else:
            return self._memory_check(key, limit, window, now)
    
    def _redis_check(self, key, limit, window, now):
        """Redis限流检查"""
        try:
            pipe = self.redis.pipeline()
            pipe.zremrangebyscore(key, 0, now - window)
            pipe.zcard(key)
            pipe.zadd(key, {str(now): now})
            pipe.expire(key, int(window) + 1)
            results = pipe.execute()
            
            return results[1] < limit
        except:
            return True
    
    def _memory_check(self, key, limit, window, now):
        """内存限流检查"""
        with self.lock:
            timestamps = self.memory_store[key]
            
            # 清理过期记录
            timestamps[:] = [t for t in timestamps if now - t < window]
            
            if len(timestamps) < limit:
                timestamps.append(now)
                return True
            
            return False


rate_limiter = RateLimiter(redis_client)


# ====================== 6. 装饰器 ======================

def auth_required(f):
    """认证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': '缺少认证令牌'}), 401
        
        try:
            token = token.replace('Bearer ', '')
            user = User.verify_token(token)
            
            if not user:
                return jsonify({'error': '无效的令牌'}), 401
            
            if not user.is_active:
                return jsonify({'error': '用户已被禁用'}), 401
            
            g.current_user = user
            
        except Exception as e:
            logger.error(f"认证错误: {e}")
            return jsonify({'error': '认证失败'}), 401
        
        return f(*args, **kwargs)
    
    return decorated


def admin_required(f):
    """管理员权限装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(g, 'current_user') or not g.current_user.is_admin:
            return jsonify({'error': '需要管理员权限'}), 403
        
        return f(*args, **kwargs)
    
    return decorated


def rate_limit_decorator(limit=100, window=3600, key_func=None):
    """限流装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # 生成限流键
            if key_func:
                key = key_func()
            else:
                key = f"rate_limit:{request.remote_addr}:{f.__name__}"
            
            if not rate_limiter.is_allowed(key, limit, window):
                return jsonify({
                    'error': '请求过于频繁',
                    'retry_after': window
                }), 429
            
            return f(*args, **kwargs)
        
        return decorated
    return decorator


def cache_result(expire=3600, key_func=None):
    """缓存装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # 生成缓存键
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = f"cache:{f.__name__}:{hash(str(args) + str(kwargs))}"
            
            # 尝试从缓存获取
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                logger.info(f"缓存命中: {cache_key}")
                return cached_result
            
            # 执行函数并缓存结果
            result = f(*args, **kwargs)
            cache_manager.set(cache_key, result, expire)
            logger.info(f"缓存存储: {cache_key}")
            
            return result
        
        return decorated
    return decorator


# ====================== 7. API路由 ======================

@app.route('/api/register', methods=['POST'])
@rate_limit_decorator(limit=5, window=300)  # 5分钟内最多5次
def register():
    """用户注册"""
    try:
        data = request.get_json()
        
        # 验证输入
        if not data or not data.get('username') or not data.get('password') or not data.get('email'):
            return jsonify({'error': '缺少必要字段'}), 400
        
        # 检查用户是否已存在
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': '用户名已存在'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': '邮箱已存在'}), 400
        
        # 创建用户
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        logger.info(f"新用户注册: {user.username}")
        
        return jsonify({
            'message': '注册成功',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"注册错误: {e}")
        return jsonify({'error': '注册失败'}), 500


@app.route('/api/login', methods=['POST'])
@rate_limit_decorator(limit=10, window=300)  # 5分钟内最多10次
def login():
    """用户登录"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': '缺少用户名或密码'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            logger.warning(f"登录失败: {data['username']}")
            return jsonify({'error': '用户名或密码错误'}), 401
        
        if not user.is_active:
            return jsonify({'error': '用户已被禁用'}), 401
        
        # 更新最后登录时间
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # 生成令牌
        token = user.generate_token()
        
        logger.info(f"用户登录: {user.username}")
        
        return jsonify({
            'message': '登录成功',
            'token': token,
            'user': user.to_dict()
        })
        
    except Exception as e:
        logger.error(f"登录错误: {e}")
        return jsonify({'error': '登录失败'}), 500


@app.route('/api/profile', methods=['GET'])
@auth_required
def get_profile():
    """获取用户资料"""
    return jsonify({
        'user': g.current_user.to_dict()
    })


@app.route('/api/posts', methods=['GET'])
@cache_result(expire=300, key_func=lambda: f"posts:{request.args.to_dict()}")
def get_posts():
    """获取文章列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        per_page = min(per_page, 100)  # 限制每页最大数量
        
        query = Post.query.filter_by(published=True)
        
        # 搜索
        search = request.args.get('search')
        if search:
            query = query.filter(Post.title.contains(search))
        
        posts = query.order_by(Post.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'posts': [post.to_dict() for post in posts.items],
            'pagination': {
                'page': page,
                'pages': posts.pages,
                'per_page': per_page,
                'total': posts.total
            }
        })
        
    except Exception as e:
        logger.error(f"获取文章列表错误: {e}")
        return jsonify({'error': '获取文章失败'}), 500


@app.route('/api/posts', methods=['POST'])
@auth_required
@rate_limit_decorator(limit=20, window=3600)  # 1小时内最多20篇
def create_post():
    """创建文章"""
    try:
        data = request.get_json()
        
        if not data or not data.get('title') or not data.get('content'):
            return jsonify({'error': '缺少标题或内容'}), 400
        
        post = Post(
            title=data['title'],
            content=data['content'],
            published=data.get('published', False),
            user_id=g.current_user.id
        )
        
        db.session.add(post)
        db.session.commit()
        
        # 清理相关缓存
        cache_manager.clear_pattern('posts:*')
        
        logger.info(f"用户 {g.current_user.username} 创建文章: {post.title}")
        
        return jsonify({
            'message': '文章创建成功',
            'post': post.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"创建文章错误: {e}")
        return jsonify({'error': '创建文章失败'}), 500


@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """获取单篇文章"""
    try:
        post = Post.query.get_or_404(post_id)
        
        if not post.published and (not hasattr(g, 'current_user') or g.current_user.id != post.user_id):
            return jsonify({'error': '文章不存在'}), 404
        
        # 增加浏览量
        post.view_count += 1
        db.session.commit()
        
        return jsonify({
            'post': post.to_dict()
        })
        
    except Exception as e:
        logger.error(f"获取文章错误: {e}")
        return jsonify({'error': '获取文章失败'}), 500


@app.route('/api/admin/users', methods=['GET'])
@auth_required
@admin_required
def admin_get_users():
    """管理员获取用户列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        users = User.query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'pagination': {
                'page': page,
                'pages': users.pages,
                'per_page': per_page,
                'total': users.total
            }
        })
        
    except Exception as e:
        logger.error(f"获取用户列表错误: {e}")
        return jsonify({'error': '获取用户列表失败'}), 500


# ====================== 8. 错误处理 ======================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '资源未找到'}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    logger.error(f"内部错误: {error}")
    return jsonify({'error': '内部服务器错误'}), 500


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': '请求参数错误'}), 400


# ====================== 9. 中间件 ======================

@app.before_request
def before_request():
    """请求前处理"""
    g.start_time = time.time()
    
    # 记录请求
    logger.info(f"{request.method} {request.path} from {request.remote_addr}")


@app.after_request
def after_request(response):
    """请求后处理"""
    # 计算处理时间
    if hasattr(g, 'start_time'):
        processing_time = time.time() - g.start_time
        response.headers['X-Processing-Time'] = f"{processing_time:.3f}s"
    
    # 添加CORS头
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    
    return response


# ====================== 10. 健康检查和监控 ======================

@app.route('/health')
def health_check():
    """健康检查端点"""
    try:
        # 检查数据库连接
        db.session.execute('SELECT 1')
        
        # 检查Redis连接
        redis_status = 'connected' if redis_client and redis_client.ping() else 'disconnected'
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'database': 'connected',
            'redis': redis_status,
            'version': '1.0.0'
        })
        
    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


@app.route('/metrics')
def metrics():
    """应用指标"""
    try:
        user_count = User.query.count()
        post_count = Post.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        
        return jsonify({
            'users': {
                'total': user_count,
                'active': active_users
            },
            'posts': {
                'total': post_count,
                'published': Post.query.filter_by(published=True).count()
            },
            'cache': {
                'type': 'redis' if redis_client else 'memory',
                'status': 'connected' if redis_client else 'local'
            }
        })
        
    except Exception as e:
        logger.error(f"获取指标失败: {e}")
        return jsonify({'error': '获取指标失败'}), 500


# ====================== 11. 数据库初始化 ======================

def init_db():
    """初始化数据库"""
    with app.app_context():
        db.create_all()
        
        # 创建管理员用户
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("管理员用户已创建: admin/admin123")


# ====================== 12. 运行应用 ======================

if __name__ == '__main__':
    init_db()
    
    print("🚀 Flask企业级应用启动")
    print("功能特性:")
    print("• JWT认证和授权")
    print("• Redis缓存")
    print("• 请求限流")
    print("• 错误处理")
    print("• 日志记录")
    print("• 健康检查")
    print("• API文档")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
