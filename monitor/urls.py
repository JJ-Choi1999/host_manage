# -*- coding: utf-8 -*-
from django.urls import path

from monitor.views.city_view import create_city, update_city, read_city, delete_city
from monitor.views.host_view import create_host, update_host, read_host, delete_host, random_change_pw, host_statis
from monitor.views.idc_view import create_idc, update_idc, read_idc, delete_idc
from monitor.views.pwh_view import create_pwh, update_pwh, read_pwh, delete_pwh
from monitor.views.ping_view import ping_test

urlpatterns = [

    path(r'monitor/city/create_city', create_city),
    path(r'monitor/city/update_city', update_city),
    path(r'monitor/city/read_city', read_city),
    path(r'monitor/city/delete_city', delete_city),

    path(r'monitor/idc/create_idc', create_idc),
    path(r'monitor/idc/update_idc', update_idc),
    path(r'monitor/idc/read_idc', read_idc),
    path(r'monitor/idc/delete_idc', delete_idc),

    path(r'monitor/host/create_host', create_host),
    path(r'monitor/host/update_host', update_host),
    path(r'monitor/host/read_host', read_host),
    path(r'monitor/host/delete_host', delete_host),
    path(r'monitor/host/random_change_pw', random_change_pw),
    path(r'monitor/host/host_statis', host_statis),

    path(r'monitor/pwh/create_pwh', create_pwh),
    path(r'monitor/pwh/update_pwh', update_pwh),
    path(r'monitor/pwh/read_pwh', read_pwh),
    path(r'monitor/pwh/delete_pwh', delete_pwh),

    path(r'monitor/ping_test', ping_test),

]