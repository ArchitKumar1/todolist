from django.conf.urls import url
from . import views
urlpatterns = [
    url('task', views.task, name='task'),
    url('login', views.login, name='login'),
    url('signup', views.signup, name='signup'),
]