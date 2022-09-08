from loguru import logger
import requests


import local_base
import settings
from settings import CHECK_CONNECTION, endpoint_urls, API_codes
from scos_units import ScosUnit, data_classes

headers = {'Content-Type': 'application/json', 'X-CN-UUID': settings.X_CN_UUID}


def check_connection():
    resp = requests.get(CHECK_CONNECTION, headers=headers)
    return resp.status_code, resp.text


def get_data_from_scos(data_type: str, unit_id: str = ''):
    page = 0
    last_page = 1
    results = []
    while page < last_page:
        url = endpoint_urls[data_type]
        if unit_id:
            url = url.replace('%unit_id', unit_id)
        resp_json = requests.get(url, headers=headers).json()
        try:
            results.extend(resp_json['results'])
            page = resp_json['page']
            last_page = resp_json['last_page']
        except Exception as error:
            print(error)
            break
    return results


def get_all_data_from_scos():
    all_data = get_scos_units_list('educational_programs')
    study_plans = get_scos_units_list('study_plans')
    all_data.extend(study_plans)
    all_data.extend(get_scos_units_list('disciplines'))
    students, study_plan_students = get_scos_units_list('students')
    all_data.extend(students)
    all_data.extend(study_plan_students)
    all_data.extend(get_scos_units_list('marks'))
    for study_plan in study_plans:
        all_data.extend(get_scos_units_list('study_plan_disciplines', study_plan.id))
    for student in students:
        all_data.extend(get_scos_units_list('contingent_flows', student.id))
    return all_data


def get_scos_units_list(unit_type: str, unit_id: str = ''):
    unit_data_from_scos = get_data_from_scos(unit_type, unit_id)
    unit_list = data_classes[unit_type].list_from_json(unit_data_from_scos, unit_id=unit_id)
    return unit_list


def get_study_plans_disciplines_from_scos(study_plan: str):
    study_plans_disciplines_from_scos = get_data_from_scos('study_plans', study_plan, 'disciplines')
    study_plans_disciplines_list = data_classes['study_plan_disciplines'].get_list(study_plan,
                                                                                   study_plans_disciplines_from_scos)
    for study_plan_disciplines in study_plans_disciplines_list:
        local_base.insert(study_plan_disciplines)


def get_students_from_scos():
    students_from_scos = get_data_from_scos('students')
    students_list, study_plans_list = data_classes['students'].list_from_json(students_from_scos)
    for student in students_list:
        local_base.insert(student)
        get_contingent_flows_from_scos(student.scos_id)
    for study_plans in study_plans_list:
        local_base.insert(study_plans)


def get_contingent_flows_from_scos(student: str):
    contingent_flows_from_scos = get_data_from_scos('students', student, 'contingent_flows')
    contingent_flows_list = data_classes['contingent_flows'].get_list(student, contingent_flows_from_scos)
    for contingent_flows in contingent_flows_list:
        local_base.insert(contingent_flows)


def get_marks_from_scos():
    marks_from_scos = get_data_from_scos('marks')
    marks_list = data_classes['marks'].list_from_json(marks_from_scos)
    for marks in marks_list:
        local_base.insert(marks)


def add_data(data_type: str):
    return send_add_request(data_type, data_classes[data_type])


def update_data(updated_data: [ScosUnit]):
    for unit in updated_data:
        send_update_request(unit)


# def create_request_row(title: str, units: list[ScosUnit]) -> str:
#     request_row = f'{{"organization_id": "{settings.ORG_ID}", ' \
#                   f'"{title}": {[ob.to_json() for ob in units]}}}'
#     return request_row


def delete_data(deleted_data: [ScosUnit]):
    for unit in deleted_data:
        send_delete_request(unit)


def create_request_row(units: list, title: str):
    request_row = f'{{"organization_id": "{settings.ORG_ID}", ' \
                      f'"{title}": {[ob.to_json() for ob in units]}}}'
    return request_row


def send_add_request(json_parameter: str, scos_unit: ScosUnit):  # TODO переписать на вызов из базы
    # Файл должен называться как параметр, потому просто добавляем расширение csv
    # json_parameter_data = scos_unit.from_file(json_parameter + '.csv')
    # body = create_request_row(json_parameter, json_parameter_data)
    # resp = requests.post(endpoint_urls[json_parameter], headers=headers,
    #                      data=body)
    # return resp.status_code, resp.text
    pass


def send_update_request(scos_unit: ScosUnit):
    body = scos_unit.to_json()
    url = endpoint_urls[scos_unit.get_table()] + '/' + scos_unit.id
    resp = requests.put(url, headers=headers, data=body)
    if resp.status_code not in API_codes['Success']:
        logger.error(f'Ошибка обновления из таблицы {scos_unit.get_table()} запросом: {body}')
        logger.error(resp.status_code, resp.text)
    else:
        logger.info(f'обновление из таблицы {scos_unit.get_table()} запросом: {body}')
    return resp.status_code, resp.text


def send_delete_request(scos_unit:  ScosUnit):
    url = endpoint_urls[scos_unit.get_table()] + '/' + scos_unit.id
    resp = requests.delete(url, headers=headers)
    if resp.status_code not in API_codes['Success']:
        logger.info(f'Ошибка удаления из таблицы {scos_unit.get_table()} по url {url}')
        logger.error(resp.status_code, resp.text)
    else:
        logger.info(f'Удаление из таблицы {scos_unit.get_table()} по url {url}')
    return resp.status_code, resp.text
