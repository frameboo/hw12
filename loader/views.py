import logging

from flask import Blueprint, render_template, request, current_app
from classes.data_manager import DataManager
from .exceptions import OutOfFreeNamesError, PicturesFormatNotSupportedError, PicturesNotUploadedError
from .upload_manager import UploadManager

loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='templates')

logger = logging.getLogger("basic")

@loader_blueprint.route('/post', methods=['Get'])
def page_form():
    return render_template("post_form.html")


@loader_blueprint.route('/post', methods=['POST'])
def page_create_posts():

    path = current_app.config.get("POST_PATH")
    data_manager = DataManager(path)
    upload_manager = UploadManager()

    # Получаем данные
    picture = request.files.get("picture", None)
    content = request.values.get("content", "")

    # Сохраняем картинку с помощью класса UploadManager
    filename_saved = upload_manager.save_with_random_name(picture)

    # Получаем путь для браузера клинта
    web_path = f"/uploads/images/{filename_saved}"

    # Создаем данные для записи в файл
    post = {"pic": web_path, "content": content}

    # Добавляем данные и файл
    data_manager.add(post)

    return render_template("post_uploaded.html", pic=web_path, content=content)


@loader_blueprint.errorhandler(OutOfFreeNamesError)
def error_out_of_free_name(e):
    return "Упс, закончились свободные имена для загрузки картинок"


@loader_blueprint.errorhandler(PicturesFormatNotSupportedError)
def error_format_not_supported(e):
    logger.info("Попытка загрузки не поддерживаемого формата картинки")
    return "Формат картинки не поддерживается"


@loader_blueprint.errorhandler(PicturesNotUploadedError)
def error_file_not_uploaded(e):
    logger.error("ошибка загрузки файла")
    return "Не удалось загрузить файл"

