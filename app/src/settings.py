# идентификаторы в тестовом контуре

class Settings:
    """Настройки программы"""
    x_cn_uuid: str = 'd6a4f02c-3833-4038-97e7-aa4426468a0f'
    org_id: str = '15d8e604-d403-4af7-9900-90f71b2af965'
    to_scos: bool
    base_exists: bool

    def get_x_cn_uuid(self) -> str:
        """UUID для доступа к ресурсам СЦОС"""
        return self.x_cn_uuid

    def get_org_id(self) -> str:
        """ID организации в сервисе СЦОС"""
        return self.org_id

    def to_scos(self) -> bool:
        """Необходимость внесения данных в СЦОС"""
        return self.to_scos

    def base_exists(self):
        return self.base_exists
