import json

from scos_units import EducationalProgram

ep = EducationalProgram.from_json(json.loads('''{
            "id": "ca0576bf-aa61-46ad-88de-365db4ff5d39",
            "title": "Компьютерные системы и технологии",
            "direction": "Информатика и вычислительная техника",
            "code_direction": "09.03.01",
            "start_year": "2022",
            "end_year": "2026",
            "organization_id": "15d8e604-d403-4af7-9900-90f71b2af965",
            "external_id": "bdb95b34-e327-4a89-9f0d-d671239feb94"
        }'''))

