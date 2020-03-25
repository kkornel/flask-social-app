import os
import secrets

from PIL import Image
from flask import url_for, current_app


def generate_link(link):
    htpplink = link
    if not link.startswith('http'):
        htpplink = 'http://' + link
    return f'<a class="link" target="_blank" href="{htpplink}">{link}</a>'


def generate_hashtag_link(tag):
    # Free to configure the URL the way adapted your project
    url = "/tags/{}/".format(tag)
    return f'<a class="hashtag" href="{url}">#{tag}</a>'


def save_image(form_picture, folder_path, picture_size):
    random_hex = secrets.token_hex(8)
    # splitext returns filename and extension, but we don't need
    # filename so we are using _
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_file_name = random_hex + file_extension
    picture_path = os.path.join(current_app.root_path, folder_path,
                                picture_file_name)
    output_size = picture_size
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    return picture_file_name


def delete_image(folder_name, file_name):
    path = os.path.join(current_app.root_path, folder_name, file_name)
    current_app.logger.debug(f'Trying to remove image: {path}')
    if os.path.exists(path):
        os.remove(path)
        current_app.logger.debug(f'Filed removed.')
        return True
    current_app.logger.debug(f'Deletion failed.')
    return False