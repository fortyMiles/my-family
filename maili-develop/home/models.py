from django.db import models

# Create your models here.


class Home(models.Model):
    home_id = models.CharField(max_length=30, unique=True)
    owner = models.CharField(max_length=13)
    avatar = models.CharField(max_length=30)

    class Meta:
        db_table = 'home'
