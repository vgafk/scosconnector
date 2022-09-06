import sqlite3
from os.path import exists

from scos_units import ScosUnit
from settings import local_base_path
from loger import write_to_log
from tables import tables, update_trigger_text


class SQL:
    def __enter__(self):
        self.conn = sqlite3.connect(local_base_path)
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, type, value, traceback):
        self.cur.close()
        self.conn.close()

    def fetchall(self, query):
        try:
            data = self.cur.execute(query).fetchall()
        except sqlite3.Error as error:
            write_to_log(f'Ошибка локальной базы: {error}')
        return data

    def execute(self, query):
        try:
            self.cur.execute(query)
            self.conn.commit()
        except sqlite3.Error as error:
            write_to_log(f'Ошибка локальной базы: {error}')


def insert(unit: ScosUnit):
    with SQL() as sql:
        columns = ','.join(unit.__dict__.keys())
        values = '"' + '","'.join(unit.__dict__.values()) + '"'
        query = f'INSERT INTO {unit.get_table()}({columns}) ' \
                f'VALUES({values});'
        sql.execute(query)
        write_to_log(f'Запись в {unit.get_table()}')


def update(unit: ScosUnit):
    with SQL() as sql:
        params = [f'{name} = "{val}"' for name, val in unit.__dict__.items()]
        query = f'UPDATE {unit.get_table} SET {", ".join(params)} ' \
                f'WHERE external_id = "{unit.__dict__["external_id"]}"'
        sql.execute(query)
        write_to_log(f'Запись в {unit.get_table()}')


def check_base():
    if not exists(local_base_path):
        write_to_log('Файл базы не обнаружен, создаем новый...')
        create_base()


def create_base():
    with SQL() as sql:
        for name, table in tables.items():
            sql.execute(table)
            write_to_log(f'Создана таблица {name}')
            sql.execute(update_trigger_text.replace('%name', name))
            write_to_log(f'Создан триггер обновления для {name}')


def get_updated_data(table: str):
    with SQL() as sql:
        query = f"SELECT * FROM {table} WHERE last_update > last_scos_update"
        print(query)