import datetime
from django.core import paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from typing import TypeVar, Dict
import time
import calendar

T = TypeVar('T')

def get_before_date(date_end="",days=1):
    if date_end == "":
        date_end = datetime.date.today().strftime('%Y-%m-%d')
    date_int = date_end.split('-')
    date_end_format = datetime.datetime(int(date_int[0]),int(date_int[1]),int(date_int[2]))
    result = date_end_format - datetime.timedelta(days=days)
    return result.strftime('%Y-%m-%d')

def get_last_date(month):
    month_split = month.split("-")
    year_int = int(month_split[0])
    month_int = int(month_split[1])
    firstDayWeekDay, monthRange = calendar.monthrange(year_int, month_int)
    lastDay = datetime.date(year=year_int,month=month_int,day=monthRange)
    return lastDay.strftime("%Y-%m-%d")

def get_last_month():
    today = datetime.date.today()
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=1)
    return last_month.strftime("%Y-%m")

def get_last_year(last_month=get_last_month()):
    end_date_str = "%s-01" % last_month
    timeArray = time.strptime(end_date_str,"%Y-%m-%d")
    timeStamp = time.mktime(timeArray)
    start_year = int(time.strftime("%Y",time.localtime(timeStamp))) - 1
    month_day = time.strftime("%m", time.localtime(timeStamp))
    start_month = "%s%s" % (start_year, month_day)
    return start_month

def queryByPage(model_infos, current_page_idx=1,page_size=10):
    current_page_idx = int(current_page_idx)
    if current_page_idx == 0:
        current_page_idx = 1
    page_size = int(page_size)
    if page_size == 0:
        page_size = 10
    if page_size > 200:
        page_size = 200
    paginator = Paginator(model_infos,page_size)
    total_size = paginator.count
    try:
        models = paginator.page(current_page_idx)
    except PageNotAnInteger:
        models = paginator.page(1)
        current_page_idx = 1
    except EmptyPage:
        models = paginator.page(paginator.num_pages)
        current_page_idx = paginator.num_pages
    return total_size,current_page_idx,page_size,models

def getResultDict(code: int,message: str, kwargs: Dict[str, T]) -> Dict[str, T]:
    if isinstance(kwargs,dict):
        return {
            "errcode": code,
            "errmsg": message,
            **kwargs
        }
    else:
        return {
            "errcode": code,
            "errmsg": message,
        }

if __name__ == "__main__":
    print(get_last_date("2022-05"))