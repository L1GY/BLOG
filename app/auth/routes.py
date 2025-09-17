from flask import render_template, redirect, url_for, flash, request  # 导入Flask核心功能
from flask_login import login_user, logout_user, current_user, login_required  # 导入用户认证功能
from app.auth import bp  # 导入认证蓝图
from app import db  # 导入数据库实例
from app.models.user import User  # 导入用户模型
from app.auth.forms import LoginForm, RegistrationForm  # 导入表单类

@bp.route('/login', methods=['GET', 'POST'])  # 定义登录路由，支持GET和POST方法
def login():
    """
    用户登录视图函数
    GET: 显示登录表单
    POST: 处理登录逻辑
    """
    
    # 如果用户已经登录，重定向到首页
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # 创建登录表单实例
    form = LoginForm()
    
    # 检查表单是否提交并验证通过
    if form.validate_on_submit():
        # 根据用户名查询用户
        user = User.query.filter_by(username=form.username.data).first()
        
        # 检查用户是否存在且密码正确
        if user and user.check_password(form.password.data):
            # 登录用户，remember_me决定是否记住登录状态
            login_user(user, remember=form.remember_me.data)
            
            # 获取下一个页面URL（如果有的话）
            next_page = request.args.get('next')
            
            # 检查next参数是否安全（防止重定向攻击）
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')  # 默认重定向到首页
                
            return redirect(next_page)  # 重定向到指定页面
        
        # 登录失败，显示错误消息
        flash('用户名或密码错误')
    
    # 渲染登录页面模板
    return render_template('auth/login.html', title='登录', form=form)

@bp.route('/register', methods=['GET', 'POST'])  # 定义注册路由
def register():
    """
    用户注册视图函数
    GET: 显示注册表单
    POST: 处理注册逻辑
    """
    
    # 如果用户已登录，重定向到首页
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # 创建注册表单实例
    form = RegistrationForm()
    
    # 检查表单是否提交并验证通过
    if form.validate_on_submit():
        # 创建新用户实例
        user = User(username=form.username.data, email=form.email.data)
        
        # 设置密码（自动加密）
        user.set_password(form.password.data)
        
        # 添加到数据库会话
        db.session.add(user)
        
        # 提交到数据库
        db.session.commit()
        
        # 显示成功消息
        flash('注册成功，请登录')
        
        # 重定向到登录页面
        return redirect(url_for('auth.login'))
    
    # 渲染注册页面模板
    return render_template('auth/register.html', title='注册', form=form)

@bp.route('/logout')  # 定义登出路由
def logout():
    """
    用户登出视图函数
    清除用户会话并重定向到首页
    """
    logout_user()  # 登出当前用户
    flash('您已成功退出登录')  # 显示成功消息
    return redirect(url_for('main.index'))  # 重定向到首页

@bp.route('/profile')  # 定义个人资料路由
@login_required  # 要求用户必须登录才能访问
def profile():
    """
    个人资料页面
    只有登录用户才能访问
    """
    return render_template('auth/profile.html', title='个人资料')