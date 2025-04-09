from django.db import models

class City(models.Model):

    class Meta:
        db_table = "city"

    province = models.CharField(max_length=255, help_text="一级行政区名")
    city = models.CharField(max_length=255, help_text="二级行政区名")
    location = models.CharField(max_length=255, help_text="具体地址")

class IDC(models.Model):

    class Meta:
        db_table = "idc"

    city_id = models.BigIntegerField(help_text="关联城市id")
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)

class Host(models.Model):

    class Meta:
        db_table = "host"

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('offline', 'Offline'),
    ]

    idc_id = models.BigIntegerField(help_text="主机关联id")
    hostname = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField(unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    root_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PasswordHistory(models.Model):

    class Meta:
        db_table = "password_history"

    host_id = models.BigIntegerField(help_text="主机关联id")
    old_password = models.CharField(max_length=255)
    changed_at = models.DateTimeField(auto_now_add=True)