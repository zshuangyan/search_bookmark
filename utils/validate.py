import jsonschema


def json_validate(schema):
    def decorator(func):
        def inner(handler):
            try:
                jsonschema.validate(handler.data, schema)
            except jsonschema.ValidationError as e:
                handler.write_error(status_code=400, error_msg=e)
            func(handler)
        return inner
    return decorator