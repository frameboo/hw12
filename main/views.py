import logging

from flask import Blueprint, render_template, request, current_app
from classes.data_manager import DataManager
from classes.exceptions import DataSourceBrokenException

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')

logger = logging.getLogger("basic")


@main_blueprint.route('/')
def main_page():
    return render_template("index.html")


@main_blueprint.route('/search/')
def search_page():
    path = current_app.config.get("POST_PATH")
    data_manager = DataManager(path)

    s = request.values.get("s", None)

    logger.info(f"Выполняется поиск: {s}")

    if s is None or s == "":
        posts = data_manager.get_all()
    else:
        posts = data_manager.search(s)
    return render_template("post_list.html", posts=posts, s=s)


@main_blueprint.errorhandler(DataSourceBrokenException)
def data_source_broken_error(e):
    return "файл с данными повержден"
