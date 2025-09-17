from datetime import datetime  # 导入日期时间模块
from flask_sqlalchemy import SQLAlchemy  # 导入SQLAlchemy ORM框架
from app import db  # 从app包导入数据库实例

class Post(db.Model):
    """
    文章模型类
    对应数据库中的posts表
    存储博客文章的基本信息
    """
    
    # 指定对应的数据库表名
    __tablename__ = 'posts'
    
    # 定义表的字段（列）
    id = db.Column(db.Integer, primary_key=True)  # 主键，自动递增的整数ID
    title = db.Column(db.String(200), nullable=False)  # 文章标题，最大200字符，不能为空
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)  # URL友好的文章标识符，唯一，建立索引
    content = db.Column(db.Text, nullable=False)  # 文章内容，长文本，不能为空
    summary = db.Column(db.String(500))  # 文章摘要，最大500字符，可为空
    featured_image = db.Column(db.String(300))  # 特色图片URL，可为空
    is_published = db.Column(db.Boolean, default=False)  # 是否已发布，默认为False（草稿）
    view_count = db.Column(db.Integer, default=0)  # 浏览次数，默认为0
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间，默认为当前时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间，修改时自动更新
    published_at = db.Column(db.DateTime)  # 发布时间，可为空（草稿没有发布时间）
    
    # 外键 - 关联到用户表
    # db.ForeignKey('users.id')表示这个字段引用users表的id字段
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 作者ID，不能为空
    
    # 关联关系
    # 一篇文章有多条评论
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    
    # 多对多关系：一篇文章有多个标签，一个标签可以属于多篇文章
    # secondary='post_tags'指定关联表（中间表）的名称
    tags = db.relationship('Tag', secondary='post_tags', backref='posts')
    
    def __repr__(self):
        """
        对象的字符串表示，调试时很有用
        例如：<Post 我的第一篇文章>
        """
        return f'<Post {self.title}>'
    
    def increment_view(self):
        """
        增加文章浏览次数
        每次调用这个方法，view_count加1
        """
        self.view_count += 1  # 浏览次数加1
        db.session.commit()   # 提交到数据库

class Comment(db.Model):
    """
    评论模型类
    对应数据库中的comments表
    存储用户对文章的评论
    """
    
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)  # 主键，评论ID
    content = db.Column(db.Text, nullable=False)  # 评论内容，不能为空
    is_approved = db.Column(db.Boolean, default=True)  # 是否已审核通过，默认为True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 评论者ID
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)  # 所属文章ID
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))  # 父评论ID，用于回复功能
    
    # 自关联关系：评论可以回复其他评论
    # remote_side=[id]表示关系的远端是Comment.id
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    
    def __repr__(self):
        return f'<Comment {self.id}>'

class Tag(db.Model):
    """
    标签模型类
    对应数据库中的tags表
    用于给文章分类和标记
    """
    
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)  # 主键，标签ID
    name = db.Column(db.String(50), unique=True, nullable=False)  # 标签名称，唯一，不能为空
    slug = db.Column(db.String(50), unique=True, nullable=False)  # URL友好的标签标识符
    color = db.Column(db.String(7), default='#007bff')  # 标签颜色，十六进制颜色代码，默认为蓝色
    
    def __repr__(self):
        return f'<Tag {self.name}>'

# 多对多关联表（中间表）
# 因为文章和标签是多对多关系，需要一张中间表来存储关联
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),  # 文章ID，外键
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)    # 标签ID，外键
    # 两个字段一起组成复合主键，确保一篇文章不会重复关联同一个标签
)