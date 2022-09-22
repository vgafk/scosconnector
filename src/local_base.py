from loguru import logger
import json
from datetime import datetime
from os.path import exists
from abc import ABC, abstractmethod
from settings import Settings
from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey, Date, and_
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from uuid import uuid4
from exceptions import BaseConnectionError
import scos_dictionaries as dicts


class LocalBase(ABC):
    Base = declarative_base()
    Session = sessionmaker()
    session: Session = None

    @abstractmethod
    def check_base(self, create: bool = False) -> None:
        pass


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
                self.__create_base()
            else:
                raise BaseConnectionError(f'База данных не существует')

    def __create_base(self):
        """Создаем базу данных"""
        try:
            self.Base.metadata.create_all(bind=self.engine)
        except Exception as ex:
            raise ex
        else:
            logger.info(f"База данных создана")

    def get_unit_class(self, unit_name: str):
        try:
            return self.unit_classes_list[unit_name]
        except KeyError:
            raise ClassNotExists(f'Класс {unit_name} в программе не предусмотрен')

    def get_new_units_list(self):  # разобраться с join
        units = []
        for unit_class in self.unit_classes_list.values():
            units.extend(self.session.query(unit_class).filter(unit_class.last_scos_update.is_(None)).all())
        return units

    def add_to_base(self, units: list[LocalBase.Base]):
        self.session.add_all(units)
        self.session.commit()

    def get_changed_units(self):
        units = []
        for unit_class in self.unit_classes_list.values():
            units.extend(
                self.session.query(unit_class).filter(unit_class.last_scos_update < unit_class.last_update).all())
        return units

    def update_in_base(self, units: list[LocalBase.Base]):
        for unit in units:
            base_unit_type = type(unit)
            base_unit = self.session.query(base_unit_type).filter_by(id=unit.id)
            base_unit.update(unit.update_data())
            self.session.commit()

    def get_deleted_units(self):  # добавить что в сцос не удалено
        units = []
        for unit_class in self.unit_classes_list.values():
            units.extend(self.session.query(unit_class).filter(and_(unit_class.deleted.is_not(None),
                                                                    unit_class.deleted_scos.is_(None))).all())
        return units

    def delete_from_base(self, units: list[LocalBase.Base]):
        for unit in units:
            base_unit_type = type(unit)
            base_unit = self.session.query(base_unit_type).filter_by(id=unit.id)
            base_unit.update({'deleted': datetime.now()})
            self.session.commit()

    def commit(self):
        self.session.commit()
