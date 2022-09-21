import json
from datetime import datetime
from os.path import exists

from settings import LOCAL_BASE_PATH, ORG_ID
from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey, Date, and_
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from uuid import uuid4
from exceptions import ClassNotExists
import scos_dictionaries as dicts

engine = create_engine(f'sqlite:///{LOCAL_BASE_PATH}', echo=False)
Base = declarative_base()
Session = sessionmaker()
session = Session(bind=engine)


class EducationalProgram(Base):
    __tablename__ = 'educational_programs'
    id = Column(Integer, primary_key=True)
    external_id = Column(String, nullable=False)
    scos_id = Column(String)
    title = Column(String, nullable=False)
    direction = Column(String, nullable=False)
    code_direction = Column(String, nullable=False)
    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=False)
    last_update = Column(DateTime, nullable=False, default=datetime.now())
    last_scos_update = Column(DateTime, nullable=True)
    deleted = Column(DateTime, nullable=True)
    deleted_scos = Column(DateTime, nullable=True)
    study_plans = relationship("StudyPlan", backref="educational_program")

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.external_id = kwargs.get('external_id', str(uuid4()))
        self.scos_id = kwargs.get('scos_id', None)
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
            'last_update': datetime.now()
            }

    def to_json(self):
        return json.dumps({
            'organization_id': ORG_ID,
            'external_id': self.external_id,
            'title': self.title,
            'direction': self.direction,
            'code_direction': self.code_direction,
            'start_year': self.start_year,
            'end_year': self.end_year
        })


class StudyPlan(Base):
    __tablename__ = 'study_plans'
    id = Column(Integer, primary_key=True)
    external_id = Column(String, nullable=False)
    scos_id = Column(String)
    title = Column(String)
    education_form = Column(String)
    educational_program_id = Column(Integer, ForeignKey("educational_programs.id"))
    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=False)
    last_update = Column(DateTime, nullable=False, default=datetime.now())
    last_scos_update = Column(DateTime, nullable=True)
    deleted = Column(DateTime, nullable=True)
    deleted_scos = Column(DateTime, nullable=True)
    study_plan_disciplines = relationship("StudyPlanDisciplines", backref="study_plan")
    study_plan_student = relationship("StudyPlanStudents", backref="study_plan")
    marks = relationship("Marks", backref="study_plan")

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.external_id = kwargs.get('external_id', str(uuid4()))
        self.scos_id = kwargs.get('scos_id', '')
        self.title = kwargs['title']
        self.direction = kwargs['direction']
        self.code_direction = kwargs['code_direction']
        self.education_form = kwargs['education_form']
        self.educational_program_id = kwargs['educational_program_id']
        self.start_year = kwargs['start_year']
        self.end_year = kwargs['end_year']

    def update_data(self):
        return {
            'title': self.title,
            'education_form': self.education_form,
            'start_year': self.start_year,
            'end_year': self.end_year,
            'last_update': datetime.now()
        }

    def to_json(self):
        return json.dumps({
            'organization_id': ORG_ID,
            'external_id': self.external_id,
            'title': self.title,
            'direction': self.educational_program.direction,            # Объект educational_program
            'code_direction': self.educational_program.code_direction,  # придет при выборке из базы
            'education_form': dicts.education_form[self.education_form],
            'educational_program': self.educational_program.external_id,
            'start_year': self.start_year,
            'end_year': self.end_year
        })


class Discipline(Base):
    __tablename__ = 'disciplines'
    id = Column(Integer, primary_key=True)
    external_id = Column(String, nullable=False)
    scos_id = Column(String)
    title = Column(String)
    last_update = Column(DateTime, nullable=False, default=datetime.now())
    last_scos_update = Column(DateTime, nullable=True)
    deleted = Column(DateTime, nullable=True)
    deleted_scos = Column(DateTime, nullable=True)
    study_plan_disciplines = relationship("StudyPlanDisciplines", backref="discipline")
    marks = relationship("Marks", backref="discipline")

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.external_id = kwargs.get('external_id', str(uuid4()))
        self.scos_id = kwargs.get('scos_id', '')
        self.title = kwargs['title']

    def update_data(self):
        return {
            'title': self.title,
            'last_update': datetime.now()
        }

    def to_json(self):
        return json.dumps({
            'organization_id': ORG_ID,
            'external_id': self.external_id,
            'title': self.title
        })


class StudyPlanDisciplines(Base):
    __tablename__ = 'study_plan_disciplines'
    id = Column(Integer, primary_key=True)
    study_plan_id = Column(ForeignKey("study_plans.id"), primary_key=True)
    discipline_id = Column(ForeignKey("disciplines.id"), primary_key=True)
    semester = Column(Integer)
    last_update = Column(DateTime, nullable=False, default=datetime.now())
    last_scos_update = Column(DateTime, nullable=True)
    deleted = Column(DateTime, nullable=True)
    deleted_scos = Column(DateTime, nullable=True)

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.study_plan_id = kwargs['study_plan']
        self.discipline_id = kwargs['discipline']
        self.semester = kwargs['semester']

    def to_json(self):
        return json.dumps({
            'organization_id': ORG_ID,
            'study_plan': self.study_plan.external_id,
            'discipline': self.discipline.external_id,
            'semester': self.semester
        })


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    external_id = Column(String, nullable=False)
    scos_id = Column(String)
    surname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    middle_name = Column(String)
    snils = Column(String)
    inn = Column(String)
    email = Column(String)
    phone = Column(String)
    study_year = Column(Integer, nullable=False)
    last_update = Column(DateTime, nullable=False, default=datetime.now())
    last_scos_update = Column(DateTime, nullable=True)
    deleted = Column(DateTime, nullable=True)
    deleted_scos = Column(DateTime, nullable=True)
    study_plan_students = relationship("StudyPlanStudents", backref="student")
    contingent_flows = relationship("ContingentFlows", backref="student")
    marks = relationship("Marks", backref="student")

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.external_id = kwargs.get('external_id', str(uuid4()))
        self.surname = kwargs['surname']
        self.name = kwargs['name']
        self.middle_name = kwargs.get('middle_name', '')
        self.snils = kwargs.get('snils', '')
        self.inn = kwargs.get('inn', '')
        self.email = kwargs.get('email', '')
        self.phone = kwargs.get('phone', '')
        self.study_year = kwargs['study_year']

    def update_data(self):
        return {
            'surname': self.surname,
            'name': self.name,
            'middle_name': self.middle_name,
            'snils': self.snils,
            'inn': self.inn,
            'email': self.email,
            'phone': self.phone,
            'study_year': self.study_year,
            'last_update': datetime.now()
            }

    def to_json(self):
        return json.dumps({
            'organization_id': ORG_ID,
            'external_id': self.external_id,
            'surname': self.surname,
            'name': self.name,
            'middle_name': self.middle_name,
            'snils': self.snils,
            'inn': self.inn,
            'email': self.email,
            'phone': self.phone,
            'study_year': self.study_year
        })


class StudyPlanStudents(Base):
    __tablename__ = 'study_plan_students'
    id = Column(Integer, primary_key=True)
    study_plan_id = Column(ForeignKey("study_plans.id"))
    student_id = Column(ForeignKey("students.id"))
    last_update = Column(DateTime, nullable=False, default=datetime.now())
    last_scos_update = Column(DateTime, nullable=True)
    deleted = Column(DateTime, nullable=True)
    deleted_scos = Column(DateTime, nullable=True)

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.study_plan_id = kwargs['study_plan']
        self.student_id = kwargs['student']

    def to_json(self):
        return json.dumps({
            'organization_id': ORG_ID,
            'study_plan': self.study_plan.external_id,
            'student': self.student.external_id
        })


class ContingentFlows(Base):
    __tablename__ = 'contingent_flows'
    id = Column(Integer, primary_key=True)
    scos_id = Column(String)
    student_id = Column(ForeignKey("students.id"))
    contingent_flow = Column(String)
    flow_type = Column(String)
    date = Column(Date)
    faculty = Column(String)
    education_form = Column(String)
    form_fin = Column(String)
    details = Column(String)
    last_update = Column(DateTime, nullable=False, default=datetime.now())
    last_scos_update = Column(DateTime, nullable=True)
    deleted = Column(DateTime, nullable=True)
    deleted_scos = Column(DateTime, nullable=True)

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.student_id = kwargs['student']
        self.contingent_flow = kwargs['contingent_flow']
        self.flow_type = kwargs['flow_type']
        self.date = datetime.strptime(kwargs['date'], '%Y-%m-%d').date()
        self.faculty = kwargs['faculty']
        self.education_form = kwargs['education_form']
        self.form_fin = kwargs['form_fin']
        self.details = kwargs['details']

    def update_data(self):
        return {
            'student_id': self.student_id,
            'contingent_flow': self.contingent_flow,
            'flow_type': self.flow_type,
            'date': self.date,
            'faculty': self.faculty,
            'education_form': self.education_form,
            'form_fin': self.form_fin,
            'details': self.details,
            'last_update': datetime.now()
        }

    def to_json(self):
        return json.dumps({
            'organization_id': ORG_ID,
            'student': self.student.external_id,
            'contingent_flow': self.contingent_flow,
            'flow_type': dicts.flow_types[self.flow_type],
            'date': self.date.strftime('%Y-%m-%dT00:00:00.000'),
            'faculty': self.faculty,
            'education_form': dicts.education_form[self.education_form],
            'form_fin': self.form_fin,
            'details': self.details
        })


class Marks(Base):
    __tablename__ = 'marks'
    id = Column(Integer, primary_key=True)
    scos_id = Column(String)
    external_id = Column(String, nullable=False)
    discipline_id = Column(ForeignKey("disciplines.id"))
    study_plan_id = Column(ForeignKey("study_plans.id"))
    student_id = Column(ForeignKey("students.id"))
    mark_type = Column(String)
    mark_value = Column(Integer)
    semester = Column(Integer)
    last_update = Column(DateTime, default=datetime.now())
    last_scos_update = Column(DateTime, nullable=True)
    deleted = Column(DateTime, nullable=True)
    deleted_scos = Column(DateTime, nullable=True)

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.external_id = kwargs.get('external_id', str(uuid4()))
        self.discipline_id = kwargs['discipline']
        self.study_plan_id = kwargs['study_plan']
        self.student_id = kwargs['student']
        self.mark_type = kwargs['mark_type']
        self.mark_value = kwargs['mark_value']
        self.semester = kwargs['semester']

    def update_data(self):
        return {
            'mark_type': self.mark_type,
            'mark_value': self.mark_value,
            'semester': self.semester,
            'last_update': datetime.now()
        }

    def to_json(self):
        return json.dumps({
            'organization_id': ORG_ID,
            'external_id': self.external_id,
            'discipline': self.discipline.external_id,
            'study_plan': self.study_plan.external_id,
            'student': self.student.external_id,
            'mark_type': dicts.marks_types[self.mark_type],
            'mark_value': self.mark_value,
            'semester': self.semester,
        })


unit_classes_list = {
    'educational_programs': EducationalProgram,
    'study_plans': StudyPlan,
    'disciplines': Discipline,
    'study_plan_disciplines': StudyPlanDisciplines,
    'students': Student,
    'study_plan_students': StudyPlanStudents,
    'contingent_flows': ContingentFlows,
    'marks': Marks
}


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
    try:
        return unit_classes_list[unit_name]
    except KeyError:
        raise ClassNotExists(f'Класс {unit_name} в программе не предусмотрен')


def get_new_units_list():  # разобраться с join
    units = []
    for unit_class in unit_classes_list.values():
        units.extend(session.query(unit_class).filter(unit_class.last_scos_update.is_(None)).all())
    return units


def add_to_base(units: list):
    session.add_all(units)
    session.commit()
    pass


def get_changed_units():
    units = []
    for unit_class in unit_classes_list.values():
        units.extend(session.query(unit_class).filter(unit_class.last_scos_update < unit_class.last_update).all())
    return units


def update_in_base(units: list):
    for unit in units:
        base_unit_type = type(unit)
        base_unit = session.query(base_unit_type).filter_by(id=unit.id)
        base_unit.update(unit.update_data())
        session.commit()


def get_deleted_units():       # добавить что в сцос не удалено
    units = []
    for unit_class in unit_classes_list.values():
        units.extend(session.query(unit_class).filter(and_(unit_class.deleted.is_not(None),
                                                      unit_class.deleted_scos.is_(None))).all())
    return units


def delete_from_base(units: list):
    for unit in units:
        base_unit_type = type(unit)
        base_unit = session.query(base_unit_type).filter_by(id=unit.id)
        base_unit.update({'deleted': datetime.now()})
        session.commit()


def commit():
    session.commit()