from datetime import datetime
import os

import sqlalchemy as sa
from flask import current_app, render_template, redirect, flash, url_for, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app import db
from app.profile.forms import EditProfileForm
from app.user.follow import EmptyForm
from app.models import User, Post
from . import bp

@bp.route('/user/<username>')
@login_required
def user(username):
    stmt = sa.select(User).where(User.username == username)
    user = db.first_or_404(stmt)    
    form = EmptyForm()
    posts = Post.get_user_posts(user.id)
    return render_template('user_profile.html', title='Пользователь', user=user, posts=posts, form=form)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():        
        changed_avatar = False
        changed_profile = False              
        # --- Avatar ---
        file= form.avatar.data               
        if file:    
            ext = os.path.splitext(file.filename)[1]        
            filename = secure_filename(f"user{current_user.get_id()}{ext}")
            upload_dir = current_app.config["UPLOAD_FOLDER"]   
            os.makedirs(upload_dir, exist_ok=True)     
            path = os.path.join(upload_dir, filename)            
            file.save(path)
            changed_avatar = True
        
        # --- Text fields ---
        if (form.username.data != current_user.username) or (form.about.data != current_user.about):
            current_user.username = form.username.data
            current_user.about = form.about.data
            changed_profile = True

        if changed_profile: db.session.commit()
        
        # --- Flash messages ---
        if changed_avatar and changed_profile: flash('Your avatar and profile changes have been saved.')
        elif changed_avatar: flash('Your avatar changes have been saved.')
        elif  changed_profile: flash('Your profile changes have been saved.')
        
        return redirect(url_for('profile.edit_profile'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about.data = current_user.about
    return render_template('edit_profile.html', title='Редактировать профиль', form=form, current_route=request.endpoint)

@bp.before_request
def before_request():
    # Update last_login timestamp for logged-in users (shown in profile column)
    if current_user.is_authenticated:
        current_user.last_login = datetime.utcnow()
        db.session.commit()
