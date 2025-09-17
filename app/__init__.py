from flask import Flask  # 导入Flask主类，用于创建Web应用
from flask_sqlalchemy import SQLAlchemy  # 导入SQLAlchemy，用于数据库操作
from flask_migrate import Migrate  # 导入Migrate，用于数据库迁移
from flask_login import LoginManager  # 导入LoginManager，用于用户认证管理
from config import Config  # 从config.py导入配置类

# 创建扩展实例
# 这些实例将在整个应用中使用
db = SQLAlchemy()  # 创建数据库实例，用于ORM操作
migrate = Migrate()  # 创建迁移实例，用于数据库版本管理
login = LoginManager()  # 创建登录管理器，处理用户会话
login.login_view = 'auth.login'  # 设置登录页面的路由名称
login.login_message = '请先登录后再访问此页面。'  # 未登录时的提示消息

def create_app(config_class=Config):
    """
    应用工厂函数
    这是一个设计模式，可以创建多个不同配置的Flask应用实例
    
    参数：
    config_class: 配置类，默认使用Config
    
    返回：
    Flask应用实例
    """
    
    # 创建Flask应用实例
    app = Flask(__name__)
    
    # 加载配置
    # from_object方法会从配置类中加载所有大写变量
    app.config.from_object(config_class)
    
    # 初始化扩展
    # 将扩展与Flask应用关联
    db.init_app(app)  # 初始化数据库
    migrate.init_app(app, db)  # 初始化迁移工具
    login.init_app(app)  # 初始化登录管理器
    
    # 注册蓝图（模块）
    # 蓝图是Flask中组织路由的一种方式，每个功能模块一个蓝图
    
    # 注册主页蓝图
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    # 注册认证蓝图（登录、注册等）
    # url_prefix='/auth'表示所有路由前面加上/auth
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # 注册文章蓝图
    # url_prefix='/post'表示所有路由前面加上/post
    from app.post import bp as post_bp
    app.register_blueprint(post_bp, url_prefix='/post')
    
    # 返回配置完成的应用实例
    return app

# 导入模型，确保在应用上下文中可用
# 这行代码必须在create_app之后，避免循环导入
from app.models import user, post