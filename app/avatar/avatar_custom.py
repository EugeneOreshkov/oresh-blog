import io
import os
from PIL import Image as PILImage

from flask import abort, current_app, request, send_file

from . import bp

@bp.route('/custom/<int:user_id>')
def custom_avatar(user_id):
    """Serve custom avatar for user"""
    avatar_path = os.path.join(current_app.config.get('UPLOAD_FOLDER', ''), f'user{user_id}.png')

    if not os.path.exists(avatar_path):
        abort(404)

    size = request.args.get('size', type=int, default=128)
    size = max(24, min(size, 512)) # Limit size between 24 and 512

    # If default:
    if size == 128:
        return send_file(avatar_path, mimetype='image/png')
    
    try:
        with PILImage.open(avatar_path) as image:  
                  
            if image.mode in ('RGBA', 'LA'):
                background = PILImage.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'RGBA':
                    background.paste(image, mask=image.split()[-1])
                else:
                    background.paste(image)
                image = background
            if image.mode != "RGB":
                image = image.convert("RGB")

            # Resize image
            img_resized = image.resize((size,size), PILImage.Resampling.LANCZOS)

            # Save to bytes
            img_bytes = io.BytesIO()
            img_resized.save(img_bytes, format='PNG')
            img_bytes.seek(0)

        return send_file(img_bytes, mimetype='image/png')
    
    except Exception:
        # If resizing fails, return original file
        return send_file(avatar_path, mimetype='image/png')   
    