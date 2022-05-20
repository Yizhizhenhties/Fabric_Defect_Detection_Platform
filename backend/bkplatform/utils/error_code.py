class ErrorMessage(object):
    def __init__(self, code: int, message: str) -> None:
        self._code = code
        self._message = message

    def Code(self) -> int:
        return self._code

    def Message(self, append: str = "") -> str:
        return self._message if not append else "{}; {}".format(self._message,append)

class ErrorCodes(object):
    SUCCED = ErrorMessage(0,"ok")
    PARSE_REQUEST_CONTENT_FAILED =  ErrorMessage(-3000,"PARSE_REQUEST_CONTENT_FAILED")
    PARAM_NOT_CORRET_ERROR = ErrorMessage(-3002,"PARAM_NOT_CORRET_ERROR")
    REQUEST_BODY_IS_EMPTY_ERROR = ErrorMessage(-3003,"REQUEST_BODY_IS_EMPTY_ERROR")
    INVALID_PARAMS_ERROR = ErrorMessage(-3004,"INVALID_PARAMS_ERROR")
    SIGNATURE_AUTH_FAILED = ErrorMessage(-3005,"SIGNATURE_AUTH_FAILED")
    USER_STATE_ERROR = ErrorMessage(-3006,"USER_STATE_ERROR")
    USER_NOT_AUTHORITY = ErrorMessage(-3007,"USER_NOT_AUTHORITY")
    RESOURCE_SPEC_ERRPR = ErrorMessage(-3008,"RESOURCE_SPEC_ERRPR")
    CMDB_BUSSINESS_NAME_ERROR = ErrorMessage(-3009,"CMDB_BUSSINESS_NAME_ERROR")
    API_EXCEPTION = ErrorMessage(-5000,"API_EXCEPTION")