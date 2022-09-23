from datetime import datetime
from loguru import logger
import requests
from requests import Response

from settings import Settings
from exceptions import SCOSAccessError, SCOSAddError, OperationTypeError
from local_base import LocalBase
from scos_dictionaries import ActionsList
from models import Base

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

    def __get_endpoint_url(self, unit: LocalBase.base, action_type: ActionsList) -> str:
        """
        Формирование endpoint'a на основании действия и типа передаваемых данных('__tablename__')

        :param unit: 'эеземпляр сущности из БД
        :param action_type: действие: 'add' - добавить, 'upd' - обновить, 'del' - удалить
        :return: ссылка на сервере СЦОС
        """
        match action_type:
            case ActionsList.ADD:
                return self.endpoint_urls[unit.__tablename__]
            case ActionsList.UPD | ActionsList.DEL:
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
    def __create_add_request_row(unit: Base) -> str:
        """
        Формирование строки тела запроса, используется при добавлении записей пакетом
        :param unit:
        :return: Строка тела запроса к серверу СЦОС
        """
        request_row = f'{{"organization_id": "{Settings().get_org_id()}", ' \
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
    def add_to_scos(self, unit: Base) -> Response:
        """
        Добавляем запись в СЦОС
        :param unit:
        :return: Ответ сервера
        """
        body = self.__create_add_request_row(unit)
        resp = requests.post(self.__get_endpoint_url(unit, action_type=ActionsList.ADD), headers=headers, data=body)
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
    def update_in_scos(self, unit: Base) -> Response:
        """
        Обновляем запись в СЦОС
        :param unit:
        :return: Ответ сервера
        """
        body = unit.to_json()
        resp = requests.put(self.__get_endpoint_url(unit, action_type=ActionsList.UPD), headers=headers, data=body)
        unit.last_scos_update = datetime.now()
        return resp

    @scos_request
    def delete_from_scos(self, unit: Base) -> Response:
        """
        Удаляем запись из СЦОС
        :param unit:
        :return: Ответ сервера
        """
        resp = requests.delete(self.__get_endpoint_url(unit, action_type=ActionsList.DEL), headers=headers)
        unit.deleted_scos = datetime.now()
        return resp



if __name__ == '__main__':
    pass
