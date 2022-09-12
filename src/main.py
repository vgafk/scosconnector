import local_base
import scos_connector
import file_reader
from normalizer import normalize


def get_all_data_from_scos():
    all_scos_data = scos_connector.get_all_data_from_scos()
    # for unit in all_scos_data:
    local_base.insert(all_scos_data)


def update_data_in_scos():
    local_updated_data = local_base.get_all_updated_data()
    scos_connector.update_data(local_updated_data)


def delete_data_from_scos():
    local_deleted_data = local_base.get_all_deleted_data()
    scos_connector.delete_data(local_deleted_data)


def set_data_in_local_base():
    add_units_list, update_units_list, delete_units_list = file_reader.read_all_files()
    normalize(add_units_list)
    normalize(update_units_list)
    local_base.insert(add_units_list)
    local_base.update(update_units_list)
    local_base.delete(delete_units_list)


if __name__ == "__main__":
    if not local_base.base_exist():
        local_base.create_base()
        # get_all_data_from_scos()

    if not file_reader.csv_dir_exists():
        file_reader.create_csv_dir()

    set_data_in_local_base()
