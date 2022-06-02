import os
import random
from loader.exceptions import PicturesFormatNotSupportedError, PicturesNotUploadedError, OutOfFreeNamesError


class UploadManager:

    def get_free_filename(self, folder, file_type):
        """Получения нового имени для загружаемого файла"""
        attemps = 0
        LIMIT_OF_ATTEMPS = 1000000

        while True:
            pic_name = random.randint(0, 1000000)
            filename_to_save = f"{pic_name}.{file_type}"
            os_path = os.path.join(folder, filename_to_save)
            is_filename_occupied = os.path.exists(os_path)

            if not is_filename_occupied:
                return filename_to_save

            attemps += 1

            if attemps > LIMIT_OF_ATTEMPS:
                raise OutOfFreeNamesError("No free names to save images")

    def if_file_type_valid(self, file_type):
        """Проверка расширения файла"""
        if file_type.lower() in ["jpeg", "jpg", "gif", "png", "webp"]:
            return True
        return False

    def save_with_random_name(self, picture):

        # Получаем данные с картинки
        filename = picture.filename
        file_type = filename.split(".")[-1]

        # Проверяем валидность картинки
        if not self.if_file_type_valid(file_type):
            raise PicturesFormatNotSupportedError(f"Формат {file_type} не поддерживается")

        # Получаем свободное имя
        folder = os.path.join(".", "uploads", "images")
        filename_to_save = self.get_free_filename(folder, file_type)

        # Сохраняем под новым именем
        try:
            picture.save(os.path.join(folder, filename_to_save))
        except FileNotFoundError:
            raise PicturesNotUploadedError(f"{folder, filename_to_save}")

        return filename_to_save
