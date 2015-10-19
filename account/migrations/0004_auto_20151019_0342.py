# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20151019_0339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activate_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
