import time
import schedule
from argparse import ArgumentParser
import sys
from loguru import logger
from sqlitebase import LocalBase, SQLiteBase
from scos_connector import SCOSConnector
from csv_reader import Reader, CSVReader
from synchronizer import Synchronizer


# Парсинг входящие параметры
def setup_params():
    parser = ArgumentParser(description='Process some integers.')
    parser.add_argument('--log_level', metavar='loger_level', type=str, dest='loger_level',
                        help='Уровень логирования процесса, по умолчанию debug', default='DEBUG',
                        choices=['debug', 'info', 'warnings', 'error', 'critical'])
    parser.add_argument('--to_scos', metavar='to_scos', type=str, dest='to_scos',
                        help='Необходимость записи в СЦОС', default='yes',
                        choices=['yes', 'no'])
    parser.add_argument('--base', metavar='base', type=str, dest='base',
                        help='Тип базы данных', default='sqlite',
                        choices=['sqlite'])
    parser.add_argument('--new_data_format', metavar='reader', type=str, dest='reader',
                        help='Формат данных обновления', default='csv',
                        choices=['csv'])
    return parser.parse_args()


def set_logger(level: str) -> None:
    logger.remove()
    logger.add(sys.stdout, level=level.upper())


def set_synchronizer(new_data_format: str, base: str, to_scos: bool) -> Synchronizer:
    """Создание объектов для работы"""

    reader = get_reader(new_data_format)
    base = get_database(base)
    connector = SCOSConnector() if to_scos == 'yes' else None

    return Synchronizer(base=base, reader=reader, connector=connector)


def get_reader(data_format: str) -> Reader:
    match data_format:
        case 'csv':
            return CSVReader(file_dir='csv_files')


def get_database(base: str) -> LocalBase:
    match base:
        case 'sqlite':
            return SQLiteBase(base_file_path='cache.db')


if __name__ == "__main__":
    args = setup_params()

    set_logger(args.loger_level)

    synchronizer = set_synchronizer(args.reader, args.base, args.to_scos)
    synchronizer.run_synchronization()
    schedule.every(10).seconds.do(synchronizer.run_synchronization)

    while True:
        schedule.run_pending()
        time.sleep(1)
