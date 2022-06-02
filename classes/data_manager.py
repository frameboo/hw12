import json

from classes.exceptions import DataSourceBrokenException


class DataManager:

    def __init__(self, path):
        self.path = path  # Путь к файлу с данными

    def load_data(self):
        """ Загрузка данных и проверка файла"""
        try:
            with open(self.path, encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):

            raise DataSourceBrokenException("Файл с данными поврежден")

        return data

    def save_data(self, data):
        """Сохранение данных"""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    def get_all(self):
        data = self.load_data()
        return data

    def search(self, substring):
        """Функция поиска по постам"""
        posts = self.load_data()
        substring = substring.lower()
        matching_post = [post for post in posts if substring in post["content"].lower()]
        return matching_post

    def add(self, post):
        """Добавление нового поста в json"""
        posts = self.load_data()
        posts.append(post)
        self.save_data(posts)
