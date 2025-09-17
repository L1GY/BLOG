from flask import render_template, request, current_app
from app.main import bp
from app.models.post import Post, Tag
from app.models.user import User
from sqlalchemy import desc

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(is_published=True).order_by(desc(Post.published_at)).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    
    recent_posts = Post.query.filter_by(is_published=True).order_by(desc(Post.created_at)).limit(5).all()
    popular_tags = Tag.query.limit(10).all()
    
    return render_template('main/index.html', 
                         posts=posts, 
                         recent_posts=recent_posts, 
                         popular_tags=popular_tags)

@bp.route('/about')
def about():
    return render_template('main/about.html')

@bp.route('/contact')
def contact():
    return render_template('main/contact.html')

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        posts = Post.query.filter(
            Post.title.contains(query) | Post.content.contains(query)
        ).filter_by(is_published=True).order_by(desc(Post.created_at)).all()
    else:
        posts = []
    
    return render_template('main/search.html', posts=posts, query=query)