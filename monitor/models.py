from django.db import models

from django.utils.formats import date_format

class City(models.Model):

    class Meta:
        db_table = "city"

    province = models.CharField(max_length=255, help_text="一级行政区名")
    city = models.CharField(max_length=255, help_text="二级行政区名")
    location = models.CharField(max_length=255, help_text="具体地址")
    is_delete = models.BooleanField(default=False, help_text="软删除标记")

    def to_dict(self):
        return {
            "id": self.id,
            "province": self.province,
            "city": self.city,
            "location": self.location,
            "is_delete": self.is_delete
        }

class IDC(models.Model):

    class Meta:
        db_table = "idc"

    city_id = models.BigIntegerField(help_text="关联城市id")
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    is_delete = models.BooleanField(default=False, help_text="软删除标记")

    def to_dict(self):
        return {
            "id": self.id,
            "city_id": self.city_id,
            "name": self.name,
            "address": self.address,
            "is_delete": self.is_delete
        }

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
    is_delete = models.BooleanField(default=False, help_text="软删除标记")

    def to_dict(self):
        return {
            "id": self.id,
            "idc_id": self.idc_id,
            "hostname": self.hostname,
            "ip_address": self.ip_address,
            "status": self.status,
            "root_password": self.root_password,
            "created_at": date_format(self.created_at, "%Y-%m-%d %H:%M:%S"),
            "updated_at": date_format(self.updated_at, "%Y-%m-%d %H:%M:%S"),
            "is_delete": self.is_delete
        }

class PasswordHistory(models.Model):

    class Meta:
        db_table = "password_history"

    host_id = models.BigIntegerField(help_text="主机关联id")
    old_password = models.CharField(max_length=255)
    changed_at = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False, help_text="软删除标记")

    def to_dict(self):
        return {
            "id": self.id,
            "host_id": self.host_id,
            "old_password": self.old_password,
            "changed_at": date_format(self.changed_at, "%Y-%m-%d %H:%M:%S"),
            "is_delete": self.is_delete
        }