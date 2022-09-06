import requests
import json

import local_base
import settings
from settings import CHECK_CONNECTION, endpoint_urls
from scos_units import ScosUnit, data_classes

headers = {'Content-Type': 'application/json', 'X-CN-UUID': settings.X_CN_UUID}


def check_connection():
    resp = requests.get(CHECK_CONNECTION, headers=headers)
    return resp.status_code, resp.text


def get_data_from_scos(data_type: str, unit_id: str = '', added_unit: str = ''):
    page = 0
    last_page = 1
    results = []
    while page < last_page:
        url = endpoint_urls[data_type]
        if unit_id:
            url += f'/{unit_id}'
        if added_unit:
            url += f'/{added_unit}'
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
    get_educational_programs_from_scos()
    get_disciplines_from_scos()
    get_study_plans_from_scos()
    get_students_from_scos()
    get_marks_from_scos()


def get_educational_programs_from_scos():
    programs_from_scos = get_data_from_scos('educational_programs')
    programs_list = data_classes['educational_programs'].list_from_json(programs_from_scos)
    for program in programs_list:
        local_base.write_to_base(program, 'educational_programs', 'a')


def get_disciplines_from_scos():
    disciplines_from_scos = get_data_from_scos('disciplines')
    disciplines_list = data_classes['disciplines'].list_from_json(disciplines_from_scos)
    for discipline in disciplines_list:
        local_base.write_to_base(discipline, 'disciplines', 'a')


def get_study_plans_from_scos():
    study_plans_from_scos = get_data_from_scos('study_plans')
    study_plans_list = data_classes['study_plans'].list_from_json(study_plans_from_scos)
    for study_plan in study_plans_list:
        local_base.write_to_base(study_plan, 'study_plans', 'a')
        get_study_plans_disciplines_from_scos(study_plan.scos_id)


def get_study_plans_disciplines_from_scos(study_plan: str):
    study_plans_disciplines_from_scos = get_data_from_scos('study_plans', study_plan, 'disciplines')
    study_plans_disciplines_list = data_classes['study_plan_disciplines'].get_list(study_plan,
                                                                                   study_plans_disciplines_from_scos)
    for study_plan_disciplines in study_plans_disciplines_list:
        local_base.write_to_base(study_plan_disciplines, 'study_plan_disciplines', 'a')


def get_students_from_scos():
    students_from_scos = get_data_from_scos('students')
    students_list, study_plans_list = data_classes['students'].list_from_json(students_from_scos)
    for student in students_list:
        local_base.write_to_base(student, 'students', 'a')
        get_contingent_flows_from_scos(student.scos_id)
    for study_plans in study_plans_list:
        local_base.write_to_base(study_plans, 'study_plan_students', 'a')


def get_contingent_flows_from_scos(student: str):
    contingent_flows_from_scos = get_data_from_scos('students', student, 'contingent_flows')
    contingent_flows_list = data_classes['contingent_flows'].get_list(student, contingent_flows_from_scos)
    for contingent_flows in contingent_flows_list:
        local_base.write_to_base(contingent_flows, 'contingent_flows', 'a')


def get_marks_from_scos():
    marks_from_scos = get_data_from_scos('marks')
    marks_list = data_classes['marks'].list_from_json(marks_from_scos)
    for marks in marks_list:
        local_base.write_to_base(marks, 'marks', 'a')


def add_data(data_type: str):
    return send_add_request(data_type, data_classes[data_type])


def update_all_data():
    update_data('students')


def update_data(data_type: str):
    updated_data = local_base.get_updated_data('students')
#     return send_update_request(data_type, data_classes[data_type])


def create_request_row(title: str, units: list[ScosUnit]) -> str:
    request_row = f'{{"organization_id": "{settings.ORG_ID}", ' \
                  f'"{title}": {[ob.to_json() for ob in units]}}}'
    return request_row


def send_add_request(json_parameter: str, scos_unit: ScosUnit):             # TODO переписать на вызов из базы
    # Файл должен называться как параметр, потому просто добавляем расширение csv
    json_parameter_data = scos_unit.from_file(json_parameter + '.csv')
    body = create_request_row(json_parameter, json_parameter_data)
    resp = requests.post(endpoint_urls[json_parameter], headers=headers,
                         data=body)
    return resp.status_code, resp.text


# def send_update_request(json_parameter: str, scos_unit: ScosUnit):
    # Файл должен называться как параметр плюс _u на конце, потому просто добавляем расширение csv
    # scos_units = scos_unit.from_file(json_parameter + '_u.csv')
    # for unit in scos_units:
        # unit_id = get_unit_id(json_parameter, unit)
        # unit.organization_id = settings.ORG_ID      # добавляем id организации для упрощения формирования json строки
        # body = json.dumps(unit.__dict__)
        # print(f'{endpoint_urls[json_parameter]}/{unit_id}')
        # print(body)
        # resp = requests.put(f'{endpoint_urls[json_parameter]}/{unit_id}', headers=headers, data=body)
        # print(resp.status_code, resp.text)
    # return 'done'



parameter = {'1': 'educational_programs', '2': 'study_plans', '3': 'disciplines', '4': 'study_plan_disciplines',
             '5': 'students', '6': 'study_plan_students', '7': 'contingent_flows', '8': 'marks'}


if __name__ == '__main__':
    # print(check_connection())
    # print(add_data(parameter['0']))
    # print(update_data(parameter['8']))
    # get_data_from_scos(parameter['8'])
    # get_all_data_from_scos()
    update_all_data()