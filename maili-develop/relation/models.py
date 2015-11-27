# -*- coding:utf-8 -*-
from django.db import models


class RelationValue(models.Model):
    title = models.CharField(max_length=10)
    weight = models.IntegerField()
    abbr = models.CharField(max_length=10)
    level = models.IntegerField()
    cft = models.CharField(max_length=10)
    cfa = models.CharField(max_length=10)
    cmt = models.CharField(max_length=10)
    cma = models.CharField(max_length=10)


class Relationship(models.Model):
    user_from = models.CharField(max_length=15)
    user_to = models.CharField(max_length=15)
    relation = models.CharField(max_length=15)
    nickname = models.CharField(max_length=15, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

class Contract(models.Model):
    ''' 朋友，也即通讯录 '''
    user_id = models.UUIDField(db_index=True)  # 谁的通讯录
    friend_id = models.UUIDField()  # 朋友id
    friend_name = models.CharField(max_length=40)  # 朋友的名称
    friend_phone = models.CharField(max_length=18)  # 朋友的手机
    remark_name = models.CharField(max_length=40)  # 备注名，默认是contact_name
    first_char = models.CharField(max_length=1, blank=True, default=None)  # 首字母，便于搜索
    remark_tags = models.CharField(max_length=50, blank=True, default=None)  # 标签
    send_msg_count = models.IntegerField(default=0)  # 发送了几条消息
    receive_msg_count = models.IntegerField(default=0)  # 收到几条消息
    unread_msgs = models.IntegerField(default=0)  # 几条未读消息
    deleted = models.BooleanField(default=False)
    relation = models.CharField(max_length=40, default='friend')  # 关系<朋友，姐姐，妹妹等>

    class Meta:
        db_table = "contract"



