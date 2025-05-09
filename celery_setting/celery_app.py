# -*- coding: utf-8 -*-
import random
import traceback
from datetime import datetime

import requests
from celery import Celery
from celery.schedules import crontab

from utils.load_config import YAML_CONFIGS_INFO

__main = YAML_CONFIGS_INFO['celery_init']['main']
__broker = YAML_CONFIGS_INFO['celery_init']['broker']
__backend = YAML_CONFIGS_INFO['celery_init']['backend']

app = Celery(__main, broker=__broker, backend=__backend)
app.conf.timezone = 'Asia/Shanghai'
app.conf.beat_schedule = {
    'random-change-pw': {
        'task': 'celery_setting.celery_app.random_change_pw',
        'schedule': 8 * 60 * 60
    },
    'statis-host': {
        'task': 'celery_setting.celery_app.statis_host',
        'schedule': crontab(hour=0, minute=0)
    }
}

# 启动定时任务 Worker(工作池)/beat(调度器):
# celery -A celery_app beat --loglevel=info
# celery -A celery_app worker --loglevel=info

@app.task
def random_change_pw():
    # print(f'当前时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, 随机数: {str(random.randint(1, 13))}')
    return requests.get(f'http://127.0.0.1:8001/monitor/host/random_change_pw').json()

@app.task
def statis_host():
    return requests.get(f'http://127.0.0.1:8001/monitor/host/host_statis').json()
