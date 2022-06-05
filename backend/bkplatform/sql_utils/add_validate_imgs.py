import json
import requests
import getopt
import os
from json import dumps
import sys
sys.path.append('..')


def main(name):
    dic = {}
    name = name
    for i in range(9):
        dic[i+1] = '../static/validate/'+name+'_'+str(i+1)+'.png'
        if not os.path.exists(dic[i+1]):
            print('There is no file: ' + dic[i+1])
            return None
    stringArr = dumps(dic)
    return stringArr


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "", ["name=", "right="])
    if len(opts) < 1 or len(opts) > 2:
        print(
            'Please input: --name=[filename] (--right=123456[from 1 to 9, -1 is allright,-2 is unknown])')
    else:
        opt_name, opt_value = opts[0]
        right = '-2'
        if len(opts) > 1:
            _, right = opts[1]
        stringArr = main(opt_value)
        if stringArr:
            res = requests.post(
                url='http://0.0.0.0:8000/api/api/addvalidateimgs/',
                data=json.dumps({
                    'imgs': stringArr,
                    'right': right
                })
            )
            if res.status_code == 200:
                print("数据添加成功")
            else:
                print("数据添加失败")
                print(res.status_code)

