class BaseException(Exception):
    def __init__(self, status_code: int, error: str):
        self.status_code = status_code
        self.error = error
    def __int__(self):
        return self.status_code
    def __str__(self):
        return self.error

class InvalidOrMissingParameters(BaseException):
    ...
class UUIDNotFound(BaseException):
    ...