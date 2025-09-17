import os  # 导入操作系统功能，用于文件路径操作
from dotenv import load_dotenv  # 导入dotenv库，用于加载.env文件中的配置

# 获取当前文件的绝对路径
# __file__是当前文件的路径，os.path.abspath转换为绝对路径
# os.path.dirname获取目录路径
basedir = os.path.abspath(os.path.dirname(__file__))

# 加载.env文件中的环境变量
# 这样可以把敏感信息（如密码）放在.env文件中，而不是硬编码在代码里
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """
    配置类，存储所有应用的配置
    使用类的好处是可以继承和扩展
    """
    
    # 应用密钥，用于加密session等敏感数据
    # 从环境变量获取，如果没有就使用默认值
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    
    # MySQL数据库配置
    # 从环境变量获取，这样不同环境（开发、测试、生产）可以用不同配置
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'           # 数据库用户名
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'password'  # 数据库密码
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'      # 数据库服务器地址
    MYSQL_PORT = os.environ.get('MYSQL_PORT') or '3306'           # 数据库端口
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'flaskblog'  # 数据库名称
    
    # 构建MySQL连接URI（统一资源标识符）
    # 格式：mysql+pymysql://用户名:密码@主机:端口/数据库名
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
    
    # 是否追踪数据库修改，设为False可以提高性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 分页配置
    POSTS_PER_PAGE = 10      # 每页显示的文章数量
    COMMENTS_PER_PAGE = 10   # 每页显示的评论数量
    
    # 管理员邮箱
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@example.com'
    
    # 上传配置
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')  # 上传文件保存路径
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大上传文件大小：16MB（16*1024*1024字节）