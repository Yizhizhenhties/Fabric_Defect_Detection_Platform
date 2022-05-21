from django.shortcuts import render
from django.conf import  settings
from utils.common import get_last_month, queryByPage, getResultDict, get_last_date
from api.models import *
from utils.error_code import ErrorCodes
from utils.api_base_view import ApiBaseView
from typing import Dict,TypeVar
from django.views import View
# Create your views here.
T = TypeVar('T')

class GetUserPassword(ApiBaseView):
    def __init__(self):
        super(GetUserPassword, self).__init__()

    def isParamsValid(self, *args, **kwargs) -> bool:
        return True

    def getResult(self, *args, **kwargs) -> Dict[str, T]:
        user_obj = User.objects.filter(account=self.params['account'])
        if user_obj:
            for item in user_obj:
                data = {'password': item.password }
        else:
            data = {'password', 'error'}
        response_data = getResultDict(ErrorCodes.SUCCED.Code(), ErrorCodes.SUCCED.Message(),{
            "data": data
        })
        return response_data
