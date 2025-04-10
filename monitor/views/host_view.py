# -*- coding: utf-8 -*-
import json

from django.db import transaction
from django.core.paginator import Paginator

from monitor.models import Host
from utils.aes_util import encrypt_text
from utils.req_handler import req_handler


@req_handler
def create_host(request):

    if request.method != 'POST':
        raise Exception('请求方式有误')

    datas = json.loads(request.body.decode('utf-8'))
    host_objs = []

    with transaction.atomic():
        for data in datas:
            host_obj = Host(
                idc_id=data.get('idc_id'),
                hostname=data.get('hostname'),
                ip_address=data.get('ip_address'),
                status=data.get('status'),
                root_password=encrypt_text(data.get('root_password')).decode("utf-8"), # 密码加密
            )
            host_objs.append(host_obj)

        Host.objects.bulk_create(host_objs)

@req_handler
def update_host(request):

    if request.method != 'PUT':
        raise Exception('请求方式有误')

    datas = json.loads(request.body.decode('utf-8'))
    filter_dict = datas.get('filter_dict', {})
    update_dict = datas.get('update_dict', {})

    hosts = __filter_hosts(filter_dict=filter_dict)
    hosts.update(**update_dict)

@req_handler
def read_host(request):

    if request.method != 'GET':
        raise Exception('请求方式有误')

    filter_dict = json.loads(request.GET.get('filter_dict', {}))
    limit = int(request.GET.get('limit', 20))
    page = int(request.GET.get('page', 1))

    hosts = __filter_hosts(filter_dict=filter_dict)
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
def delete_host(request):

    if request.method != 'DELETE':
        raise Exception('请求方式有误')

    filter_dict = request.GET

    hosts = __filter_hosts(filter_dict=filter_dict)
    hosts.update(is_delete=True)

def __filter_hosts(filter_dict):

    hosts = Host.objects.filter(is_delete=False)

    if filter_dict.get('id'):
        hosts = hosts.filter(id=filter_dict.get('id'))

    if filter_dict.get('ids'):
        hosts = hosts.filter(id__in=filter_dict.get('ids'))

    if filter_dict.get('idc_id'):
        hosts = hosts.filter(idc_id=filter_dict.get('idc_id'))

    if filter_dict.get('idc_ids'):
        hosts = hosts.filter(idc_id__in=filter_dict.get('idc_ids'))

    if filter_dict.get('hostname'):
        hosts = hosts.filter(hostname=filter_dict.get('hostname'))

    if filter_dict.get('ip_address'):
        hosts = hosts.filter(ip_address=filter_dict.get('ip_address'))

    if filter_dict.get('status'):
        hosts = hosts.filter(status=filter_dict.get('status'))

    if filter_dict.get('root_password'):
        hosts = hosts.filter(root_password=filter_dict.get('root_password'))

    if len(filter_dict.get('created_at_range', [])) == 2:
        created_at_range = filter_dict.get('created_at_range', [])
        hosts = hosts.filter(created_at__gte=created_at_range[0], created_at__lte=created_at_range[1])

    if len(filter_dict.get('updated_at_range', [])) == 2:
        updated_at_range = filter_dict.get('updated_at_range', [])
        hosts = hosts.filter(updated_at__gte=updated_at_range[0], updated_at__lte=updated_at_range[1])

    return hosts