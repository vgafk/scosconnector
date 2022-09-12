import json
from datetime import datetime
from settings import ORG_ID
from loguru import logger

#  Форма обучения
# education_form = {'заочная': 'EXTRAMURAL', 'очная': 'FULL_TIME','очнозаочная': 'PART_TIME',
#                   'сок.заочная': 'SHORT_EXTRAMURAL', 'сок.очная': 'SHORT_FULL_TIME','экстернат': 'EXTERNAL'}

# Движение студентов
# flow_types = {'Зачисление в Организацию': 'ENROLLMENT', 'Отчисление из Организации': 'DEDUCTION',
#               'Перевод на следующий курс': 'TRANSFER', 'Восстановление в Организации': 'REINSTATEMENT',
#               'Предоставление академического отпуска': 'SABBATICAL_TAKING'}

# Типы оценок
# marks_types = {'оценка': 'MARK', 'зачет': 'CREDIT', 'Дифференцированный зачет': 'DIF_CREDIT',
#                'Стобалльная оценка': 'HUNDRED_POINT'}


class ScosUnit:
    table_name: str
    base_id: int

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @classmethod
    def to_json(cls):
        pass

    @classmethod
    def query(cls, action: str):
        pass

    @staticmethod
    def list_from_json(data_list, unit_id=''):
        pass

    def get_table(self):
        return self.table_name

    def id(self):
        return self.id

    def get_values(self):
        pass


class EducationalProgram(ScosUnit):
    table_name = 'educational_programs'

    def __init__(self, **kwargs):
        self.external_id = kwargs.get('external_id', '')
        self.id = kwargs.get('id', '')
        self.title = kwargs['title']
        self.direction = kwargs['direction']
        self.code_direction = kwargs['code_direction']
        self.start_year = kwargs['start_year']
        self.end_year = kwargs['end_year']
        self.base_id = kwargs.get('base_id', '')

    def to_json(self):
        return json.dumps({
            'external_id': self.external_id,
            'title': self.title,
            'direction': self.direction,
            'code_direction': self.code_direction,
            'start_year': self.start_year,
            'end_year': self.end_year
        })

    @staticmethod
    def list_from_json(data_list, unit_id=''):
        unit_list = []
        for data in data_list:
            unit_list.append(EducationalProgram(**data))
        return unit_list

    def get_values(self):
        columns = []
        values = []
        for key, val in self.__dict__.items():
            # if key not in ['']:
            columns.append(key)
            values.append(str(val))
        return columns, values


class StudyPlans(ScosUnit):
    table_name = 'study_plans'

    def __init__(self, **kwargs):
        self.external_id = kwargs.get('external_id', '')
        self.id = kwargs.get('id', '')
        self.title = kwargs['title']
        self.direction = kwargs['direction']
        self.code_direction = kwargs['code_direction']
        self.start_year = kwargs['start_year']
        self.end_year = kwargs['end_year']
        self.education_form = kwargs['education_form']
        self.educational_program_id = kwargs['educational_program_id']
        self.base_id = kwargs.get('base_id', '')

    def to_json(self):
        return json.dumps({
            'external_id': self.external_id,
            'title': self.title,
            'direction': self.direction,
            'code_direction': self.code_direction,
            'start_year': self.start_year,
            'end_year': self.end_year,
            'education_form': self.education_form,
            'educational_program': self.educational_program_id,
            'id': self.id
        })

    @staticmethod
    def list_from_json(data_list, unit_id=''):
        sp_list = []
        for data in data_list:
            sp_list.append(StudyPlans(**data))

        return sp_list

    def get_values(self):
        columns = []
        values = []
        for key, val in self.__dict__.items():
            # if key not in ['study_plan']:
            columns.append(key)
            values.append(str(val))
        return columns, values


class Disciplines(ScosUnit):
    table_name = 'disciplines'

    def __init__(self, **kwargs):
        self.external_id = kwargs.get('external_id', '')
        self.id = kwargs.get('id', '')
        self.title = kwargs['title']
        self.base_id = kwargs.get('base_id', '')
        self.study_plan = kwargs.get('study_plan', '')

    def to_json(self):
        return json.dumps({
            'external_id': self.external_id,
            'title': self.title,
            'id': self.id
        })

    @staticmethod
    def list_from_json(data_list, unit_id=''):
        unit_list = []
        for data in data_list:
            unit_list.append(Disciplines(**data))
        return unit_list

    def get_values(self):
        columns = []
        values = []
        for key, val in self.__dict__.items():
            if key not in ['study_plan']:
                columns.append(key)
                values.append(str(val))
        return columns, values


class StudyPlanDisciplines(ScosUnit):
    table_name = 'study_plan_disciplines'

    def __init__(self, **kwargs):
        self.study_plan = kwargs['study_plan']
        self.discipline = kwargs['discipline']
        self.semester = kwargs['semester']

    def to_json(self):
        return json.dumps({
            'study_plan': self.study_plan,
            'discipline': self.discipline,
            'semester': self.semester
        })

    @staticmethod
    def list_from_json(data_list, unit_id=''):
        unit_list = []
        for data in data_list:
            if unit_id:
                data.study_plan = unit_id
            unit_list.append(StudyPlanDisciplines(**data))
        return unit_list

    def get_values(self):
        columns = []
        values = []
        for key, val in self.__dict__.items():
            if key not in ['']:
                columns.append(key)
                values.append(str(val))
        return columns, values

class Students(ScosUnit):
    table_name = 'students'

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.external_id = kwargs['external_id']
        self.surname = kwargs['surname']
        self.name = kwargs['name']
        self.middle_name = kwargs['middle_name']
        # self.date_of_birth = date_of_birth
        self.snils = kwargs['snils']
        self.inn = kwargs['inn']
        self.email = kwargs['email']
        self.phone = kwargs['phone']
        self.study_year = kwargs['study_year']

    def to_json(self):
        return json.dumps({'organization_id': ORG_ID,
                           'external_id': self.external_id,
                           'surname': self.surname,
                           'name': self.name,
                           'middle_name': self.middle_name,
                           # 'date_of_birth': self.date_of_birth,
                           'snils': self.snils,
                           'inn': self.inn,
                           'email': self.email,
                           'phone': self.phone,
                           'study_year': self.study_year
                           })

    @staticmethod
    def list_from_json(data_list, unit_id=''):          # TODO Убрать возврат двух элементов
        unit_list = []
        sp_list = []
        for data in data_list:
            unit_list.append(Students(**data))
            try:
                for sp in data['study_plans']:
                    sp_list.append(StudyPlanStudents(study_plan=sp['id'], student=data['id']))
            except KeyError as k_error:          # При создании экземпляра из данных выбранных из локальной базы,
                if k_error.__str__() != 'study_plans':    # данные приходят без вложенного study_plans, для избежания ошибки
                    logger.error(f'Нет ключа {k_error}')  # игнорим это исключение
        return unit_list, sp_list


class StudyPlanStudents(ScosUnit):
    table_name = 'study_plan_students'

    def __init__(self, study_plan, student):
        self.study_plan = study_plan
        self.student = student

    def to_json(self):
        return json.dumps({'study_plan': self.study_plan,
                           'student': self.student})


class ContingentFlow(ScosUnit):
    table_name = 'contingent_flows'

    def __init__(self, **kwargs):
        self.student = kwargs['student_id']
        self.contingent_flow = kwargs['contingent_flow']
        self.flow_type = kwargs['flow_type']
        self.date = kwargs['date']
        self.faculty = kwargs['faculty']
        self.education_form = kwargs['education_form']
        self.form_fin = kwargs['form_fin']
        self.details = kwargs['details']
        self.id = kwargs['id']

    @staticmethod
    def list_from_json(data_list, unit_id=''):
        unit_list = []
        for data in data_list:
            unit_list.append(ContingentFlow(**data))
        return unit_list


class Marks(ScosUnit):
    table_name = 'marks'

    def __init__(self, **kwargs):
        self.external_id = kwargs['external_id']
        self.id = kwargs['id']
        try:            # TODO Переделать на один try
            self.discipline = kwargs['discipline']['external_id']
        except TypeError:
            self.discipline = kwargs['discipline']
        try:
            self.study_plan = kwargs['study_plan']['external_id']
        except TypeError:
            self.study_plan = kwargs['study_plan']
        try:
            self.student = kwargs['student']['external_id']
        except TypeError:
            self.student = kwargs['student']
        self.mark_type = kwargs['mark_type']
        try:
            self.mark_value = kwargs['value']
        except KeyError:
            self.mark_value = kwargs['mark_value']

        self.semester = kwargs['semester']

    def to_json(self):
        return json.dumps({'organization_id': ORG_ID,
                           'external_id': self.external_id,
                           'discipline': self.discipline,
                           'study_plan': self.study_plan,
                           'student': self.student,
                           'mark_type': self.mark_type,
                           'mark_value': int(self.mark_value),
                           'semester': int(self.semester)
                           })

    @staticmethod
    def list_from_json(data_list, unit_id=''):
        unit_list = []
        for data in data_list:
            unit_list.append(Marks(**data))
        return unit_list


# Порядок имеет значение
data_classes = {
    'educational_programs': EducationalProgram,
    'study_plans': StudyPlans,
    'disciplines': Disciplines,
    'study_plan_disciplines': StudyPlanDisciplines,
    'students': Students,
    'study_plan_students': StudyPlanStudents,
    'contingent_flows': ContingentFlow,
    'marks': Marks,
}
