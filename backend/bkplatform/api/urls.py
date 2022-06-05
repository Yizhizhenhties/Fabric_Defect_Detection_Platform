from django.conf.urls import url
from django.urls.resolvers import URLPattern
from api import views

urlpatterns = [
    url('pwd/', views.GetUserPassword.as_view()),
    url('process/', views.Process.as_view()),
    url('ex4/', views.exam4.as_view()),
    url('validate/', views.GetValidateImg.as_view()),
    url('history/', views.GetHistoryList.as_view()),
    url('gethistoryimg/', views.GetHistoryImgs.as_view()),
    url('addfeedback/',views.AddFeedback.as_view()),
    url('addvalidateimgs/', views.AddValidateImgs)
]
