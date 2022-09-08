import sqlite3
from os.path import exists
from loguru import logger

from scos_units import ScosUnit, data_classes
from settings import local_base_path
from tables import tables, update_trigger_text


class SQL:
    def __enter__(self):
        self.conn = sqlite3.connect(local_base_path)
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, type, value, traceback):
        self.cur.close()
        self.conn.close()

    def get_dict(self, query):
        records = []
        try:
            values = self.cur.execute(query).fetchall()
            column_names = [column[0] for column in self.cur.description]
            for value in values:
                records.append(dict(zip(column_names, value)))
        except sqlite3.Error as error:
            logger.error(f'Ошибка локальной базы: {error}')
        return records

    def execute(self, query):
        try:
            self.cur.execute(query)
            self.conn.commit()
        except sqlite3.Error as error:
            logger.error(f'Ошибка локальной базы: {error}')


def insert(unit: ScosUnit):
    with SQL() as sql:
        columns = ','.join(unit.__dict__.keys())
        # данные могут быть пустыми, приводим их к строке
        values = '"' + '","'.join(list(map(str, unit.__dict__.values()))) + '"'

        query = f'INSERT INTO {unit.get_table()}({columns}) ' \
                f'VALUES({values});'
        logger.debug(query)
        sql.execute(query)
        logger.info(f'Запись в {unit.get_table()}')


def update(unit: ScosUnit):
    with SQL() as sql:
        params = [f'{name} = "{val}"' for name, val in unit.__dict__.items()]
        query = f'UPDATE {unit.get_table} SET {", ".join(params)} ' \
                f'WHERE external_id = "{unit.__dict__["external_id"]}"'
        sql.execute(query)
        logger.info(f'Обновление таблицы {unit.get_table()}')


def base_exist():
    if not exists(local_base_path):
        logger.info('Файл базы не обнаружен, создаем новый...')
        return False
    else:
        return True


def create_base():
    with SQL() as sql:
        for name, table in tables.items():
            sql.execute(table)
            logger.info(f'Создана таблица {name}')
            sql.execute(update_trigger_text.replace('%name', name))
            logger.info(f'Создан триггер обновления для {name}')


def get_all_updated_data():
    all_updated_data = []
    # all_updated_data.extend(get_updated_data('educational_programs'))
    # all_updated_data.extend(get_updated_data('study_plans'))
    # all_updated_data.extend(get_updated_data('disciplines'))
    # у students из list_from_json Возвращается два списка, потому берем первый
    all_updated_data.extend(data_classes['students'].list_from_json(get_updated_data('students'))[0])
    # all_updated_data.extend(get_updated_data('contingent_flows'))
    # all_updated_data.extend(get_updated_data('marks'))
    # all_updated_data.extend(data_classes['marks'].list_from_json(get_updated_data('marks')))

    return all_updated_data


def get_updated_data(table: str):
    with SQL() as sql:
        query = f"SELECT * FROM {table} WHERE last_update > last_scos_update"
        return sql.get_dict(query)


def get_all_deleted_data():
    all_deleted_data = []
    # all_deleted_data.extend(get_deleted_data('educational_programs'))
    # all_deleted_data.extend(get_deleted_data('study_plans'))
    # all_deleted_data.extend(data_classes['disciplines'].list_from_json(get_deleted_data('disciplines')))
    # у students из list_from_json Возвращается два списка, потому берем первый
    # all_deleted_data.extend(data_classes['students'].list_from_json(get_deleted_data('students'))[0])
    # all_deleted_data.extend(get_deleted_data('contingent_flows'))
    # all_deleted_data.extend(get_deleted_data('marks'))
    # all_deleted_data.extend(data_classes['marks'].list_from_json(get_deleted_data('marks')))

    return all_deleted_data


def get_deleted_data(table: str):
    with SQL() as sql:
        query = f"SELECT * FROM {table} WHERE deleted IS NOT NULL AND deleted_scos IS NULL"
        return sql.get_dict(query)