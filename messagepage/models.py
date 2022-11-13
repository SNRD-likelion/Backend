from django.db import models

# Create your models here.
class Messages(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='email',
                              null=True, blank=True)
    contents = models.TextField
    project_name = models.ForeignKey('mainpage.Projects', on_delete=models.CASCADE, db_column='project_name',
                              null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'messages'