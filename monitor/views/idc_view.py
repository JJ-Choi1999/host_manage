# -*- coding: utf-8 -*-
import json

from django.db import transaction
from django.core.paginator import Paginator

from monitor.models import IDC
from utils.req_handler import req_handler

@req_handler
def create_idc(request):

    if request.method != 'POST':
        raise Exception('请求方式有误')

    datas = json.loads(request.body.decode('utf-8'))
    idc_objs = []

    with transaction.atomic():
        for data in datas:
            idc_obj = IDC(
                city_id=data.get('city_id'),
                name=data.get('name'),
                address=data.get('address'),
            )
            idc_objs.append(idc_obj)

        IDC.objects.bulk_create(idc_objs)

@req_handler
def update_idc(request):
    
    if request.method != 'PUT':
        raise Exception('请求方式有误')

    datas = json.loads(request.body.decode('utf-8'))
    filter_dict = datas.get('filter_dict', {})
    update_dict = datas.get('update_dict', {})

    idcs = __filter_idcs(filter_dict=filter_dict)
    idcs.update(**update_dict)

@req_handler
def read_idc(request):
    
    if request.method != 'GET':
        raise Exception('请求方式有误')

    filter_dict = json.loads(request.GET.get('filter_dict', {}))
    limit = int(request.GET.get('limit', 20))
    page = int(request.GET.get('page', 1))

    idcs = __filter_idcs(filter_dict=filter_dict)
    paginator = Paginator(idcs, limit)
    page_objs = paginator.get_page(page)

    return {
        "page": page,
        "limit": limit,
        "count": paginator.count,
        "num_pages": paginator.num_pages,
        "data": list(map(lambda x: x.to_dict(), page_objs))
    }

@req_handler
def delete_idc(request):
    
    if request.method != 'DELETE':
        raise Exception('请求方式有误')

    filter_dict = request.GET

    idcs = __filter_idcs(filter_dict=filter_dict)
    idcs.update(is_delete=True)

def __filter_idcs(filter_dict: dict = {}):

    idcs = IDC.objects.filter(is_delete=False)

    if filter_dict.get('id'):
        idcs = idcs.filter(id=filter_dict.get('id'))

    if filter_dict.get('ids'):
        idcs = idcs.filter(id__in=filter_dict.get('ids'))

    if filter_dict.get('city_id'):
        idcs = idcs.filter(city_id=filter_dict.get('id'))

    if filter_dict.get('city_ids'):
        idcs = idcs.filter(city_id__in=filter_dict.get('ids'))

    if filter_dict.get('province'):
        idcs = idcs.filter(province=filter_dict.get('province'))

    if filter_dict.get('name'):
        idcs = idcs.filter(name__contains=filter_dict.get('name'))

    if filter_dict.get('address'):
        idcs = idcs.filter(address__contains=filter_dict.get('address'))

    if filter_dict.get('is_delete') != None:
        idcs = idcs.filter(is_delete=filter_dict.get('is_delete'))

    return idcs