from django.conf.urls import url
from . import views
urlpatterns = [
    url('viewallitems', views.view_all_items, name = 'view_all_items'),
    url('additem', views.add_item, name = 'add_item'),
    url('deleteitem', views.delete_item, name = 'delete_item'),
]