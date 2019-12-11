from django.conf.urls import url
from . import views
urlpatterns = [
    url('home', views.home, name='home'),
    url('login', views.login, name='login'),
    url('useradd', views.user_add,name = 'user_add'),
    url('groupadd', views.group_add,name = 'group_add'),
    url('taskadd', views.task_add,name = 'task_add'),

    url('userget', views.user_get,name = 'user_get'),
    url('groupget', views.group_get,name = 'group_get'),
    url('taskgetfromgroup', views.task_get_from_group, name = 'task_get_from_group'),
    url('taskget', views.task_get,name = 'task_get'),
]