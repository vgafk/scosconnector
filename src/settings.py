# идентификаторы в тестовом контуре
X_CN_UUID = 'd6a4f02c-3833-4038-97e7-aa4426468a0f'
ORG_ID = '15d8e604-d403-4af7-9900-90f71b2af965'

# Локальная база данных sqlite
local_base_path = 'cache.db'

# Общий формат url
API_URL = 'https://test.online.edu.ru/'  # тестовый контур
# API_URL = 'https://online.edu.ru/api/'     # боевой контур
API_URL_V1 = API_URL + 'api/v1/'
API_URL_V2 = API_URL + 'vam/api/v2/'


# Конкретные endpoints
CHECK_CONNECTION = API_URL_V1 + 'connection/check'      # Проверка подключения
OPEN_ID_CONF = 'https://auth.online.edu.ru/realms/portfolio/.well-known/openid-configuration' # Настройка OpenID

# Название параметра и url могут отличаться, например study_plan_disciplines без s в plan
endpoint_urls = {
    'educational_programs': API_URL_V2 + 'educational_programs',
    'study_plans': API_URL_V2 + 'study_plans',
    'disciplines': API_URL_V2 + 'disciplines',
    'study_plan_disciplines': API_URL_V2 + 'study_plans/%unit_id/disciplines',
    'students': API_URL_V2 + 'students',
    'study_plan_students': API_URL_V2 + 'study_plans_students',
    'contingent_flows': API_URL_V2 + 'students/%unit_id/contingent_flows',
    'marks': API_URL_V2 + 'marks'
}

