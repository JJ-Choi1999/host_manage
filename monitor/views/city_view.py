# -*- coding: utf-8 -*-
import json

from django.db import transaction
from django.core.paginator import Paginator

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

    if request.method != 'PUT':
        raise Exception('请求方式有误')

    datas = json.loads(request.body.decode('utf-8'))
    filter_dict = datas.get('filter_dict', {})
    update_dict = datas.get('update_dict', {})

    citys = __filter_citys(filter_dict=filter_dict)
    citys.update(**update_dict)

@req_handler
def read_city(request):

    if request.method != 'GET':
        raise Exception('请求方式有误')

    filter_dict = json.loads(request.GET.get('filter_dict', {}))
    limit = int(request.GET.get('limit', 20))
    page = int(request.GET.get('page', 1))

    citys = __filter_citys(filter_dict=filter_dict)
    paginator = Paginator(citys, limit)
    page_objs = paginator.get_page(page)

    return {
        "page": page,
        "limit": limit,
        "count": paginator.count,
        "num_pages": paginator.num_pages,
        "data": list(map(lambda x: x.to_dict(), page_objs))
    }

@req_handler
def delete_city(request):

    if request.method != 'DELETE':
        raise Exception('请求方式有误')

    filter_dict = request.GET

    citys = __filter_citys(filter_dict=filter_dict)
    citys.update(is_delete=True)

def __filter_citys(filter_dict: dict = {}):

    citys = City.objects.filter(is_delete=False)

    if filter_dict.get('id'):
        citys = citys.filter(id=filter_dict.get('id'))

    if filter_dict.get('ids'):
        citys = citys.filter(id__in=filter_dict.get('ids'))

    if filter_dict.get('province'):
        citys = citys.filter(province=filter_dict.get('province'))

    if filter_dict.get('city'):
        citys = citys.filter(city=filter_dict.get('city'))

    if filter_dict.get('location'):
        citys = citys.filter(location__contains=filter_dict.get('location'))

    if filter_dict.get('is_delete') != None:
        citys = citys.filter(is_delete=filter_dict.get('is_delete'))

    return citys