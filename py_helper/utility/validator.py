from py_helper.models.exception.input_required_exception import InputRequiredAppException


class Validator:

    @staticmethod
    def required_validator(inputs: []):
        missing_fields = []
        for item in inputs:
            for key, value in item.items():
                if value is None or value == "":
                    missing_fields.append(key)

        if len(missing_fields) > 0:
            raise InputRequiredAppException(missing_fields)
