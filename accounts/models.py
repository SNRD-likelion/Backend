from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=100, unique=True, default='email@example.com')
    password = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=30, null=True)
    information = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users'