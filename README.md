# Flask 博客网站

一个使用 Flask 框架和 MySQL 数据库构建的博客网站。

## 项目结构

```
├── app/
│   ├── __init__.py          # 应用工厂
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py          # 用户模型
│   │   └── post.py          # 文章、评论、标签模型
│   ├── routes/              # 路由蓝图
│   │   ├── main/            # 主页面路由
│   │   ├── auth/            # 认证路由
│   │   └── post/            # 文章管理路由
│   ├── templates/           # HTML模板
│   │   ├── base.html        # 基础模板
│   │   ├── main/            # 主页面模板
│   │   ├── auth/            # 认证模板
│   │   └── post/            # 文章模板
│   ├── static/              # 静态文件
│   │   ├── css/             # 样式文件
│   │   ├── js/              # JavaScript文件
│   │   └── images/          # 图片文件
│   └── utils/               # 工具函数
├── migrations/              # 数据库迁移文件
├── config.py                # 配置文件
├── run.py                   # 应用入口
├── requirements.txt         # 依赖列表
└── .env                     # 环境变量
```

## 功能特性

- ✅ 用户注册与登录
- ✅ 文章发布、编辑、删除
- ✅ 文章分类与标签
- ✅ 评论系统
- ✅ 搜索功能
- ✅ 响应式设计
- ✅ 分页功能
- ✅ 用户个人资料

## 技术栈

- **后端**: Python Flask
- **数据库**: MySQL
- **ORM**: SQLAlchemy
- **迁移工具**: Flask-Migrate
- **认证**: Flask-Login
- **表单**: Flask-WTF
- **前端**: Bootstrap 5
- **图标**: Font Awesome

## 安装与运行

### 1. 环境准备

确保已安装：
- Python 3.7+
- MySQL 5.7+
- pip (Python包管理器)

### 2. 克隆项目

```bash
git clone [项目地址]
cd blog-website
```

### 3. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 配置数据库

#### 创建MySQL数据库
```sql
CREATE DATABASE blog_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 配置环境变量
编辑 `.env` 文件：
```
DATABASE_URL=mysql+pymysql://username:password@localhost/blog_db
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True
```

### 6. 初始化数据库

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 7. 运行应用

```bash
python run.py
```

访问: http://localhost:5000

## 使用说明

### 管理员功能

1. 注册第一个用户
2. 在数据库中设置该用户为管理员：
   ```sql
   UPDATE users SET is_admin = 1 WHERE id = 1;
   ```

### 创建文章

1. 注册并登录账户
2. 点击导航栏中的"写文章"
3. 填写文章标题、内容、标签等信息
4. 选择是否立即发布
5. 点击保存文章

### 文章管理

- **查看文章**: 点击文章标题
- **编辑文章**: 文章作者或管理员可以编辑
- **删除文章**: 文章作者或管理员可以删除

### 评论系统

- 登录用户可以对文章发表评论
- 支持回复评论
- 管理员可以管理评论

## 开发指南

### 添加新功能

1. 创建新的模型（如需要）
2. 创建新的路由蓝图
3. 创建对应的模板文件
4. 更新导航菜单

### 数据库迁移

```bash
# 创建新的迁移
flask db migrate -m "Description of changes"

# 应用迁移
flask db upgrade

# 回滚迁移
flask db downgrade
```

### 调试模式

在开发环境中，应用会自动重载：
```bash
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows
```

## 部署

### 生产环境配置

1. 设置环境变量：
   ```
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```

2. 使用WSGI服务器（如Gunicorn）：
   ```bash
   pip install gunicorn
   gunicorn run:app
   ```

3. 配置反向代理（如Nginx）

### Docker部署

（可选）创建Docker配置文件进行容器化部署。

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 支持与联系

如有问题，请通过以下方式联系：
- 邮箱: contact@myblog.com
- 提交 Issue: [项目Issues页面]