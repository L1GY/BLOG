#!/usr/bin/env python3
"""
Flask博客网站启动脚本
这个文件是整个网站的入口点，就像main函数一样
"""

import os  # 导入操作系统功能，用于创建文件夹等
from app import create_app, db  # 从app包导入创建应用的函数和数据库实例
from app.models.user import User  # 导入用户模型类
from app.models.post import Post, Tag, Comment  # 导入文章相关模型类
from flask_migrate import upgrade  # 导入数据库迁移升级功能

# 创建Flask应用实例
# create_app()是工厂函数，返回配置好的Flask应用
app = create_app()

@app.shell_context_processor
def make_shell_context():
    """
    为Flask shell添加上下文
    当你在终端输入'flask shell'时，这些变量会自动可用
    方便调试和测试
    """
    return {
        'db': db,           # 数据库实例
        'User': User,       # 用户模型类
        'Post': Post,       # 文章模型类
        'Tag': Tag,         # 标签模型类
        'Comment': Comment  # 评论模型类
    }

if __name__ == '__main__':
    # 这个判断确保只有直接运行这个文件时才会执行下面的代码
    # 如果被其他文件导入，不会执行
    
    # 确保上传目录存在
    # exist_ok=True表示如果目录已存在不会报错
    os.makedirs('app/static/uploads', exist_ok=True)
    
    # 初始化数据库
    # app.app_context()创建应用上下文，确保数据库操作在应用环境中执行
    with app.app_context():
        upgrade()  # 执行数据库迁移，确保所有表都存在
    
    # 启动Flask开发服务器
    # debug=True开启调试模式，代码修改后自动重启
    # host='0.0.0.0'允许外部访问
    # port=5000使用5000端口
    app.run(debug=True, host='0.0.0.0', port=5000)