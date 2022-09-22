import csv
import os
from loguru import logger
from local_base import LocalBase
from exceptions import CSVDirectoryError, ClassNotExists
from scos_dictionaries import ActionsList
from models import get_unit


class CSVReader:

    def __init__(self, file_dir: str):
        self.csv_file_path = file_dir

    def check_csv_dir(self, create=False) -> None:
        """Проверяем наличие директории для csv файлов

        :param create: создать директории при отсутствии
        """
        if not os.path.exists(self.csv_file_path):
            logger.debug(f"Директория {self.csv_file_path} для csv файлов не существует")
            if create:
                logger.debug(f"Директорию требуется создать")
            else:
                raise CSVDirectoryError("Директория для CSV файлов не существует и не создана")

    def __create_csv_dir(self):
        """Создание директории для csv файлов"""
        try:
            os.mkdir(self.csv_file_path)
            logger.info()
        except OSError as ex:
            logger.error(f'Ошибка создания директории для csv файлов {self.csv_file_path}: {ex}')
        else:
            logger.info(f'Создана директория для csv файлов: {self.csv_file_path}')

    def read_files(self) -> dict[ActionsList, list[LocalBase.Base]]:
        """Чтение всех файлов в директории по типам, a_ добавление, u_ обновление, d_ удаление"""
        units_list: dict = {ActionsList.ADD: [], ActionsList.UPD: [], ActionsList.DEL: []}
        for file in os.listdir(self.csv_file_path):
            if file.startswith('a_'):
                action = ActionsList.ADD
            elif file.startswith('u_'):
                action = ActionsList.UPD
            elif file.startswith('d_'):
                action = ActionsList.DEL
            else:
                action = ActionsList.NOP

            units_list[action] += self.__read_file(self.csv_file_path + '/' + file)
            logger.debug(f'прочитан файл {file}')

        return units_list

    @staticmethod
    def __read_file(file: str) -> list[LocalBase.Base]:
        units_list = []
        try:
            file_name = os.path.basename(file)
            # Убираем расширение и префикс файла
            unit_name = os.path.splitext(file_name)[0][2:]

            with open(file) as open_file:
                units_data = csv.DictReader(open_file, dialect='excel')
                for unit_data in units_data:
                    unit = get_unit(unit_name, **unit_data)
                    units_list.append(unit)

        except ClassNotExists:
            logger.error(f'Файл {file} имеет не верное название, название файла должно соответствовать названию класса')
        except Exception as er:
            logger.error(f'Не удалось cформировать данные из файла {file}: {er}')
        finally:
            return units_list

    def clear_scv_directory(self):
        """Очистка директории с csv файлами"""
        for file in os.scandir(self.csv_file_path):
            os.remove(file.path)


if __name__ == '__main__':
    pass
