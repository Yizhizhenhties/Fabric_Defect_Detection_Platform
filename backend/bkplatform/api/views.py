import base64
from io import BytesIO
from PIL import Image
from utils.common import get_last_month, queryByPage, getResultDict, get_last_date
from api.models import *
from api.nn_backend import *
from utils.error_code import ErrorCodes
from utils.api_base_view import ApiBaseView
from typing import Dict, TypeVar
from django.views import View
from django.http import HttpResponse, HttpRequest
import json
import datetime
from api.EX4 import *
from django.views.decorators.http import require_http_methods
import random
import uuid
import datetime
import os
# Create your views here.
T = TypeVar('T')

processor = Backend()
EX4 = MyModel()

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
        return HttpResponse(json.dumps(data),content_type='application/json')
    
    def post(self, request, *args, **kwargs):
        myFiles = request.FILES.getlist("file", None)
        if not myFiles:
            return HttpResponse({"errcode": ErrorCodes.API_EXCEPTION.Code(),
                                 "errmsg": ErrorCodes.API_EXCEPTION.Message()},
                                content_type='application/json')
        now_time = datetime.datetime.now()
        base64_img_list = []
        for myFile in myFiles:
            img = Image.open(myFile.file).convert('RGB')
            is_fabric, is_normal, mask, heat = processor.process(img)
            src_img = self.image_to_base64(img)
            base64_img = self.image_to_base64(mask)
            heat = self.image_to_base64(heat)
            if not is_fabric:
                base64_img_list.append({
                    "is_fabric": False,
                    "src_img": src_img,
                    "pro_img": "此图片不为目标纺织物",
                    "is_normal": "此图片不为目标纺织物",
                    "time": now_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "has_pro_img": False,
                    "heat": heat
                })
            else:
                base64_img_list.append({
                    "is_fabric": True,
                    "src_img": src_img,
                    "pro_img": '无缺陷部分' if is_normal else base64_img,
                    "is_normal": 'True' if is_normal else 'False',
                    "time": now_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "has_pro_img": False if is_normal else True,
                    "heat": heat
                })
        #
        if 'username' in request.POST:
            username = request.POST.get("username")
            dirpath = "static/image/"+str(username)+'/'
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            uuid_ = uuid.uuid1()
            dic = {}
            length = 0
            pro_length = 0
            for img in base64_img_list:
                if img["is_fabric"]:
                    file_i_path = os.path.join(dirpath, str(uuid_)+'_'+str(length)+'.png')
                    dic[length] = file_i_path
                    b64_data = img["heat"].split(';base64,')[1]
                    img_decode = base64.b64decode(b64_data)
                    with open(file_i_path, "wb") as f:
                        f.write(img_decode)
                    length += 1
                    if img["is_normal"] == 'True':
                        pro_length += 1
            imgurls = json.dumps(dic)
            history_obj = History(his_uuid=uuid_,username=username,length=length,pro_length=pro_length,imgurls=imgurls,createtime=datetime.datetime.now(),updatetime=datetime.datetime.now())
            history_obj.save()
        # 
        return self.packResponse(getResultDict(ErrorCodes.SUCCED.Code(), ErrorCodes.SUCCED.Message(), {
            "data": base64_img_list
        }))

class GetValidateImg(ApiBaseView):
    def __init__(self):
        super(GetValidateImg, self).__init__()

    def isParamsValid(self, *args, **kwargs) -> bool:
        return True

    def image_to_base64(self, image: Image.Image, fmt='png') -> str:
        output_buffer = BytesIO()
        image.save(output_buffer, format=fmt)
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data).decode('utf-8')
        return f'data:image/{fmt};base64,' + base64_str

    def getResult(self, *args, **kwargs) -> Dict[str, T]:
        validate_obj = ValidateImages.objects.filter()
        ranint = random.randint(1,len(validate_obj))
        imgs = validate_obj[ranint-1]
        right = imgs.right
        imgs_url = json.loads(imgs.imgurls)
        data = []
        for i in range(9):
            url = imgs_url[str(i+1)]
            img = Image.open(url[1:]).convert('RGB')
            img_base64 = self.image_to_base64(img)
            data.append({
                'va_img': img_base64
            })
        response_data = getResultDict(ErrorCodes.SUCCED.Code(), ErrorCodes.SUCCED.Message(), {
            "data": data,
            "right": right
        })
        return response_data

class GetHistoryList(ApiBaseView):
    def __init__(self):
        super(GetHistoryList, self).__init__()

    def isParamsValid(self, *args, **kwargs) -> bool:
        return True

    def getResult(self, *args, **kwargs) -> Dict[str, T]:
        history_obj = History.objects.filter(username=self.params['username'])
        data = []
        for item in history_obj:
            data.append({
                'uuid': item.his_uuid,
                'username': item.username,
                'length': item.length,
                'pro_length': item.pro_length,
                'imgurls': item.imgurls,
                'createtime': item.createtime.strftime('%Y-%m-%d %H:%M:%S'),
                'updatetime': item.updatetime.strftime('%Y-%m-%d %H:%M:%S')
            })
        response_data = getResultDict(ErrorCodes.SUCCED.Code(), ErrorCodes.SUCCED.Message(), {
            "data": data
        })
        return response_data

class GetHistoryImgs(ApiBaseView):
    def __init__(self):
        super(GetHistoryImgs, self).__init__()

    def isParamsValid(self, *args, **kwargs) -> bool:
        return True
    
    def image_to_base64(self, image: Image.Image, fmt='png') -> str:
        output_buffer = BytesIO()
        image.save(output_buffer, format=fmt)
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data).decode('utf-8')
        return f'data:image/{fmt};base64,' + base64_str

    def getResult(self, *args, **kwargs) -> Dict[str, T]:
        imgurls = self.params['imgurls']
        length = self.params['length']
        imgurls = json.loads(imgurls)
        data = []
        for i in range(length):
            img = Image.open(imgurls[str(i)]).convert('RGB')
            base64_img = self.image_to_base64(img)
            data.append({
                'img': base64_img
            })
        response_data = getResultDict(ErrorCodes.SUCCED.Code(), ErrorCodes.SUCCED.Message(), {
            "data": data
        })
        return response_data

class AddFeedback(ApiBaseView):
    def __init__(self):
        super(AddFeedback, self).__init__()

    def isParamsValid(self, *args, **kwargs) -> bool:
        return True

    def getResult(self, *args, **kwargs) -> Dict[str, T]:
        fb = Feedback(check=self.params['check'],text=self.params['text'])
        fb.save()
        response_data = getResultDict(ErrorCodes.SUCCED.Code(), ErrorCodes.SUCCED.Message(), {
            "data": {'ok': 'ok'}
        })
        return response_data

@require_http_methods(['POST'])
def AddValidateImgs(request: HttpRequest, *args, **kwargs):
    body = json.loads(request.body)
    if 'imgs' in body:
        stringArr = body['imgs']
        right = '-2'
        if 'right' in body:
            right = body['right']
        va_imgs = ValidateImages(imgurls=stringArr,right=right)
        va_imgs.save()
        response = HttpResponse(status=200)
    else:
        response = HttpResponse(status=400)  # 参数错误
    return response


class exam4(View):
    def __init__(self):
        super(exam4, self).__init__()

    def packResponse(self, data):
        return HttpResponse(json.dumps(data),content_type='application/json')

    def post(self, request, *args, **kwargs):
        myFiles = request.FILES.getlist("file", None)
        if not myFiles:
            return HttpResponse({"errcode": ErrorCodes.API_EXCEPTION.Code(),
                                 "errmsg": ErrorCodes.API_EXCEPTION.Message()},
                                content_type='application/json')
        now_time = datetime.datetime.now()
        response_list = []
        for myFile in myFiles:
            img = Image.open(myFile.file)
            output_ = EX4.process(img)
            response_list.append({
                "output": str(output_)
            })
        return self.packResponse(getResultDict(ErrorCodes.SUCCED.Code(), ErrorCodes.SUCCED.Message(), {
            "data": response_list
        }))

