from loguru import logger
from os.path import exists
from local_base import LocalBase
from sqlalchemy import create_engine, and_
from exceptions import BaseConnectionError


class SQLiteBase(LocalBase):
    def __init__(self, base_file_path: str):
        self.local_base_path = base_file_path
        self.engine = create_engine(f'sqlite:///{self.local_base_path}', echo=False)
        self.session = self.Session(bind=self.engine)

    def check_base(self, create: bool = False) -> None:
        """ Проверка существования файла базы данных

        :param create: Создать базу при отсутствии
        """
        if not exists(self.local_base_path):
            logger.debug(f"База данных {self.local_base_path} не существует")
            if create:
                logger.debug(f"Базу данных требуется создать")
                self.create_base()
            else:
                raise BaseConnectionError(f'База данных не существует')

    def create_base(self):
        """Создаем базу данных"""
        try:
            self.base.metadata.create_all(bind=self.engine)
        except Exception as ex:
            raise ex
        else:
            logger.info(f"База данных создана")

