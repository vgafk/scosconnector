import local_base
import scos_connector
import csv_reader
from loguru import logger
from exceptions import SCOSAccessError, SCOSAddError
scos_error_count = 0


def send_data_to_scos():
    try:
        scos_connector.check_connection()
        new_units_list = local_base.get_new_units_list()
        for new_unit in new_units_list:
            scos_connector.add_data_to_scos(new_unit)
            local_base.commit()
    except SCOSAccessError as ex:
        logger.error(ex)
    except SCOSAddError as ex:
        logger.error(ex)


if __name__ == "__main__":
    # try:
        local_base.check_base(create=True)

        csv_reader.check_csv_dir(create=True)
        csv_reader.read_files()

        send_data_to_scos()
        csv_reader.clear_scv_directory()
    # except Exception as ex:
    #     logger.error(f'большая ошибка: {ex}')