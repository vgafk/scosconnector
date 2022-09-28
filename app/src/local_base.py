from abc import ABC, abstractmethod
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Base, get_unit_classes_list, Updatable
from loguru import logger
from scos_dictionaries import ActionsList


class LocalBase(ABC):
    base = Base
    Session = sessionmaker()
    session: Session = None

    @abstractmethod
    def check_base(self, create: bool = False) -> None:
        pass

    @abstractmethod
    def create_base(self):
        pass

    def get_new_units_list(self) -> Base:
        """Выборка новых записей из локальной базы"""
        units = []
        for unit_class in get_unit_classes_list().values():
            units.extend(self.session.query(unit_class).filter(unit_class.last_scos_update.is_(None)).all())
        return units

    def add_to_base(self, units: list[Base]):
        """Добавление записей в локальную базу"""
        self.session.add_all(units)
        self.session.commit()
        logger.debug('Внесение новых записей в локальную базе завершено')

    def get_changed_units(self):
        """Выборка обновленных записей"""
        units = []
        for unit_class in get_unit_classes_list().values():
            units.extend(
                self.session.query(unit_class).filter(unit_class.last_scos_update < unit_class.last_update).all())
        return units

    def update_in_base(self, units: list[Updatable]):
        """Обновление записей в локальной базе"""
        for unit in units:
            base_unit_type = type(unit)
            base_unit = self.session.query(base_unit_type).filter_by(id=unit.id)
            base_unit.update(unit.update_data())
            self.session.commit()
        logger.debug('Обновление записей в локальной базе завершено')

    def get_deleted_units(self):
        """Список записей с отметкой об удалении"""
        units = []
        for unit_class in get_unit_classes_list().values():
            units.extend(self.session.query(unit_class).filter(and_(unit_class.deleted.is_not(None),
                                                                    unit_class.deleted_scos.is_(None))).all())
        return units

    def delete_from_base(self, units: list[Base]):
        """Удаление из локальной базы, делается отметка об удалении данные по факту остаются"""
        for unit in units:
            base_unit_type = type(unit)
            base_unit = self.session.query(base_unit_type).filter_by(id=unit.id)
            base_unit.update({'deleted': datetime.now()})
            self.session.commit()
        logger.debug('Удаление записей из локальной базы завершено')

    def get_all_units(self):
        """Выборка сех записей подлежащих отправке в СЦОС"""
        unit_list: {ActionsList: list[Base]} = {ActionsList.ADD: self.get_new_units_list(),
                                                ActionsList.UPD: self.get_changed_units(),
                                                ActionsList.DEL: self.get_deleted_units()}
        return unit_list

    def commit(self):
        self.session.commit()