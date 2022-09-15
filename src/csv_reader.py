import csv
import os
from settings import CSV_FILE_PATH
from loguru import logger
import local_base
from exceptions import ClassNotExists


def check_csv_dir(create=False) -> bool:
    """Проверяем наличие директории для csv файлов

    :param create: создать директории при отсутствии
    """
    if not os.path.exists(CSV_FILE_PATH):
        if create:
            create_csv_dir()
        else:
            return False
    else:
        return True


def create_csv_dir():
    """Создание директории для csv файлов"""
    try:
        os.mkdir(CSV_FILE_PATH)
    except OSError as ex:
        logger.error(f'Ошибка создания директории для csv файлов {CSV_FILE_PATH}: {ex}')
    else:
        logger.info(f'Создана директория для csv файлов: {CSV_FILE_PATH}')


def read_files():
    """Чтение всех файлов в директории по типам, a_ добавление, u_ обновление, d_ удаление"""
    for file in os.listdir(CSV_FILE_PATH):
        if file.startswith('a_'):
            local_base.add_to_base(read_file(CSV_FILE_PATH + '/' + file))
    for file in os.listdir(CSV_FILE_PATH):
        if file.startswith('u_'):
            local_base.update_in_base(read_file(CSV_FILE_PATH + '/' + file))
    for file in os.listdir(CSV_FILE_PATH):
        if file.startswith('d_'):
            local_base.delete_from_base(read_file(CSV_FILE_PATH + '/' + file))


def read_file(file: str) -> list[local_base.Base]:
    try:
        file_name = os.path.basename(file)
        unit_name = os.path.splitext(file_name)[0][2:]  # Убираем расширение и префикс
        units_list = []
        unit_class = local_base.get_unit_class(unit_name)

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


def clear_scv_directory():
    for file in os.scandir(CSV_FILE_PATH):
        os.remove(file.path)


if __name__ == '__main__':
    read_files()

    # nep = local_base.EducationalProgram(id=1,
    #                                    base_id=1,
    #                                    title='Психология и социальная педагогика',
    #                                    direction='Психолого-педагогическое образование',
    #                                    code_direction='44.03.02',
    #                                    start_year=2022,
    #                                    end_year=2026)

# local_base.session.add(ep)
# local_base.session.commit()
#
    # ep = local_base.session.query(local_base.EducationalProgram).\
    #     filter(local_base.EducationalProgram.base_id == 1).\
    #     update(nep.update_data())
    # print(nep.update_data())
    # local_base.session.commit()
    # print(ep[0])
