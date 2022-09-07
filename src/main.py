import local_base
import scos_connector


def get_all_data_from_scos():
    all_scos_data = scos_connector.get_all_data_from_scos()
    for unit in all_scos_data:
        local_base.insert(unit)


if __name__ == "__main__":
    if not local_base.base_exist():
        local_base.create_base()
    get_all_data_from_scos()



