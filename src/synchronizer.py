from local_base import LocalBase
from scos_connector import SCOSConnector
from reader import Reader
from loguru import logger
from scos_dictionaries import ActionsList

# количество ошибок для отправки уведомления
scos_error_count = 1


class Synchronizer:
    """Класс синхронизации собственной базы данных с ИС организации, и с СЦОС"""

    def __init__(self, base: LocalBase, connector: SCOSConnector, reader: Reader):
        self.base_local = base
        self.connector = connector
        self.reader = reader

    def _sent_to_local_base(self, unit_list: dict[ActionsList, list[LocalBase.base]]):
        self.base_local.check_base(True)
        self.base_local.add_to_base(unit_list[ActionsList.ADD])
        self.base_local.update_in_base(unit_list[ActionsList.UPD])
        self.base_local.delete_from_base(unit_list[ActionsList.DEL])
        self.base_local.commit()

        logger.info("Изменение внесение, изменение и удаление данных в локальной базе данных завершены")

    def _send_to_scos(self, unit_list: dict[ActionsList, list[LocalBase.base]]):
        self.connector.check_connection()
        for unit in unit_list[ActionsList.ADD]:
            self.connector.add_to_scos(unit)
        for unit in unit_list[ActionsList.UPD]:
            self.connector.update_in_scos(unit)
        for unit in unit_list[ActionsList.DEL]:
            self.connector.delete_from_scos(unit)
        self.base_local.commit()

        logger.info("Изменение внесение, изменение и удаление на сервере СЦОС завершены")

    def run_synchronization(self):
        """Обновление локальной базы данных и синхронизация с сервером СЦОС"""
        units_list = self.reader.get_new_data()

        self._sent_to_local_base(units_list)

        if self.connector:
            scos_unit_list = self.base_local.get_all_units()
            logger.debug("Синхронизация с СЦОС...")
            self._send_to_scos(scos_unit_list)
            logger.info("Синхронизация локальной базы данных с сервером СЦОС завершена")
        else:
            logger.warning("Синхронизация локальной базы данных с сервером СЦОС отключена")
