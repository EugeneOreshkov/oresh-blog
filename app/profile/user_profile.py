import base64
from datetime import datetime
from io import BytesIO
import os
from PIL import Image as PILImage

import sqlalchemy as sa
from flask import current_app, render_template, redirect, flash, url_for, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app import db
from app.profile.forms import EditProfileForm
from app.user.follow import EmptyForm
from app.models import User
from app.service.pagination import get_user_posts_with_pagination
from . import bp

@bp.route('/user/<username>')
@login_required
def user(username):
    stmt = sa.select(User).where(User.username == username)
    user = db.first_or_404(stmt) 

    form = EmptyForm()

    page = request.args.get('page', 1, type=int)    
    posts = get_user_posts_with_pagination(page)
    
    next_url = url_for('profile.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    
    prev_url = url_for('profile.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    
    return render_template(
        'user_profile.html',
        title='Пользователь',
        user=user,
        posts=posts.items,
        prev_url=prev_url,
        next_url=next_url,
        form=form
    )

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():        
        changed_avatar = False
        changed_profile = False              
        
        # --- Priority: Cropped Avatar ---
        cropped_data = form.cropped_avatar_data.data
        if cropped_data and cropped_data.startswith('data:image'):
            try:
                # Remove data:image/png;base64, prefix
                header, encoded = cropped_data.split(',', 1)
                image_data = base64.b64decode(encoded)

                # Open with PIL and ensure it's RGB
                image = PILImage.open(BytesIO(image_data))
                if image.mode != 'RGB':
                    image.convert('RGB')
                
                # Resize to 256x256 for consistency
                image = image.resize((256,256), PILImage.Resampling.LANCZOS)

                filename = secure_filename(f"user{current_user.get_id()}.png")

                upload_dir = current_app.config["UPLOAD_FOLDER"]   
                os.makedirs(upload_dir, exist_ok=True)

                path = os.path.join(upload_dir, filename)

            except Exception as e:
               flash(f'Ошибка при сохранении аватара: {str(e)}', 'error')

        # --- Fallback: Regular file upload ---                   
        elif file:  
            file= form.avatar.data

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
        if changed_avatar and changed_profile: flash('Аватар и профиль обновлены.')
        elif changed_avatar: flash('Аватар обновлен.')
        elif  changed_profile: flash('Профиль обновлен.')
        
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
