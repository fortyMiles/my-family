# -*- coding:utf-8 -*-

import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    GENDERS = (
        ('M', u'男'),
        ('F', u'女'),
        ('N', u'未知'),
    )
    ROLES = (
        ('normal', u'普通用户'),
        ('tutor', u'麦粒导师'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=18, unique=True)  # 必填项，且唯一
    nickname = models.CharField(max_length=30)  # 昵称如果不填默认就是张小姐、陈先生
    first_name = models.CharField(max_length=20, blank=True)  # 名字选填
    last_name = models.CharField(max_length=20)  # 姓氏必填
    full_name = models.CharField(max_length=40, blank=True, db_index=True)  # 可起到搜索作用
    avatar = models.CharField(max_length=50, default="/avator")  # 没有则会有默认头像
    tagline = models.CharField(max_length=140, blank=True)  # 个人的签名档
    gender = models.CharField(max_length=1, default='N', choices=GENDERS)
    marital_status = models.BooleanField(default=False)  # 婚否
    birthday = models.DateField(null=True, blank=True, default=None)
    country = models.CharField(max_length=30, blank=True)
    province = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=10, choices=ROLES, default="normal")
    is_active = models.BooleanField(default=False)  # 是否激活
    activate_at = models.DateTimeField(auto_now_add=True)  # 激活的时间
    # activate_at = models.DateTimeField(default=None, blank=True)  # 激活的时间
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_login = models.BooleanField(default=False, blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        db_table = 'user'


class Relationship(models.Model):
    ''' 关系表 '''
    from_user_id = models.UUIDField(db_index=True)
    to_user_id = models.UUIDField(db_index=True)
    relation = models.CharField(max_length=15, db_index=True)  # 关系的名称
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "relationship"


class Friendship(models.Model):
    ''' 朋友，也即通讯录 '''
    user_id = models.UUIDField(db_index=True)  # 谁的通讯录
    friend_id = models.UUIDField()  # 朋友id
    friend_name = models.CharField(max_length=40)  # 朋友的名称
    friend_phone = models.CharField(max_length=18)  # 朋友的手机
    remark_name = models.CharField(max_length=40)  # 备注名，默认是contact_name
    first_char = models.CharField(max_length=1)  # 首字母，便于搜索
    remark_tags = models.CharField(max_length=50)  # 标签
    send_msg_count = models.IntegerField(default=0)  # 发送了几条消息
    receive_msg_count = models.IntegerField(default=0)  # 收到几条消息
    unread_msgs = models.IntegerField(default=0)  # 几条未读消息
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "friendship"


class UserCounter(models.Model):
    ''' 计数器: 用在一些需要计数的地方，比如多少条未读消息，多少条新状态 '''
    user_id = models.UUIDField(primary_key=True)
    unread_msgs = models.IntegerField(default=0)
    unread_feeds = models.IntegerField(default=0)
    unread_comments = models.IntegerField(default=0)
    unread_invitations = models.IntegerField(default=0)
    unread_topics = models.IntegerField(default=0)
    chat_ats = models.IntegerField(default=0)
    feed_ats = models.IntegerField(default=0)
    # should be more...
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_counter'


class Captcha(models.Model):
    ''' 验证码：分不同purposes，可能是发到手机，也可能是发到邮箱 '''
    PURPOSES = (
        ('register', u'注册用户'),
        ('changeEmail', u'更换邮箱'),
        ('resetPasswd', u'重置密码')
    )
    phone = models.CharField(max_length=18)
    code = models.CharField(max_length=10, db_index=True)  # 验证码
    purpose = models.CharField(max_length=15, choices=PURPOSES, default='register')
    created_at = models.DateTimeField(auto_now_add=True)
    send_at = models.DateTimeField(blank=True, null=True, default=None)
    send = models.BooleanField(default=False)
    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(blank=True, null=True, default=None)
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'captcha'


class Invitation(models.Model):
    ''' 如果invitee为空（未注册或者找不到Ta），可以通过phone或者email邀请 '''
    inviter_id = models.UUIDField(db_index=True)  # 邀请者
    invitee_id = models.UUIDField(db_index=True)  # 被邀请者
    phone = models.CharField(max_length=18)
    relation = models.CharField(max_length=15)  # invitee是inviter的什么人
    message = models.CharField(max_length=200)  # 邀请语
    invitation_code = models.CharField(max_length=10)  # 也可以邀请码的方式
    invitation_url = models.CharField(max_length=100)  # 邀请链接
    accepted = models.BooleanField(default=False)
    ignore = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'invitation'


class AppSetting(models.Model):
    ''' App的一些设置 '''
    user_id = models.UUIDField(primary_key=True)
    language = models.CharField(max_length=10)
    background_pic = models.CharField(max_length=50)
    searchable = models.BooleanField(default=True)
    remind_of_new_msg = models.BooleanField(default=True)
    auto_update = models.BooleanField(default=True)
    # should be more...

    class Meta:
        db_table = 'app_setting'
