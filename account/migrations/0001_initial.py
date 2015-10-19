# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppSetting',
            fields=[
                ('user_id', models.UUIDField(serialize=False, primary_key=True)),
                ('language', models.CharField(max_length=10)),
                ('background_pic', models.CharField(max_length=50)),
                ('searchable', models.BooleanField(default=True)),
                ('remind_of_new_msg', models.BooleanField(default=True)),
                ('auto_update', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'app_setting',
            },
        ),
        migrations.CreateModel(
            name='Captcha',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=18)),
                ('code', models.CharField(max_length=10, db_index=True)),
                ('purpose', models.CharField(default=b'register', max_length=15, choices=[(b'register', '\u6ce8\u518c\u7528\u6237'), (b'changeEmail', '\u66f4\u6362\u90ae\u7bb1'), (b'resetPasswd', '\u91cd\u7f6e\u5bc6\u7801')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('send_at', models.DateTimeField(default=None, null=True, blank=True)),
                ('send', models.BooleanField(default=False)),
                ('used', models.BooleanField(default=False)),
                ('used_at', models.DateTimeField(default=None, null=True, blank=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'captcha',
            },
        ),
        migrations.CreateModel(
            name='FriendShip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.UUIDField(db_index=True)),
                ('friend_id', models.UUIDField()),
                ('friend_name', models.CharField(max_length=40)),
                ('friend_phone', models.CharField(max_length=18)),
                ('remark_name', models.CharField(max_length=40)),
                ('first_char', models.CharField(max_length=1)),
                ('remark_tags', models.CharField(max_length=50)),
                ('send_msg_count', models.IntegerField(default=0)),
                ('receive_msg_count', models.IntegerField(default=0)),
                ('unread_msgs', models.IntegerField(default=0)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'friendship',
            },
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inviter_id', models.UUIDField(db_index=True)),
                ('invitee_id', models.UUIDField(db_index=True)),
                ('phone', models.CharField(max_length=18)),
                ('relation', models.CharField(max_length=15)),
                ('message', models.CharField(max_length=200)),
                ('invitation_code', models.CharField(max_length=10)),
                ('invitation_url', models.CharField(max_length=100)),
                ('accepted', models.BooleanField(default=False)),
                ('ignore', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'invitation',
            },
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_user_id', models.UUIDField(db_index=True)),
                ('to_user_id', models.UUIDField(db_index=True)),
                ('relation', models.CharField(max_length=15, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'relationship',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('phone', models.CharField(unique=True, max_length=18)),
                ('nickname', models.CharField(max_length=30)),
                ('first_name', models.CharField(max_length=20, blank=True)),
                ('last_name', models.CharField(max_length=20)),
                ('full_name', models.CharField(db_index=True, max_length=40, blank=True)),
                ('avatar', models.CharField(max_length=50)),
                ('tagline', models.CharField(max_length=140, blank=True)),
                ('gender', models.CharField(default=b'N', max_length=1, choices=[(b'M', '\u7537'), (b'F', '\u5973'), (b'N', '\u672a\u77e5')])),
                ('marital_status', models.BooleanField(default=False)),
                ('birthday', models.DateField(default=None, null=True, blank=True)),
                ('country', models.CharField(max_length=30, blank=True)),
                ('province', models.CharField(max_length=30, blank=True)),
                ('city', models.CharField(max_length=30, blank=True)),
                ('role', models.CharField(default=b'normal', max_length=10, choices=[(b'normal', '\u666e\u901a\u7528\u6237'), (b'tutor', '\u9ea6\u7c92\u5bfc\u5e08')])),
                ('is_active', models.BooleanField(default=False)),
                ('activate_at', models.DateTimeField(default=None)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='UserCounter',
            fields=[
                ('user_id', models.UUIDField(serialize=False, primary_key=True)),
                ('unread_msgs', models.IntegerField(default=0)),
                ('unread_feeds', models.IntegerField(default=0)),
                ('unread_comments', models.IntegerField(default=0)),
                ('unread_invitations', models.IntegerField(default=0)),
                ('unread_topics', models.IntegerField(default=0)),
                ('chat_ats', models.IntegerField(default=0)),
                ('feed_ats', models.IntegerField(default=0)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'user_counter',
            },
        ),
    ]
