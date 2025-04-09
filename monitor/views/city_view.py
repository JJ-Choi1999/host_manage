# -*- coding: utf-8 -*-
import json

from django.db import transaction

from monitor.models import City
from utils.req_handler import req_handler

@req_handler
def create_city(request):

    if request.method != 'POST':
        raise Exception('请求方式有误')

    datas = json.loads(request.body.decode('utf-8'))
    city_objs = []

    with transaction.atomic():
        for data in datas:
            city_obj = City(
                province=data.get('province'),
                city=data.get('city'),
                location=data.get('location'),
            )
            city_objs.append(city_obj)

        City.objects.bulk_create(city_objs)

@req_handler
def update_city(request):
    pass

@req_handler
def read_city(request):
    pass

@req_handler
def delete_city(request):
    pass

@req_handler
def __filter_city(request):
    pass