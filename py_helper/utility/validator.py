from py_helper.models.exception.input_required_exception import InputRequiredException


class Validator:

    @staticmethod
    def required_validator(inputs: []):
        missing_fields = []
        for item in inputs:
            for key, value in item.items():
                if value is None or value == "":
                    missing_fields.append(key)

        if len(missing_fields) > 0:
            raise InputRequiredException(missing_fields)
