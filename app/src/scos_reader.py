import requests

import local_base
from scos_connector import SCOSConnector
headers = {'Content-Type': 'application/json', 'X-CN-UUID': 'd6a4f02c-3833-4038-97e7-aa4426468a0f'}


def get_data_from_scos():
    page = 1
    last_page = 15
    results = []
    while page < last_page:
        url = f'https://test.online.edu.ru/vam/api/v2/disciplines?page={page}'
        resp_json = requests.get(url, headers=headers).json()
        results.extend(resp_json['results'])
        page += 1

    for row in results:
        print(row['id'])

if __name__ == '__main__':
    get_data_from_scos()
