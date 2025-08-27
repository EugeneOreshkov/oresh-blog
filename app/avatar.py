import hashlib
from flask import Blueprint, Response, request
import pydenticon
bp = Blueprint("avatar_bp", __name__)

FOREGROUND = [
    "rgb(57,255,20)", # Neon Green
    "rgb(0,255,255)", # Neon Cyan / Aqua
    "rgb(255,20,147)", # Deep Pink
    "rgb(255,255,0)", # Acid Yellow
    "rgb(255,0,255)", # Magenta / Fuchsia
    "rgb(255,69,0)", # Neon Orange-Red
    "rgb(0,191,255)" # Neon Sky Blue
]

BACKGROUND = "rgb(0,0,0)" # Black

generator = pydenticon.Generator(
    12,
    12,
    digest=hashlib.sha1,
    foreground = FOREGROUND,
    background = BACKGROUND
)

@bp.get("/avatar")
def avatar():
    seed = request.args.get("seed")
    size = max(24, min(int(request.args.get("size")), 512))
    image = generator.generate(seed, size, size, output_format="png")
    return Response(image, mimetype="image/png")




