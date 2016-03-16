#coding:utf-8
from django.conf.urls import url
from .models import Accommodation,User
from . import views

urlpatterns = [
    url(r'^acc/(?P<accommodation_id>[0-9]+)$',views.acc_detail,name = 'acc_detail'),#公寓DetailView

    url(r'^register_json$',views.register_json,name = 'register'),#
    url(r'^reg_login$',views.reg_login,name = 'reg_login'),
    url(r'^login_json$',views.login_json,name = 'login_json'),

    url(r'^user/(?P<user_id>[0-9]+)$',views.user_detail,name = 'user'),
    url(r'^acc$', views.acc_list_view),
    url(r'^user/user_edit_json$',views.edit_user,name='edit-user'),
    url('^logout$',views.logout,name='logout')
]