import csv
import os
from loguru import logger
from models import Base
from exceptions import CSVDirectoryError, ClassNotExists
from scos_dictionaries import ActionsList
from models import get_unit
from reader import Reader


class CSVReader(Reader):

    def __init__(self, file_dir: str):
        self.csv_file_path = file_dir

    def __check_csv_dir(self, create=False) -> None:
        """Проверяем наличие директории для csv файлов

        :param create: создать директории при отсутствии
        """
        if not os.path.exists(self.csv_file_path):
            logger.debug(f"Директория {self.csv_file_path} для csv файлов не существует")
            if create:
                self.__create_csv_dir()
            else:
                raise CSVDirectoryError("Директория для CSV файлов не существует и не создана")

    def __create_csv_dir(self) -> None:
        """Создание директории для csv файлов"""
        try:
            os.mkdir(self.csv_file_path)
            logger.info(f'Создана директория для csv файлов')
        except OSError as ex:
            logger.error(f'Ошибка создания директории для csv файлов {self.csv_file_path}: {ex}')
        else:
            logger.info(f'Создана директория для csv файлов: {self.csv_file_path}')

    def __read_files(self) -> dict[ActionsList, list[Base]]:
        """Чтение всех файлов в директории по типам"""
        units_list: dict = {x: [] for x in ActionsList}
        for file in os.listdir(self.csv_file_path):
            action = file.split('_')[0]
            if action in ActionsList.list_values():
                units_list[ActionsList(action)] += self.__read_file(self.csv_file_path + '/' + file)
            logger.debug(f'прочитан файл {file}')

        logger.info(f'Чтение файлов завершено, для добавления: {len(units_list[ActionsList.ADD])}, '
                    f'для изменения: {len(units_list[ActionsList.UPD])}, '
                    f'для удаления {len(units_list[ActionsList.DEL])}')

        return units_list

    @staticmethod
    def __read_file(file: str) -> list[Base]:
        """Читает файл в формате csv"""
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

    def __clear_scv_directory(self):
        """Очистка директории с csv файлами"""
        for file in os.scandir(self.csv_file_path):
            os.remove(file.path)

    def get_new_data(self) -> dict[ActionsList, list[Base]]:
        self.__check_csv_dir(create=True)
        units_list = self.__read_files()
        self.__clear_scv_directory()
        return units_list


if __name__ == '__main__':
    pass
