from datetime import datetime  # 导入日期时间模块，用于记录创建和更新时间
from flask_sqlalchemy import SQLAlchemy  # 导入SQLAlchemy，ORM框架
from flask_login import UserMixin  # 导入用户认证基类，提供用户会话管理功能
from werkzeug.security import generate_password_hash, check_password_hash  # 导入密码加密和验证工具
from app import db, login  # 从app包导入数据库实例和登录管理器

class User(UserMixin, db.Model):
    """
    用户模型类
    对应数据库中的users表
    UserMixin提供Flask-Login需要的用户认证方法
    """
    
    # 指定对应的数据库表名
    __tablename__ = 'users'
    
    # 定义表的字段（列）
    id = db.Column(db.Integer, primary_key=True)  # 主键，自动递增的整数ID
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)  # 用户名，唯一，不能为空，建立索引
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)     # 邮箱，唯一，不能为空，建立索引
    password_hash = db.Column(db.String(255))  # 密码哈希，存储加密后的密码，长度增加到255以容纳scrypt等长哈希
    avatar_url = db.Column(db.String(200))     # 头像URL，存储用户头像图片地址
    bio = db.Column(db.Text)                   # 个人简介，长文本
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间，默认为当前时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间，修改时自动更新
    is_admin = db.Column(db.Boolean, default=False)  # 是否管理员，默认为False
    
    # 定义关系（外键关联）
    # 一个用户有多篇文章，backref='author'表示Post类可以通过author访问对应的用户
    # lazy='dynamic'返回查询对象，可以进一步筛选
    # cascade='all, delete-orphan'表示删除用户时同时删除其所有文章
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    
    # 一个用户有多条评论
    comments = db.relationship('Comment', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        """
        对象的字符串表示，调试时很有用
        例如：<User zhangsan>
        """
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """
        设置用户密码
        接收明文密码，生成哈希值存储到数据库
        """
        # 使用Werkzeug的generate_password_hash生成安全的密码哈希
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        检查密码是否正确
        接收明文密码，与存储的哈希值比较
        返回True或False
        """
        # 使用Werkzeug的check_password_hash验证密码
        return check_password_hash(self.password_hash, password)
    
    def get_posts_count(self):
        """
        获取用户的文章数量
        返回整数
        """
        return self.posts.count()

# 用户加载回调函数
# Flask-Login需要这个函数来从用户ID获取用户对象
@login.user_loader
def load_user(id):
    """
    从用户ID加载用户对象
    用于Flask-Login的会话管理
    id参数是字符串，需要转换为整数
    """
    # 使用User.query.get()通过主键查询用户
    return User.query.get(int(id))