from django.db import models

# Create your models here.
class User(models.Model):
    session_id = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, default='email@example.com')
    password = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users'