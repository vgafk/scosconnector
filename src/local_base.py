from datetime import datetime
from os.path import exists

from settings import LOCAL_BASE_PATH
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from uuid import uuid4
from exceptions import ClassNotExists

engine = create_engine(f'sqlite:///{LOCAL_BASE_PATH}', echo=True)
Base = declarative_base()
Session = sessionmaker()
session = Session(bind=engine)


class EducationalProgram(Base):
    __tablename__ = 'educational_programs'
    id = Column(Integer, primary_key=True)
    base_id = Column(Integer)
    external_id = Column(String, nullable=False)
    scos_id = Column(String)
    title = Column(String, nullable=False)
    direction = Column(String, nullable=False)
    code_direction = Column(String, nullable=False)
    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=False)
    last_update = Column(DateTime, nullable=False, default=datetime.now())
    last_scos_update = Column(DateTime)
    deleted = Column(DateTime)
    deleted_scos = Column(DateTime)

    def __init__(self, **kwargs):
        self.base_id = kwargs.get('base_id', 0)
        self.external_id = kwargs.get('external_id', str(uuid4()))
        self.scos_id = kwargs.get('scos_id', '')
        self.title = kwargs['title']
        self.direction = kwargs['direction']
        self.code_direction = kwargs['code_direction']
        self.start_year = kwargs['start_year']
        self.end_year = kwargs['end_year']

    def update_data(self):
        return {
            'title': self.title,
            'direction': self.direction,
            'code_direction': self.code_direction,
            'start_year': self.start_year,
            'end_year': self.end_year,
            'last_update': datetime.now(),
            'scos_id': self.scos_id
            }


class StudyPlans(Base):
    __tablename__ = 'study_plans'
    id = Column(Integer, primary_key=True)
    base_id = Column(Integer)
    external_id = Column(String, nullable=False)
    scos_id = Column(String)
    title = Column(String)
    education_form = Column(String)
    educational_program_id = Column(Integer)
    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=False)
    last_update = Column(DateTime, nullable=False, default=datetime.now())
    last_scos_update = Column(DateTime)
    deleted = Column(DateTime)
    deleted_scos = Column(DateTime)

    def __init__(self, **kwargs):
        self.base_id = kwargs.get('base_id', '')
        self.external_id = kwargs.get('external_id', str(uuid4()))
        self.scos_id = kwargs.get('scos_id', '')
        self.title = kwargs['title']
        self.education_form = kwargs['education_form']
        self.educational_program_id = kwargs['educational_program_id']
        self.start_year = kwargs['start_year']
        self.end_year = kwargs['end_year']

    def update_data(self):
        return {
            'title': self.title,
            'start_year': self.start_year,
            'education_form': self.education_form,
            'end_year': self.end_year,
            'last_update': datetime.now()
        }


class Disciplines(Base):
    __tablename__ = 'disciplines'
    id = Column(Integer, primary_key=True)
    base_id = Column(Integer)
    external_id = Column(String, nullable=False)
    scos_id = Column(String)
    title = Column(String)
    last_update = Column(DateTime, nullable=False, default=datetime.now())
    last_scos_update = Column(DateTime)
    deleted = Column(DateTime)
    deleted_scos = Column(DateTime)

    def __init__(self, **kwargs):
        self.base_id = kwargs.get('base_id', '')
        self.external_id = kwargs.get('external_id', str(uuid4()))
        self.scos_id = kwargs.get('scos_id', '')
        self.title = kwargs['title']

    def update_data(self):
        return {
            'title': self.title
        }


class StudyPlanDisciplines(Base):
    __tablename__ = 'study_plan_disciplines'
    id = Column(Integer, primary_key=True)
    base_id = Column(Integer)
    study_plan = Column(Integer)
    discipline = Column(Integer)
    semester = Column(Integer)
    last_update = Column(DateTime, nullable=False, default=datetime.now())
    last_scos_update = Column(DateTime)
    deleted = Column(DateTime)
    deleted_scos = Column(DateTime)

    def __init__(self, **kwargs):
        self.base_id = kwargs.get('base_id', '')
        self.study_plan = kwargs['study_plan']
        self.discipline = kwargs['discipline']
        self.semester = kwargs['semester']


def check_base(create: bool = False):
    """ Проверка существования файла базы данных

    :param create: Создать базу при отсутствии
    :return: Наличие файла базы данных
    """
    if not exists(LOCAL_BASE_PATH):
        if create:
            create_base()
        else:
            return False
    else:
        return True


def create_base():
    """Создаем базу данных"""
    Base.metadata.create_all(bind=engine)


def get_unit_class(unit_name: str):
    match unit_name:
        case 'educational_programs':
            return EducationalProgram
        case 'study_plans':
            return StudyPlans
        case 'disciplines':
            return Disciplines
        case 'study_plan_disciplines':
            return StudyPlanDisciplines
        case _:
            raise ClassNotExists


def add_to_base(units: list):
    session.add_all(units)
    session.commit()


def update_in_base(units: list):
    for unit in units:
        base_unit_type = type(unit)
        base_unit = session.query(base_unit_type).filter_by(base_id=unit.base_id)
        base_unit.update(unit.update_data())
        session.commit()

# ep = local_base.session.query(local_base.EducationalProgram).\
    #     filter(local_base.EducationalProgram.base_id == 1).\
    #     update(nep.update_data())
    # print(nep.update_data())


def delete_from_base(units: list):
    pass
