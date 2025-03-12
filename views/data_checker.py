empty_field_check = {"", None}

# missing data checker
def missing_data_checker(user_data, required_key_fields):
    user_data_keys = user_data.keys()
    user_data_values = user_data.values()

    missing_key = required_key_fields.difference(user_data_keys)

    missing_value = empty_field_check.intersection(user_data_values)

    if missing_key or missing_value:
        return (True, list(missing_key), list(missing_value))

    return (False, False, False)