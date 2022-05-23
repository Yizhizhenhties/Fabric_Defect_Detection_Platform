import imp
import os
import base64
from io import BytesIO
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

    def image_to_base64(self, image: Image.Image, fmt='png') -> str:
        output_buffer = BytesIO()
        image.save(output_buffer, format=fmt)
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data).decode('utf-8')
        return f'data:image/{fmt};base64,' + base64_str

    def packResponse(self, data):
        return HttpResponse(json.dumps(data), content_type='application/json')

    def post(self, request, *args, **kwargs):
        myFiles = request.FILES.getlist("file", None)
        if not myFiles:
            return HttpResponse({"errcode": ErrorCodes.API_EXCEPTION.Code(),
                                 "errmsg": ErrorCodes.API_EXCEPTION.Message()},
                                content_type='application/json')
        # for myFile in myFiles:
        #    destination = open(os.path.join(
        #        "static/image/", myFile.name), 'wb+')
        #    for chunk in myFile.chunks():
        #        destination.write(chunk)
        #    destination.close()
        base64_img_list = []
        for myFile in myFiles:
            img = Image.open(myFile.file).convert('RGB')
            base64_img = self.image_to_base64(img)
            base64_img_list.append(base64_img)
        return self.packResponse(getResultDict(ErrorCodes.SUCCED.Code(), ErrorCodes.SUCCED.Message(), {
            "data": base64_img_list
        }))
