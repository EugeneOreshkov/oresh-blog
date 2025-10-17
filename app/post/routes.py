from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from app.models import Post
from app.post.forms import PostForm
from app import db
from . import bp

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """New post page."""    
    
    post_form = PostForm()  
    if post_form.validate_on_submit():
        post = Post(
            title=post_form.title.data,
            body=post_form.body.data,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Ваш пост опубликован!')
        return redirect(url_for('index'))    

    return render_template(
        'create_post.html',        
        form=post_form,
        title='Создать пост'
    )