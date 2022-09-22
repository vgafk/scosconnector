import sys
import argparse
from enum import Enum

from local_base import LocalBase
from scos_connector import SCOSConnector
from csv_reader import CSVReader
from loguru import logger
from exceptions import SCOSAccessError, SCOSAddError

# количество ошибок для отправки уведомления
scos_error_count = 1


class Action:
    """Класс синхронизации собственной базы данных с ИС организации, и с СЦОС"""
    def __init__(self, base_local: LocalBase, connector: SCOSConnector, reader_csv: CSVReader):
        self.base_local = base_local
        self.connector = connector
        self.reader_csv = reader_csv

    def run_synchronization(self):
        """Синхронизация с сервером СЦОС"""
        try:
            unit_list = self.reader_csv.read_files()
            logger.debug(unit_list)
            # self.send_data_to_scos()
            # self.csvreader.clear_scv_directory()
        except Exception as ex:
            logger.error(f'большая ошибка: {ex}')


# def send_data_to_scos():
#     "Полная синхронизация данныз в СЦОС с данными локальной базы данных"
#     try:
#         units_list = {}
#         SCOSConnector.check_connection()
#         units_list['add'] = base.get_new_units_list()      # Добавляем новые записи
#         units_list['upd'] = base.get_changed_units()       # Добавляем измененные записи
#         units_list['del'] = base.get_deleted_units()
#         for action, units in units_list.items():
#             for unit in units:
#                 scosconnector.send_to_scos(unit, action_type=action)
#                 base.commit()
#     except SCOSAccessError as ex:
#         logger.error(ex)
#     except SCOSAddError as ex:
#         logger.error(ex)




    #
