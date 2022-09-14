from scos_units import ScosUnit, data_classes
from functools import singledispatch
import uuid
from local_base_old import get_external_id


@singledispatch
def normalize(arg):
    return arg


@normalize.register
def norm_list(units: list):
    for unit in units:
        norm_single(unit)


@normalize.register
def norm_single(unit: ScosUnit):
    if isinstance(unit, data_classes.get('educational_programs')):
        norm_educational_programs(unit)
    elif isinstance(unit, data_classes.get('study_plans')):
        norm_study_plans(unit)
    elif isinstance(unit, data_classes.get('disciplines')):
        norm_disciplines(unit)
    elif isinstance(unit, data_classes.get('study_plan_disciplines')):
        norm_study_plans_disciplines(unit)
    elif isinstance(unit, data_classes.get('study_plan_students')):
        pass
    elif isinstance(unit, data_classes.get('contingent_flows')):
        pass
    elif isinstance(unit, data_classes.get('marks')):
        pass


def norm_educational_programs(unit: ScosUnit):
    # проверяем есть ли у программы в external_id, если нет, генерируем новый
    if external_id := get_external_id('educational_programs', unit.base_id):
        unit.external_id = external_id
    else:
        unit.external_id = str(uuid.uuid4())
    return unit


def norm_study_plans(unit: ScosUnit):
    # проверяем есть ли у программы в external_id, если нет, генерируем новый
    if external_id := get_external_id('study_plans', unit.base_id):
        unit.external_id = external_id
    else:
        unit.external_id = str(uuid.uuid4())
    unit.educational_program_id = get_external_id('educational_programs', unit.educational_program_id)
    return unit


def norm_disciplines(unit: ScosUnit):
    if external_id := get_external_id('disciplines', unit.base_id):
        unit.external_id = external_id
    else:
        unit.external_id = str(uuid.uuid4())
    unit.study_plan = get_external_id('study_plans', unit.study_plan)
    return unit


def norm_study_plans_disciplines(unit: ScosUnit):
    # заменяем id из локальной базы, на внешние id
    unit.study_plan = get_external_id('study_plans', unit.study_plan)
    unit.discipline = get_external_id('disciplines', unit.discipline)
    return unit
