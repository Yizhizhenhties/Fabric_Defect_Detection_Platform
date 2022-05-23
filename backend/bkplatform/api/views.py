import imp
import os
from PIL import Image
from django.shortcuts import render
from django.conf import settings
from utils.common import get_last_month, queryByPage, getResultDict, get_last_date
from api.models import *
from utils.error_code import ErrorCodes
from utils.api_base_view import ApiBaseView
from typing import Dict, TypeVar
from django.views import View
from django.http import HttpResponse
import json
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
                data = {'password': item.password}
        else:
            data = {'password', 'error'}
        response_data = getResultDict(ErrorCodes.SUCCED.Code(), ErrorCodes.SUCCED.Message(), {
            "data": data
        })
        return response_data


class Process(View):
    def __init__(self):
        super(Process, self).__init__()

    def packResponse(self, data):
        return HttpResponse(json.dumps(data),content_type='application/json')
    
    def post(self, request, *args, **kwargs):
        myFiles = request.FILES.getlist("file", None)
        if not myFiles:
            return HttpResponse({"errcode": ErrorCodes.API_EXCEPTION.Code(),
                                 "errmsg": ErrorCodes.API_EXCEPTION.Message()},
                                content_type='application/json')
        for myFile in myFiles:
            # 打开特定的文件进行二进制的写操作(有更新，无新建)
            destination = open(os.path.join(
                "static/image/", myFile.name), 'wb+')
            for chunk in myFile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
        return self.packResponse(getResultDict(ErrorCodes.SUCCED.Code(), ErrorCodes.SUCCED.Message(), {
            "data": ''
        }))
