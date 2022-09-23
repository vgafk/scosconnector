from enum import Enum

# Форма обучения
education_form = {'Заочная': 'EXTRAMURAL', 'Очная': 'FULL_TIME','Очнозаочная': 'PART_TIME',
                  'Сок.заочная': 'SHORT_EXTRAMURAL', 'Сок.очная': 'SHORT_FULL_TIME', 'Экстернат': 'EXTERNAL'}

# Движение студентов
flow_types = {'Зачисление': 'ENROLLMENT', 'Отчисление': 'DEDUCTION',
              'Перевод': 'TRANSFER', 'Восстановление': 'REINSTATEMENT',
              'Академ': 'SABBATICAL_TAKING'}

# Типы оценок
marks_types = {'Оценка': 'MARK', 'Зачет': 'CREDIT', 'Диф.зачет': 'DIF_CREDIT',
               '100оценка': 'HUNDRED_POINT'}


# Префиксы файлов для определения действия в данными в файле
class ActionsList(Enum):
    """a_ добавление, u_ обновление, d_ удаление"""
    ADD = 'a'
    UPD = 'u'
    DEL = 'd'

    @classmethod
    def list_values(cls):
        return list(map(lambda x: x.value, cls))
