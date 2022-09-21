import csv
import os
from loguru import logger
from local_base import LocalBase
from exceptions import ClassNotExists


class CSVReader:
    base = LocalBase()
    csv_file_path = 'csv_files'

    def check_csv_dir(self, create=False) -> bool:
        """Проверяем наличие директории для csv файлов

        :param create: создать директории при отсутствии
        """
        if not os.path.exists(self.csv_file_path):
            if create:
                self.__create_csv_dir()
            else:
                return False
        else:
            return True

    def __create_csv_dir(self):
        """Создание директории для csv файлов"""
        try:
            os.mkdir(self.csv_file_path)
        except OSError as ex:
            logger.error(f'Ошибка создания директории для csv файлов {self.csv_file_path}: {ex}')
        else:
            logger.info(f'Создана директория для csv файлов: {self.csv_file_path}')

    def read_files(self):
        """Чтение всех файлов в директории по типам, a_ добавление, u_ обновление, d_ удаление"""
        for file in os.listdir(self.csv_file_path):
            if file.startswith('a_'):
                self.base.add_to_base(self.__read_file(self.csv_file_path + '/' + file))
        for file in os.listdir(self.csv_file_path):
            if file.startswith('u_'):
                self.base.update_in_base(self.__read_file(self.csv_file_path + '/' + file))
        for file in os.listdir(self.csv_file_path):
            if file.startswith('d_'):
                self.base.delete_from_base(self.__read_file(self.csv_file_path + '/' + file))

    def __read_file(self, file: str) -> list[base.Base]:
        units_list = []
        try:
            file_name = os.path.basename(file)
            # Убираем расширение и префикс
            unit_name = os.path.splitext(file_name)[0][2:]
            # Получаем класс по имени файла
            unit_class = self.base.get_unit_class(unit_name)

            with open(file) as open_file:
                units_data = csv.DictReader(open_file, dialect='excel')
                for unit_data in units_data:
                    unit = unit_class(**unit_data)
                    units_list.append(unit)

        except ClassNotExists:
            logger.error(f'Файл {file} имеет не верное название, название файла должно соответствовать названию класса')
        except TypeError:
            logger.error(f'Не удалось создать объект из файла {file}')
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
