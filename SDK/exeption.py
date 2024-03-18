class BaseExceptionSDK(Exception):
    pass


class BadRequest(BaseExceptionSDK):
    def __init__(self, exception):
        super().__init__(str(exception))


class InternalServerError(BaseExceptionSDK):
    def __init__(self, exception):
        super().__init__(str(exception))


class UnknownStatusCode(BaseExceptionSDK):
    def __init__(self, exception):
        super().__init__(str(exception))
