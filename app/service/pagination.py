from flask_login import current_user
from app import app, db
from app.models import Post

def get_following_posts_with_pagination(page):    
    posts = db.paginate(
        current_user.following_posts(),
        page = page,
        per_page=app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    return posts

def get_all_posts_with_pagination(page):    
    posts = db.paginate(
        Post.query.order_by(Post.timestamp.desc()),
        page = page,
        per_page=app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    return posts

def get_user_posts_with_pagination(page):
    query = current_user.posts.select().order_by(Post.timestamp.desc())
    posts = db.paginate(
        query, page=page,
        per_page=app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    return posts
    