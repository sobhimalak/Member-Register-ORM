
def validate(values):
    is_valid = True
    values_invalid = []

    if len(values['-FIRST_NAME-']) == 0:
        values_invalid.append(' FIRST NAME & ')
        is_valid = False

    if len(values['-LAST_NAME-']) == 0:
        values_invalid.append(' LAST NAME & ')
        is_valid = False

    if len(values['-POST_NUMBER-']) == 0:
        values_invalid.append(' POST NUMBER & ')
        is_valid = False

    if len(values['-ADDRESS-']) == 0:
        values_invalid.append(' ADDRESS')
        is_valid = False

    # if values['-SUBSCRIPTION-'] == 0:
    #     values_invalid.append(' SUBSCRIPTION')
    #     is_valid = False


    result = {"is_valid": is_valid, "values_invalid": values_invalid}
    return result


def generate_error_message(values_invalid):
    error_message = ''
    for value_invalid in values_invalid:
        error_message += value_invalid

    return error_message
