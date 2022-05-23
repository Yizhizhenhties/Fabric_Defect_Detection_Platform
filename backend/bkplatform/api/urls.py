from django.conf.urls import url
from django.urls.resolvers import URLPattern
from api import views

urlpatterns = [
    url('pwd/', views.GetUserPassword.as_view()),
    url('process/', views.Process.as_view())
]
