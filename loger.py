from datetime import datetime


def write_to_log(text: str):
    print(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}>>\t{text}')
