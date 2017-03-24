from werkzeug.exceptions import BadRequest
import re
TYPE_VALIDATOR = 1
MIN_VALIDATOR = 2
MAX_VALIDATOR = 3
REGEX_VALIDATOR = 4
VALID_VALUES_VALIDATOR = 5
NUMERIC_STRING_VALIDATOR = 6


def validate_type(param, type):
    if isinstance(param, type):
        return param
    else:
        raise BadRequest("The param %s is not of type %s" %(param, type))


def validate_min(param, min):
    if param >= min:
        return param
    else:
        raise BadRequest("The param %s is less than %s" %(param, min))


def validate_max(param, max):
    if param <= max:
        return param
    else:
        raise BadRequest("The param %s is greater than %s" %(param, max))


def validate_regex(param, regex):
    if re.match(regex, param):
        return param
    else:
        raise BadRequest("The param %s does not match to regex %s" % (param, regex))


def validate_valid_values(param, valid_values):
    if param in valid_values:
        return param
    else:
        raise BadRequest("The param %s is not a valid value. Valid values: %s"
                         % (param, ', '.join(str(valid) for valid in valid_values)))


def validate_numeric_string(param):
    try:
        float(param)
        return param
    except:
        raise BadRequest("The param %s is not a valid numeric value" % param)


def validate_param(param, param_tuple, required=False):
    if param is None:
        if not required:
            return None
        else:
            raise BadRequest("The param %s is mandatory" % param)

    for ituple in param_tuple:
        if ituple[0] == TYPE_VALIDATOR:
            param = validate_type(param, ituple[1])
        elif ituple[0] == MIN_VALIDATOR:
            param = validate_min(param, ituple[1])
        elif ituple[0] == MAX_VALIDATOR:
            param = validate_max(param, ituple[1])
        elif ituple[0] == REGEX_VALIDATOR:
            param = validate_regex(param, ituple[1])
        elif ituple[0] == VALID_VALUES_VALIDATOR:
            param = validate_valid_values(param, ituple[1])
        elif ituple[0] == NUMERIC_STRING_VALIDATOR:
            param = validate_numeric_string(param)
    return param

