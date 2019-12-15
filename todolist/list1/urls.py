from django.conf.urls import url
from . import views
urlpatterns = [
    url('home', views.home, name='home'),
    url('login', views.login, name='login'),
    url('useradd', views.user_add,name = 'user_add'),
    url('userget', views.user_get, name='user_get'),

    url('groupadd', views.group_add,name = 'group_add'),
    url('groupget', views.group_get, name='group_get'),

    url('taskadd/(?P<groupid>\w{0,30})/$', views.task_add,name = 'task_add'),
    url('taskget/(?P<groupid>\w{0,30})/$', views.task_get,name = 'task_get'),
    url('taskdelete', views.delete_task, name='delete_task'),
    url('taskstatuschange', views.change_task_status, name='change_task_status'),
]