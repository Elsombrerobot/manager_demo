from functools import wraps
import random
import secrets
from PIL import Image
from pathlib import Path
from flask import current_app, flash, redirect, request, url_for
from PIL import Image, ImageColor, ImageDraw, ImageFont
from flask_login import current_user

from manager_demo import bcrypt
from manager_demo.models import User

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_ext = Path(form_picture.filename).suffix
    picture_fn = random_hex + f_ext
    picture_path = Path(current_app.root_path) / "static" / "profile_pics" / picture_fn
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(str(picture_path))
    return picture_fn
    
def delete_picture(picture_fn):
    picture_path = Path(current_app.root_path) / "static" / "profile_pics" / picture_fn
    Path(picture_path).unlink()
    return picture_path

def generate_profile_picture(initials, size=125):
    font_size=50
    font = Path(current_app.root_path) / "static" / "JosefinSans-Bold.ttf"
    colors = [name for name, _ in ImageColor.colormap.items()]
    colors.remove("white")
    color = random.choice(colors)
    img = Image.new('RGB', (size, size), color = color)
    font_type = ImageFont.truetype(str(font),font_size)
    fw, fh = font_type.getsize(initials.upper())
    center = (size/2 - fw/2, size/2 - fh/2)
    draw = ImageDraw.Draw(img)
    draw.text(center, initials.upper(), font=font_type, fill="white")
    random_hex = secrets.token_hex(8)
    picture_fn = f'{random_hex}.jpeg'
    picture_path = Path(current_app.root_path) / "static" / "profile_pics" / picture_fn
    img.save(str(picture_path), quality=100)
    return picture_fn

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def generate_password(first_name, last_name):
    unhashed_password = first_name + last_name[0]
    return hash_password(unhashed_password)

def generate_email(first_name, last_name):
    return f"{first_name.lower()}{last_name[0].lower()}@manager-demo.com"

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if not current_user.is_admin():
            flash('Please connect as admin to access this page.', 'danger')
            return redirect(url_for("users.login", next=url_for(request.endpoint, **kws)))            
        return f(*args, **kws)            
    return decorated_function



