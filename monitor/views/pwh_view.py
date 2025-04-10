# -*- coding: utf-8 -*-
import json

from django.db import transaction
from django.core.paginator import Paginator

from monitor.models import PasswordHistory
from utils.aes_util import encrypt_text, decrypt_text
from utils.req_handler import req_handler

@req_handler
def create_pwh(request):

    if request.method != 'POST':
        raise Exception('请求方式有误')

    datas = json.loads(request.body.decode('utf-8'))
    batch_insert(datas)

@req_handler
def update_pwh(request):

    if request.method != 'PUT':
        raise Exception('请求方式有误')

    datas = json.loads(request.body.decode('utf-8'))
    filter_dict = datas.get('filter_dict', {})
    update_dict = datas.get('update_dict', {})

    pwhs = __filter_pwhs(filter_dict=filter_dict)
    pwhs.update(**update_dict)

@req_handler
def read_pwh(request):

    if request.method != 'GET':
        raise Exception('请求方式有误')

    filter_dict = json.loads(request.GET.get('filter_dict', {}))
    limit = int(request.GET.get('limit', 20))
    page = int(request.GET.get('page', 1))

    hosts = __filter_pwhs(filter_dict=filter_dict)
    paginator = Paginator(hosts, limit)
    page_objs = paginator.get_page(page)

    return {
        "page": page,
        "limit": limit,
        "count": paginator.count,
        "num_pages": paginator.num_pages,
        "data": list(map(lambda x: x.to_dict(), page_objs))
    }

@req_handler
def delete_pwh(request):

    if request.method != 'DELETE':
        raise Exception('请求方式有误')

    filter_dict = request.GET

    pwhs = __filter_pwhs(filter_dict=filter_dict)
    pwhs.update(is_delete=True)

def __filter_pwhs(filter_dict):

    pwhs = PasswordHistory.objects.filter(is_delete=False)

    if filter_dict.get('id'):
        pwhs = pwhs.filter(id=filter_dict.get('id'))

    if filter_dict.get('ids'):
        pwhs = pwhs.filter(id__in=filter_dict.get('ids'))

    if filter_dict.get('host_id'):
        pwhs = pwhs.filter(host_id=filter_dict.get('host_id'))

    if filter_dict.get('host_ids'):
        pwhs = pwhs.filter(host_id__in=filter_dict.get('host_ids'))

    if filter_dict.get('old_password'):
        pwhs = pwhs.filter(old_password=filter_dict.get('old_password'))

    if len(filter_dict.get('changed_at_range', [])) == 2:
        changed_at_range = filter_dict.get('changed_at_range', [])
        pwhs = pwhs.filter(created_at__gte=changed_at_range[0], created_at__lte=changed_at_range[1])

    return pwhs

def batch_insert(datas: list):
    pwh_objs = []
    with transaction.atomic():
        for data in datas:
            pwh_obj = PasswordHistory(
                host_id=data.get('host_id'),
                old_password=data.get('old_password')
            )
            pwh_objs.append(pwh_obj)

        PasswordHistory.objects.bulk_create(pwh_objs)