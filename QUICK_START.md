# Flask博客网站 - 快速启动指南

## 🚀 快速开始

### 1. 环境准备
确保已安装：
- Python 3.8+
- MySQL 5.7+ 或 MariaDB
- Git

### 2. 安装步骤

```bash
# 克隆项目
git clone <your-repo-url>
cd flask-blog

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 复制配置文件
cp .env.example .env

# 编辑配置文件
# 修改 .env 文件中的数据库连接信息

# 一键安装
python setup.py
```

### 3. 手动安装（可选）

如果自动安装失败，可以手动执行：

```bash
# 安装依赖
pip install -r requirements.txt

# 初始化数据库
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 启动应用
python run.py
```

### 4. 默认账户

安装完成后，系统会自动创建管理员账户：
- 用户名：`admin`
- 密码：`admin123`
- 邮箱：`admin@example.com`

**⚠️ 重要：首次登录后请立即修改密码！**

### 5. 访问地址

- 网站首页：http://localhost:5000
- 管理后台：http://localhost:5000/admin
- 登录页面：http://localhost:5000/auth/login
- 注册页面：http://localhost:5000/auth/register

### 6. 功能特性

#### ✅ 已实现功能
- [x] 用户注册/登录
- [x] 文章发布/编辑/删除
- [x] 文章分类和标签
- [x] 文章搜索
- [x] 评论系统
- [x] 用户个人中心
- [x] 响应式设计
- [x] 管理后台

#### 🔄 待开发功能
- [ ] 富文本编辑器
- [ ] 文件上传
- [ ] 邮件通知
- [ ] 社交登录
- [ ] 文章点赞
- [ ] 站内消息
- [ ] 高级搜索
- [ ] 数据备份

### 7. 常用命令

```bash
# 启动开发服务器
python run.py

# 进入Flask shell
flask shell

# 创建数据库迁移
flask db migrate -m "描述"

# 应用数据库迁移
flask db upgrade

# 回滚数据库迁移
flask db downgrade

# 运行测试
python -m pytest
```

### 8. 项目结构

```
flask-blog/
├── app/                    # 应用主目录
│   ├── main/              # 主页蓝图
│   ├── auth/              # 认证蓝图
│   ├── post/              # 文章蓝图
│   ├── admin/             # 管理后台
│   ├── models/            # 数据模型
│   ├── templates/         # 模板文件
│   └── static/            # 静态文件
├── migrations/             # 数据库迁移
├── venv/                  # 虚拟环境
├── requirements.txt       # 依赖列表
├── run.py                 # 启动脚本
├── setup.py              # 安装脚本
├── .env                  # 配置文件
└── README.md             # 项目说明
```

### 9. 遇到问题？

#### ❗ 常见问题

**1. MySQL连接失败**
- 检查MySQL服务是否启动
- 确认用户名密码正确
- 检查防火墙设置

**2. 端口被占用**
- 修改 `run.py` 中的端口号
- 或者关闭占用5000端口的程序

**3. 权限问题**
- Windows: 以管理员身份运行
- Linux/Mac: 使用 `sudo` 或检查文件权限

**4. 依赖安装失败**
- 更新pip: `pip install --upgrade pip`
- 安装编译工具: Visual Studio Build Tools
- 使用国内镜像: `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

### 10. 技术支持

如有问题，请：
1. 查看 `README.md` 详细文档
2. 检查日志文件
3. 提交Issue到项目仓库
4. 联系项目维护者

---

**祝你使用愉快！** 🎉