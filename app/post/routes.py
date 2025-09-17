from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.post import bp
from app import db
from app.models.post import Post, Comment, Tag
from app.post.forms import PostForm, CommentForm
from sqlalchemy import desc
import re

def slugify(text):
    """将标题转换为URL友好的slug"""
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    text = re.sub(r'[-\s]+', '-', text)
    return text

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    tag_slug = request.args.get('tag')
    
    query = Post.query.filter_by(is_published=True)
    
    if tag_slug:
        tag = Tag.query.filter_by(slug=tag_slug).first_or_404()
        query = query.filter(Post.tags.contains(tag))
    
    posts = query.order_by(desc(Post.published_at)).paginate(
        page=page, per_page=10, error_out=False)
    
    tags = Tag.query.limit(20).all()
    
    return render_template('post/index.html', posts=posts, tags=tags, tag_slug=tag_slug)

@bp.route('/<slug>')
def detail(slug):
    post = Post.query.filter_by(slug=slug, is_published=True).first_or_404()
    post.increment_view()
    
    form = CommentForm()
    comments = Comment.query.filter_by(post_id=post.id, is_approved=True).order_by(Comment.created_at.desc())
    
    return render_template('post/detail.html', post=post, form=form, comments=comments)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    
    if form.validate_on_submit():
        slug = slugify(form.title.data)
        
        # 确保slug唯一
        counter = 1
        original_slug = slug
        while Post.query.filter_by(slug=slug).first():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        post = Post(
            title=form.title.data,
            slug=slug,
            content=form.content.data,
            summary=form.summary.data,
            featured_image=form.featured_image.data,
            is_published=form.is_published.data,
            user_id=current_user.id
        )
        
        # 处理标签
        tag_names = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name, slug=slugify(tag_name))
                db.session.add(tag)
            post.tags.append(tag)
        
        if form.is_published.data:
            post.published_at = datetime.utcnow()
        
        db.session.add(post)
        db.session.commit()
        
        flash('文章创建成功！')
        return redirect(url_for('post.detail', slug=post.slug))
    
    return render_template('post/create.html', form=form)

@bp.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    
    if post.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    form = PostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.summary = form.summary.data
        post.featured_image = form.featured_image.data
        post.is_published = form.is_published.data
        
        if form.is_published.data and not post.published_at:
            post.published_at = datetime.utcnow()
        
        # 更新标签
        post.tags.clear()
        tag_names = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name, slug=slugify(tag_name))
                db.session.add(tag)
            post.tags.append(tag)
        
        db.session.commit()
        flash('文章更新成功！')
        return redirect(url_for('post.detail', slug=post.slug))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.summary.data = post.summary
        form.featured_image.data = post.featured_image
        form.is_published.data = post.is_published
        form.tags.data = ', '.join([tag.name for tag in post.tags])
    
    return render_template('post/edit.html', form=form, post=post)

@bp.route('/<slug>/delete', methods=['POST'])
@login_required
def delete(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    
    if post.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    db.session.delete(post)
    db.session.commit()
    
    flash('文章已删除！')
    return redirect(url_for('main.index'))

@bp.route('/<slug>/comment', methods=['POST'])
@login_required
def add_comment(slug):
    post = Post.query.filter_by(slug=slug, is_published=True).first_or_404()
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            user_id=current_user.id,
            post_id=post.id,
            parent_id=form.parent_id.data if form.parent_id.data else None
        )
        db.session.add(comment)
        db.session.commit()
        
        flash('评论发布成功！')
    
    return redirect(url_for('post.detail', slug=slug))