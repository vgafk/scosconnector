import csv
import os
from settings import CSV_FILE_PATH
from loguru import logger
from scos_units import data_classes


def csv_dir_exists():
    return os.path.exists(CSV_FILE_PATH)


def create_csv_dir():
    try:
        os.mkdir(CSV_FILE_PATH)
    except OSError:
        logger.error(f'Ошибка создания директории для csv файлов: {CSV_FILE_PATH}')
    else:
        logger.info(f'Создана директория для csv файлов: {CSV_FILE_PATH}')


def read_all_files():
    add_units_list = []
    update_units_list = []
    delete_units_list = []
    # for file in os.listdir(CSV_FILE_PATH):
    try:
        for file_name in data_classes:
            print(CSV_FILE_PATH + '/a_' + file_name + '.csv')
            if os.path.exists(CSV_FILE_PATH + '/a_' + file_name + '.csv'):
                add_units_list.extend(read_file(CSV_FILE_PATH + '/a_' + file_name + '.csv'))
            if os.path.exists(CSV_FILE_PATH + '/u_' + file_name + '.csv'):
                update_units_list.extend(read_file(CSV_FILE_PATH + '/a_' + file_name + '.csv'))
            if os.path.exists(CSV_FILE_PATH + '/d_' + file_name + '.csv'):
                delete_units_list.extend(read_file(CSV_FILE_PATH + '/a_' + file_name + '.csv'))
    except TypeError as error:
        logger.error(f'Ошибка чтения файлов {error}')
    return add_units_list, update_units_list, delete_units_list


def read_file(file: str):
    with open(file) as open_file:
        file_name = os.path.basename(file)
        unit_name = os.path.splitext(file_name)[0][2:]      # Убираем расширение и префикс
        try:
            units = data_classes[unit_name].list_from_json(csv.DictReader(open_file, dialect='excel'))
            return units
        except Exception as er:
            logger.error(f'Не удалось cформировать данные из файла {file}: {er}')

