import json
from datetime import datetime

from loguru import logger
import requests
from settings import Settings
from exceptions import SCOSAccessError, SCOSAddError, OperationTypeError
from local_base import LocalBase

headers = {'Content-Type': 'application/json', 'X-CN-UUID': Settings().get_x_cn_uuid()}

# Общий формат url
API_URL = 'https://test.online.edu.ru/'  # тестовый контур
# API_URL = 'https://online.edu.ru/api/'     # боевой контур
API_URL_V1 = API_URL + 'api/v1/'
API_URL_V2 = API_URL + 'vam/api/v2/'

CHECK_CONNECTION_URL = API_URL_V1 + 'connection/check'  # Проверка подключения


class SCOSConnector:
    # Конкретные endpoints
    # Название параметра и url могут отличаться, например study_plan_disciplines без s в plan
    endpoint_urls = {
        'educational_programs': API_URL_V2 + 'educational_programs',
        'study_plans': API_URL_V2 + 'study_plans',
        'disciplines': API_URL_V2 + 'disciplines',
        'study_plan_disciplines': API_URL_V2 + 'study_plans_disciplines',
        'students': API_URL_V2 + 'students',
        'study_plan_students': API_URL_V2 + 'study_plans_students',
        'contingent_flows': API_URL_V2 + 'contingent_flows',
        'marks': API_URL_V2 + 'marks'
    }

    def __get_endpoint_url(self, unit: LocalBase.Base, action_type: str) -> str:
        """
        Формирование endpoint'a на основании действия и типа передаваемых данных('__tablename__')

        :param unit: 'эеземпляр сущности из БД
        :param action_type: действие: 'add' - добавить, 'upd' - обновить, 'del' - удалить
        :return: ссылка на сервере СЦОС
        """
        match action_type:
            case 'add':
                return self.endpoint_urls[unit.__tablename__]
            case 'upd' | 'del':
                if unit.__tablename__ == 'study_plan_disciplines':  # Связь учебных планов и дисциплин идет через планы
                    return f"{self.endpoint_urls['study_plans']}/{unit.study_plan.scos_id}/" \
                           f"disciplines/{unit.discipline.scos_id}?semester={unit.semester}"
                elif unit.__tablename__ == 'study_plan_students':  # Связь планов и студентов идет через студентов
                    return f"{self.endpoint_urls['students']}/{unit.student.scos_id}/" \
                           f"study_plans/{unit.study_plan.scos_id}"
                else:
                    return f"{self.endpoint_urls[unit.__tablename__]}/{unit.scos_id}"
            case 'load':
                return f"{self.endpoint_urls[unit.__tablename__]}"
            case _:
                raise OperationTypeError("Неизвестная операция, используйте 'add', 'upd' или 'del'")

    @staticmethod
    def check_connection():
        """Проверка подключения"""
        resp = requests.get(CHECK_CONNECTION_URL, headers=headers)
        if resp.status_code < 200 or resp.status_code > 300:
            raise SCOSAccessError(f'Сервер СЦОС недоступен: {resp.text}')

    @staticmethod
    def __create_add_request_row(unit) -> str:
        """Формирование строки тела запроса, используется при добавлении записей пакетом """
        request_row = f'{{"organization_id": "{settings.ORG_ID}", ' \
                      f'"{unit.__tablename__}": [{unit.to_json()}]}}'  # Формируется список из unit.to_json()
        return request_row

    @staticmethod
    def scos_request(fun):
        def wrapper(self, unit):
            resp = fun(self, unit)
            if resp.status_code < 200 or resp.status_code > 300:
                raise SCOSAddError(f'Ошибка внесения данных в СЦОС:\n body = {resp.request.body}\n '
                                   f'url = {resp.url}\n '
                                   f'error = {resp.text}')
            return resp

        return wrapper

    @scos_request
    def __add_to_scos(self, unit):
        body = self.__create_add_request_row(unit)
        resp = requests.post(self.__get_endpoint_url(unit, action_type='add'), headers=headers, data=body)
        unit.last_scos_update = datetime.now()  # Устанавливаем дату и время добавления в СЦОС
        resp_json = resp.json()['results'][0]
        scos_id = resp_json['id']
        if scos_id is None:
            raise SCOSAddError(f'При загрузке получены неверные данные:\n body = {resp.request.body}\n '
                               f"uploadStatusType = {resp_json['uploadStatusType']}, "
                               f"additional_info = {resp_json['additional_info']}")
        unit.scos_id = scos_id
        return resp

    @scos_request
    def __update_in_scos(self, unit):
        body = unit.to_json()
        resp = requests.put(self.__get_endpoint_url(unit, action_type='upd'), headers=headers, data=body)
        unit.last_scos_update = datetime.now()
        return resp

    @scos_request
    def __delete_from_scos(self, unit):
        resp = requests.delete(self.__get_endpoint_url(unit, action_type='del'), headers=headers)
        unit.deleted_scos = datetime.now()
        return resp

    def send_to_scos(self, unit, action_type: str):
        if action_type == 'add':
            resp = self.__add_to_scos(unit)
        elif action_type == 'upd':
            resp = self.__update_in_scos(unit)
        else:
            resp = self.__delete_from_scos(unit)
        logger.info(resp.text)
        return resp.status_code, resp.text


# def get_data_from_scos(data_type: str, unit_id: str = ''):
#     page = 0
#     last_page = 1
#     results = []
#     while page < last_page:
#         url = endpoint_urls[data_type]
#         if unit_id:
#             url = url.replace('%unit_id', unit_id)
#         resp_json = requests.get(url, headers=headers).json()
#         try:
#             results.extend(resp_json['results'])
#             page = resp_json['page']
#             last_page = resp_json['last_page']`
#         except Exception as error:
#             print(error)
#             break
#     return results
#
#
# def get_all_data_from_scos():
#     all_data = get_scos_units_list('educational_programs')
#     study_plans = get_scos_units_list('study_plans')
#     all_data.extend(study_plans)
#     all_data.extend(get_scos_units_list('disciplines'))
#     students, study_plan_students = get_scos_units_list('students')     # TODO сделать по отдельности
#     all_data.extend(students)
#     all_data.extend(study_plan_students)
#     all_data.extend(get_scos_units_list('marks'))
#     for study_plan in study_plans:
#         all_data.extend(get_scos_units_list('study_plan_disciplines', study_plan.id))
#     for student in students:
#         all_data.extend(get_scos_units_list('contingent_flows', student.id))
#     return all_data
#
#
# def get_scos_units_list(unit_type: str, unit_id: str = ''):
#     unit_data_from_scos = get_data_from_scos(unit_type, unit_id)
#     unit_list = data_classes[unit_type].list_from_json(unit_data_from_scos, unit_id=unit_id)
#     return unit_list
#
#
# def get_study_plans_disciplines_from_scos(study_plan: str):
#     study_plans_disciplines_from_scos = get_data_from_scos('study_plans', study_plan, 'disciplines')
#     study_plans_disciplines_list = data_classes['study_plan_disciplines'].get_list(study_plan,
#                                                                                    study_plans_disciplines_from_scos)
#     for study_plan_disciplines in study_plans_disciplines_list:
#         local_base.insert(study_plan_disciplines)
#
#
# def get_students_from_scos():
#     students_from_scos = get_data_from_scos('students')
#     students_list, study_plans_list = data_classes['students'].list_from_json(students_from_scos)
#     for student in students_list:
#         local_base.insert(student)
#         get_contingent_flows_from_scos(student.scos_id)
#     for study_plans in study_plans_list:
#         local_base.insert(study_plans)
#
#
# def get_contingent_flows_from_scos(student: str):
#     contingent_flows_from_scos = get_data_from_scos('students', student, 'contingent_flows')
#     contingent_flows_list = data_classes['contingent_flows'].get_list(student, contingent_flows_from_scos)
#     for contingent_flows in contingent_flows_list:
#         local_base.insert(contingent_flows)
#
#
# def get_marks_from_scos():
#     marks_from_scos = get_data_from_scos('marks')
#     marks_list = data_classes['marks'].list_from_json(marks_from_scos)
#     for marks in marks_list:
#         local_base.insert(marks)
#
#
# def add_data(data_type: str):
#     return send_add_request(data_type, data_classes[data_type])
#
#
# def update_data(updated_data: [ScosUnit]):
#     for unit in updated_data:
#         send_update_request(unit)
#
#
# # def create_request_row(title: str, units: list[ScosUnit]) -> str:
# #     request_row = f'{{"organization_id": "{settings.ORG_ID}", ' \
# #                   f'"{title}": {[ob.to_json() for ob in units]}}}'
# #     return request_row
#
#
# def delete_data(deleted_data: [ScosUnit]):
#     for unit in deleted_data:
#         send_delete_request(unit)
#
#
# def create_request_row(units: list, title: str):
#     request_row = f'{{"organization_id": "{settings.ORG_ID}", ' \
#                       f'"{title}": {[ob.to_json() for ob in units]}}}'
#     return request_row
#
#
# def send_add_request(json_parameter: str, scos_unit: ScosUnit):  # TODO переписать на вызов из базы
#     # Файл должен называться как параметр, потому просто добавляем расширение csv
#     # json_parameter_data = scos_unit.from_file(json_parameter + '.csv')
#     # body = create_request_row(json_parameter, json_parameter_data)
#     # resp = requests.post(endpoint_urls[json_parameter], headers=headers,
#     #                      data=body)
#     # return resp.status_code, resp.text
#     pass
#
#
# def send_update_request(scos_unit: ScosUnit):
#     body = scos_unit.to_json()
#     url = endpoint_urls[scos_unit.get_table()] + '/' + scos_unit.id
#     resp = requests.put(url, headers=headers, data=body)
#     if resp.status_code not in API_codes['Success']:
#         logger.error(f'Ошибка обновления из таблицы {scos_unit.get_table()} запросом: {body}')
#         logger.error(str(resp.status_code), resp.text)
#     else:
#         logger.info(f'обновление из таблицы {scos_unit.get_table()} запросом: {body}')
#     return resp.status_code, resp.text
#
#
# def send_delete_request(scos_unit:  ScosUnit):
#     url = endpoint_urls[scos_unit.get_table()] + '/' + scos_unit.id
#     resp = requests.delete(url, headers=headers)
#     if resp.status_code not in API_codes['Success']:
#         logger.info(f'Ошибка удаления из таблицы {scos_unit.get_table()} по url {url}')
#         logger.error(str(resp.status_code), resp.text)
#     else:
#         logger.info(f'Удаление из таблицы {scos_unit.get_table()} по url {url}')
#     return resp.status_code, resp.text

if __name__ == '__main__':
    pass
