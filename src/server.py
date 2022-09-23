from argparse import ArgumentParser
import sys
from loguru import logger
from local_base import LocalBase
from sqlitebase import SQLiteBase
from scos_connector import SCOSConnector
from csv_reader import CSVReader
from action import Action
from exceptions import BaseConnectionError


# Парсинг входящие параметры
def setup_params():
    parser = ArgumentParser(description='Process some integers.')
    parser.add_argument('--log_level', metavar='loger_level', type=str, dest='loger_level',
                        help='Уровень логирования процесса, по умолчанию debug', default='DEBUG',
                        choices=['debug', 'info', 'warnings', 'error', 'critical'])
    parser.add_argument('--to_scos', metavar='to_scos', type=str, dest='to_scos',
                        help='Необходимость записи в СЦОС', default='yes',
                        choices=['yes', 'no'])
    parser.add_argument('--first_run', metavar='first_run', type=str, dest='first_run',
                        help='Первый запуск программы', default='no',
                        choices=['yes', 'no'])
    return parser.parse_args()


def set_logger(level: str) -> None:
    logger.remove()
    logger.add(sys.stdout, level=level.upper())


def first_run(base_local: LocalBase, reader_csv: CSVReader):
    try:
        base_local.check_base(create=True)
        reader_csv.check_csv_dir(create=True)
    except BaseConnectionError as ex:
        logger.critical(f'{type(ex)}: {ex}')


def set_action():
    """Создание объектов для работы"""
    args = setup_params()
    csvreader = CSVReader(file_dir='csv_files')
    base = SQLiteBase(base_file_path='cache.db')
    connector = SCOSConnector()

    if args.first_run:
        first_run(base_local=base, reader_csv=csvreader)

    return Action(base_local=base, reader_csv=csvreader, connector=connector)


if __name__ == "__main__":
    action = set_action()

    action.run_synchronization()