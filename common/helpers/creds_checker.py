from functools import wraps


def response_checker(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        function_response = function(*args,**kwargs)
        if function_response is None:
            raise RuntimeError(f"{function.__name__} is return nulled response!")
        return function_response
    return wrapper