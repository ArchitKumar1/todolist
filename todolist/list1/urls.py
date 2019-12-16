from django.conf.urls import url
from . import views
urlpatterns = [
    url('home', views.home, name='home'),
    url('login', views.login, name='login'),
    url('useradd', views.user_add,name = 'user_add'),
    url('userget', views.get_all_users, name='get_all_users'),

    url('groupadd', views.group_add,name = 'group_add'),
    url('groupget', views.group_get, name='group_get'),
    url('groupdelete', views.group_delete, name='group_delete'),


    url('taskadd/(?P<groupid>\w{0,30})/$', views.task_add,name = 'task_add'),
    url('taskget/(?P<groupid>\w{0,30})/$', views.task_get,name = 'task_get'),
    url('taskdelete', views.task_delete, name='task_delete'),
    url('taskstatuschange', views.change_task_status, name='change_task_status'),

    url('groupshare',views.share_group,name ="share_group"),
]