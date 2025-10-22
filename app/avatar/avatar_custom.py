import os

from flask import abort, current_app, send_file

from . import bp

@bp.route('/avatar/<current_user.id>')
def custom_avatar(current_user):
    """Serve custom avatar for user"""
    avatar_path = os.path.join(current_app.config.get('UPLOAD_FOLDER', ''), f'user{current_user.id}.png')

    if (os.path.exists()):
        return send_file(avatar_path, mimetype='image/png')
    else:
        abort(404)
    