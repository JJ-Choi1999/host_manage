# host_manage
1. 环境: Python 3.12、Django 4.1、MySQL 8.0.37
2. 导入 sql 文件夹下文件夹到mysql数据库
2. 打开 conf 文件夹按照实际情况修改配置
3. pip install -r requirements.txt 按照依赖
4. 项目根目录下执行以下命令启动Django 和 Celery
   1. 启动django, python manage.py runserver 0.0.0.0:8001
   2. 启动Celery Worker, celery -A celery_setting.celery_app worker --loglevel=info -P eventlet
   3. 启动Celery Beat, celery -A celery_setting.celery_app beat --loglevel=info