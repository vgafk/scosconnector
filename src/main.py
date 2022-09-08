import local_base
import scos_connector


def get_all_data_from_scos():
    all_scos_data = scos_connector.get_all_data_from_scos()
    for unit in all_scos_data:
        local_base.insert(unit)


def update_data_in_scos():
    local_updated_data = local_base.get_all_updated_data()
    scos_connector.update_data(local_updated_data)


def delete_data_from_scos():
    local_deleted_data = local_base.get_all_deleted_data()
    scos_connector.delete_data(local_deleted_data)


if __name__ == "__main__":
    if not local_base.base_exist():
        local_base.create_base()
        get_all_data_from_scos()

    delete_data_from_scos()
    # update_data_in_scos()