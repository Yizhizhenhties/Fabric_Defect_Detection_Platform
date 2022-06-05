import json
from django.views import View
from django.http import HttpResponse
from utils.error_code import ErrorCodes
from utils.common import getResultDict


class ApiBaseView(View):
    def __init__(self):
        super(ApiBaseView, self).__init__()
        self.params = None
        self.request = None

    def get_user_product(self) -> dict:
        user_product = self.request.session.get("user_product")
        product_id_list = []
        if user_product != "":
            user_product_split = user_product.split(",")
            for item in user_product_split:
                product_id_list.append(int(item))
        return product_id_list

    def parseRequest(self, request):
        if request.body:
            try:
                req = json.loads(request.body)
            except Exception as e:
                return  ErrorCodes.PARSE_REQUEST_CONTENT_FAILED.Code(), ErrorCodes.PARSE_REQUEST_CONTENT_FAILED.Message \
                    ("detail: {}".format(e))
            if "params" not in req or not isinstance(req["params"],dict):
                return ErrorCodes.PARAM_NOT_CORRET_ERROR.Code(), ErrorCodes.PARAM_NOT_CORRET_ERROR.Message()
            else:
                self.params = req["params"]
            return ErrorCodes.SUCCED.Code(), ErrorCodes.SUCCED.Message()
        else:
            return ErrorCodes.REQUEST_BODY_IS_EMPTY_ERROR.Code(), ErrorCodes.REQUEST_BODY_IS_EMPTY_ERROR.Message()

    def packResponse(self, data):
        return HttpResponse(json.dumps(data),content_type='application/json')

    def post(self, request, *args, **kwargs):
        self.request = request
        ret, msg = self.parseRequest(request)
        if ret != 0:
            return self.packResponse({"errcode": ret, "errmsg": msg})
        if not self.isParamsValid(*args, **kwargs):
            return self.packResponse({"errcode": ErrorCodes.INVALID_PARAMS_ERROR.Code(),
                                      "errmsg": ErrorCodes.INVALID_PARAMS_ERROR.Message()})
        try:
            return self.packResponse(self.getResult(*args, **kwargs))
        except Exception as e:
            print(e)
            return self.packResponse({"errcode": ErrorCodes.API_EXCEPTION.Code(),
                                      "errmsg": ErrorCodes.API_EXCEPTION.Message()})

    def get_result_dict(self, *args, **kwargs) -> dict:
        result = getResultDict(ErrorCodes.SUCCED.Code(), ErrorCodes.SUCCED.Message(),{})
        return result

