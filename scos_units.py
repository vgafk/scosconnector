import csv
import json
from datetime import datetime
from select import select


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

    @classmethod
    def from_list(cls, values):
        return cls(*values)

    @classmethod
    def to_json(cls):
        pass

    @classmethod
    def query(cls, action: str):
        pass

    @staticmethod
    def list_from_json(data_list):
        pass

    @classmethod
    def from_file(cls, file_name: str):
        unit_list = []
        with open(file_name, 'r', newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=';')
            next(data, None)  # пропускаем строку с заголовками
            for row in data:
                unit_list.append(cls.from_list(row))
        return unit_list


class EducationalProgram(ScosUnit):
    def __init__(self, title: str, direction: str, code_direction: str, start_year: str,
                 end_year: str, scos_id: str = '', external_id: str = ''):
        self.external_id = external_id
        self.title = title
        self.direction = direction
        self.code_direction = code_direction
        self.start_year = start_year
        self.end_year = end_year
        self.scos_id = scos_id
        self.last_scos_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def to_json(self):
        return json.dumps({
            'external_id': self.external_id,
            'title': self.title,
            'direction': self.direction,
            'code_direction': self.code_direction,
            'start_year': self.start_year,
            'end_year': self.end_year,
            'id': self.scos_id
        })

    @staticmethod
    def list_from_json(data_list):
        unit_list = []
        for data in data_list:
            unit_list.append(EducationalProgram(data['title'],
                                                data['direction'],
                                                data['code_direction'],
                                                data['start_year'],
                                                data['end_year'],
                                                data['id'],
                                                data['external_id']))
        return unit_list


class StudyPlans(ScosUnit):
    def __init__(self, external_id: str, title: str, direction: str, code_direction: str, start_year: str,
                 end_year: str, education_form: str, educational_program: str, scos_id: str = ''):
        self.external_id = external_id
        self.title = title
        self.direction = direction
        self.code_direction = code_direction
        self.start_year = start_year
        self.end_year = end_year
        self.education_form = education_form
        self.educational_program_scos_id = educational_program
        self.scos_id = scos_id
        self.last_scos_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def to_json(self):
        return json.dumps({
            'external_id': self.external_id,
            'title': self.title,
            'direction': self.direction,
            'code_direction': self.code_direction,
            'start_year': self.start_year,
            'end_year': self.end_year,
            'education_form': self.education_form,
            'educational_program': self.educational_program_scos_id,
            'id': self.scos_id
        })

    @staticmethod
    def list_from_json(data_list):
        sp_list = []
        for data in data_list:
            sp_list.append(StudyPlans(data['external_id'],
                                      data['title'],
                                      data['direction'],
                                      data['code_direction'],
                                      data['start_year'],
                                      data['end_year'],
                                      data['education_form'],
                                      data['educational_program_id'],
                                      data['id']))

        return sp_list


class Disciplines(ScosUnit):
    def __init__(self, external_id: str, title: str, scos_id: str = 0):
        self.external_id = external_id
        self.title = title
        self.scos_id = scos_id
        self.last_scos_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def to_json(self):
        return json.dumps({
            'external_id': self.external_id,
            'title': self.title,
            'id': self.scos_id
        })

    @staticmethod
    def list_from_json(data_list):
        unit_list = []
        for data in data_list:
            unit_list.append(Disciplines(data['external_id'],
                                         data['title'],
                                         data['id']))
        return unit_list


class StudyPlanDisciplines(ScosUnit):
    def __init__(self, study_plan: str, discipline: str, semester: int):
        self.study_plan_scos_id = study_plan
        self.discipline_scos_id = discipline
        self.semester = str(semester)
        self.last_scos_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def to_json(self):
        return json.dumps({
            'study_plan': self.study_plan_scos_id,
            'discipline': self.discipline_scos_id,
            'semester': int(self.semester)
        })

    @staticmethod
    def get_list(study_plan: str, data_list):
        unit_list = []
        for data in data_list:
            unit_list.append(StudyPlanDisciplines(study_plan, data['discipline'], data['semester']))
        return unit_list


class Students(ScosUnit):
    def __init__(self, external_id: str, surname: str, name: str, middle_name: str,  # date_of_birth: str,
                 snils: str, inn: str, email: str, study_year: str, scos_id: str = ''):
        self.external_id = external_id
        self.surname = surname
        self.name = name
        self.middle_name = middle_name
        # self.date_of_birth = date_of_birth
        self.snils = snils
        self.inn = inn
        self.email = email
        self.study_year = str(study_year)
        self.scos_id = scos_id
        self.last_scos_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def to_json(self):
        return json.dumps({'external_id': self.external_id,
                           'surname': self.surname,
                           'name': self.name,
                           'middle_name': self.middle_name,
                           # 'date_of_birth': self.date_of_birth,
                           'snils': self.snils,
                           'inn': self.inn,
                           'email': self.email,
                           'study_year': int(self.study_year)
                           })

    @staticmethod
    def list_from_json(data_list):
        unit_list = []
        sp_list = []
        for data in data_list:
            unit_list.append(Students(data['external_id'],
                                      data['surname'],
                                      data['name'],
                                      data['middle_name'],
                                      # data['dateOfBirth'],
                                      data['snils'],
                                      data['inn'],
                                      data['email'],
                                      data['study_year'],
                                      data['id']))
            for sp in data['study_plans']:
                sp_list.append(StudyPlanStudents(data['id'], sp['id']))

        return unit_list, sp_list


class StudyPlanStudents(ScosUnit):
    def __init__(self, study_plan: str, student: str):
        self.study_plan_scos_id = study_plan
        self.student_scos_id = student


class ContingentFlow(ScosUnit):
    def __init__(self, student: str, contingent_flow: str, flow_type: str, date: str, faculty: str, education_form: str,
                 form_fin: str, details: str, scos_id: str = ''):
        self.student_scos_id = student
        self.contingent_flow = contingent_flow
        self.flow_type = flow_type
        self.date = date
        self.faculty = faculty
        self.education_form = education_form
        self.form_fin = form_fin
        self.details = details
        self.scos_id = scos_id
        self.last_scos_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_list(student: str, data_list):
        unit_list = []
        for data in data_list:
            unit_list.append(ContingentFlow(data['student_id'],
                                            data['contingent_flow'],
                                            data['flow_type'],
                                            data['date'],
                                            data['faculty'],
                                            data['education_form'],
                                            data['form_fin'],
                                            data['details'],
                                            data['id']))
        return unit_list


class Marks(ScosUnit):
    def __init__(self, discipline: str, study_plan: str, student: str, mark_type: str, mark_value: str, semester: str,
                 scos_id: str = ''):
        self.discipline = discipline
        self.study_plan = study_plan
        self.student = student
        self.mark_type = mark_type
        self.mark_value = str(mark_value)
        self.semester = str(semester)
        self.scos_id = scos_id
        self.last_scos_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def to_json(self):
        return json.dumps({'discipline': self.discipline,
                           'study_plan': self.study_plan,
                           'student': self.student,
                           'mark_type': self.mark_type,
                           'mark_value': int(self.mark_value),
                           'semester': int(self.semester)
                           })

    @staticmethod
    def list_from_json(data_list):
        unit_list = []
        for data in data_list:
            unit_list.append(Marks(data['discipline']['external_id'],
                                   data['study_plan']['external_id'],
                                   data['student']['external_id'],
                                   data['mark_type'],
                                   data['value'],
                                   data['semester'],
                                   data['id']))
        return unit_list


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
