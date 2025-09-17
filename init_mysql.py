#!/usr/bin/env python3
"""
MySQL数据库初始化脚本
用于创建数据库和表结构
"""

import pymysql
import os
from config import Config

def create_database():
    """创建MySQL数据库"""
    try:
        # 连接MySQL服务器（不指定数据库）
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            port=int(Config.MYSQL_PORT),
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # 创建数据库（如果不存在）
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✓ 数据库 '{Config.MYSQL_DATABASE}' 创建成功或已存在")
            
        connection.commit()
        connection.close()
        return True
        
    except Exception as e:
        print(f"✗ 数据库创建失败: {e}")
        return False

def check_mysql_connection():
    """检查MySQL连接"""
    try:
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            port=int(Config.MYSQL_PORT),
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE,
            charset='utf8mb4'
        )
        connection.close()
        print("✓ MySQL连接成功")
        return True
    except Exception as e:
        print(f"✗ MySQL连接失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("MySQL数据库初始化")
    print("=" * 50)
    
    print(f"数据库配置:")
    print(f"主机: {Config.MYSQL_HOST}:{Config.MYSQL_PORT}")
    print(f"用户: {Config.MYSQL_USER}")
    print(f"数据库: {Config.MYSQL_DATABASE}")
    print()
    
    # 创建数据库
    if not create_database():
        return False
    
    # 检查连接
    if not check_mysql_connection():
        return False
    
    print("\n" + "=" * 50)
    print("MySQL数据库初始化完成！")
    print("=" * 50)
    print("接下来请运行: python setup.py")

if __name__ == "__main__":
    main()