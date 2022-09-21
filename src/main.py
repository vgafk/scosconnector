from local_base import LocalBase
from scos_connector import SCOSConnector
from csv_reader import CSVReader
from loguru import logger
from exceptions import SCOSAccessError, SCOSAddError

scos_error_count = 0
csvreader = CSVReader()
scosconnector = SCOSConnector()
base = LocalBase()


def send_data_to_scos():
    "Полная синхронизация данныз в СЦОС с данными локальной базы данных"
    try:
        units_list = {}
        SCOSConnector.check_connection()
        units_list['add'] = base.get_new_units_list()      # Добавляем новые записи
        units_list['upd'] = base.get_changed_units()       # Добавляем измененные записи
        units_list['del'] = base.get_deleted_units()
        for action, units in units_list.items():
            for unit in units:
                scosconnector.send_to_scos(unit, action_type=action)
                base.commit()
    except SCOSAccessError as ex:
        logger.error(ex)
    except SCOSAddError as ex:
        logger.error(ex)


if __name__ == "__main__":
    try:
        base.check_base(create=True)
        csvreader.check_csv_dir(create=True)
        csvreader.read_files()
        send_data_to_scos()
        csvreader.clear_scv_directory()
    except Exception as ex:
        logger.error(f'большая ошибка: {ex}')