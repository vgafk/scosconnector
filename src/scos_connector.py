import json
from datetime import datetime

from loguru import logger
import requests
import settings
from exceptions import SCOSAccessError, SCOSAddError, OperationTypeError

headers = {'Content-Type': 'application/json', 'X-CN-UUID': settings.X_CN_UUID}

# Общий формат url
API_URL = 'https://test.online.edu.ru/'  # тестовый контур
# API_URL = 'https://online.edu.ru/api/'     # боевой контур
API_URL_V1 = API_URL + 'api/v1/'
API_URL_V2 = API_URL + 'vam/api/v2/'

CHECK_CONNECTION_URL = API_URL_V1 + 'connection/check'      # Проверка подключения

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


def get_endpoint_url(unit, action_type: str = 'add') -> str:
    match action_type:
        case 'add':
            return endpoint_urls[unit.__tablename__]
        case 'upd' | 'del':
            if unit.__tablename__ == 'study_plan_disciplines':
                return f"{endpoint_urls['study_plans']}/{unit.study_plans.external_id}/" \
                       f"disciplines/{unit.disciplines.external_id}"
            elif unit.__tablename__ == 'study_plan_students':
                return f"{endpoint_urls['students']}/{unit.students.external_id}/" \
                       f"study_plans/{unit.study_plans.external_id}"
            else:
                return f"{endpoint_urls[unit.__tablename__]}/{unit.scos_id}"
        case 'load':
            pass
        case _:
            raise OperationTypeError("Неизвестная операция, используйте 'add', 'upd' или 'del'")


def check_connection():
    resp = requests.get(CHECK_CONNECTION_URL, headers=headers)
    if resp.status_code < 200 or resp.status_code > 300:
        raise SCOSAccessError(f'Сервер СЦОС недоступен: {resp.text}')


def create_add_request_row(unit) -> str:
    request_row = f'{{"organization_id": "{settings.ORG_ID}", ' \
                  f'"{unit.__tablename__}": [{unit.to_json()}]}}'
    return request_row


# def create_update_request_row(unit) -> str:
#     request_row = f'{{"organization_id": "{settings.ORG_ID}", ' \
#                   f'{unit.to_json()}'
#     return request_row


def get_new_scos_id(resp):
    if resp.status_code < 200 or resp.status_code > 300:
        raise SCOSAddError(f'Ошибка внесения данных в СЦОС:\n body = {resp.request.body}\n '
                           f'url = {resp.url}\n '
                           f'error = {resp.text}')
    resp_json = resp.json()['results'][0]
    scos_id = resp_json['id']
    if scos_id is None:
        raise SCOSAddError(f'При загрузке получены неверные данные:\n body = {resp.request.body}\n '
                           f"uploadStatusType = {resp_json['uploadStatusType']}, "
                           f"additional_info = {resp_json['additional_info']}")
    return scos_id


def send_to_scos(unit, action_type: str):
    if action_type == 'add':
        body = create_add_request_row(unit)
        resp = requests.post(get_endpoint_url(unit), headers=headers, data=body)
        unit.scos_id = get_new_scos_id(resp)
    elif action_type == 'upd':
        body = unit.to_json()                           # create_update_request_row(unit)
        resp = requests.put(get_endpoint_url(unit, action_type='upd'), headers=headers, data=body)
    else:
        resp = requests.delete(get_endpoint_url(unit, action_type='del'), headers=headers)
    unit.last_scos_update = datetime.now()
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
#             last_page = resp_json['last_page']
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
    print(get_endpoint_url('', 'upd'))