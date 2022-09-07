import sqlite3
from os.path import exists
from loguru import logger

from scos_units import ScosUnit
from settings import local_base_path
from tables import tables, update_trigger_text


# def to_str(val):
#     return '' if val is None else str(val)


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


def get_updated_data(table: str):
    with SQL() as sql:
        query = f"SELECT * FROM {table} WHERE last_update > last_scos_update"
        return sql.get_dict(query)

