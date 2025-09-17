# MySQL数据库配置指南

## 🎯 概述

本项目已完全配置为使用MySQL数据库。

## 📋 配置步骤

### 1. 安装MySQL
确保已安装MySQL 5.7+ 或 MariaDB 10.2+

### 2. 创建数据库
使用以下任一方法创建数据库：

#### 方法A：自动创建（推荐）
```bash
python init_mysql.py
```

#### 方法B：手动创建
```sql
-- 登录MySQL
mysql -u root -p

-- 创建数据库
CREATE DATABASE flaskblog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户（可选）
CREATE USER 'flaskuser'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON flaskblog.* TO 'flaskuser'@'localhost';
FLUSH PRIVILEGES;
```

### 3. 配置环境变量

#### 复制环境变量模板
```bash
cp .env.example .env
```

#### 编辑 .env 文件
```bash
# 数据库连接信息
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DATABASE=flaskblog

# 或者使用完整的连接字符串
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/flaskblog
```

### 4. 一键安装
```bash
python setup.py
```

## ⚙️ 数据库配置详解

### 配置文件结构

**config.py** 中的MySQL配置：
```python
# MySQL数据库配置
MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'password'
MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
MYSQL_PORT = os.environ.get('MYSQL_PORT') or '3306'
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'flaskblog'

# 构建MySQL连接URI
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
```

### 环境变量优先级
1. `DATABASE_URL`（完整连接字符串）- 最高优先级
2. `MYSQL_*` 系列变量 - 次优先级
3. 默认值 - 最低优先级

## 🔧 常见问题解决

### 连接失败问题

#### 1. MySQL服务未启动
```bash
# Windows
net start mysql

# Linux
sudo systemctl start mysql
```

#### 2. 权限问题
```sql
-- 给用户授权
GRANT ALL PRIVILEGES ON flaskblog.* TO 'youruser'@'localhost';
FLUSH PRIVILEGES;
```

#### 3. 端口问题
检查MySQL端口：
```bash
netstat -an | grep 3306
```

### 数据库连接测试

#### 使用脚本测试
```bash
python init_mysql.py
```

#### 使用Python测试
```python
import pymysql
from config import Config

connection = pymysql.connect(
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    database=Config.MYSQL_DATABASE,
    charset='utf8mb4'
)
print("连接成功！")
connection.close()
```

## 🚀 快速启动命令汇总

```bash
# 1. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 2. 安装依赖
pip install -r requirements.txt

# 3. 初始化MySQL数据库
python init_mysql.py

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填写MySQL连接信息

# 5. 一键安装
python setup.py

# 6. 启动应用
python run.py
```

## 📊 数据库表结构

### 主要数据表

#### users 表
- id (主键)
- username (用户名)
- email (邮箱)
- password_hash (密码哈希)
- avatar_url (头像)
- bio (简介)
- created_at (创建时间)
- updated_at (更新时间)
- is_admin (管理员标志)

#### posts 表
- id (主键)
- title (标题)
- slug (URL别名)
- content (内容)
- summary (摘要)
- featured_image (特色图片)
- is_published (发布状态)
- view_count (浏览次数)
- created_at (创建时间)
- updated_at (更新时间)
- published_at (发布时间)
- user_id (外键，关联用户)

#### comments 表
- id (主键)
- content (内容)
- is_approved (审核状态)
- created_at (创建时间)
- user_id (外键，关联用户)
- post_id (外键，关联文章)
- parent_id (自关联，回复评论)

#### tags 表
- id (主键)
- name (标签名)
- slug (URL别名)
- color (颜色)

#### post_tags 表
- post_id (外键)
- tag_id (外键)



## 📞 技术支持

如有MySQL配置问题，请：
1. 检查MySQL服务状态
2. 验证用户名密码
3. 确认防火墙设置
4. 查看错误日志
5. 联系项目维护者

---

**现在项目已完全支持MySQL数据库！** 🎉