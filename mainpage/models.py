from django.db import models

# Create your models here.
class Projects(models.Model):
    project_name = models.CharField(max_length=100, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'projects'


class Project_contents(models.Model):
    category = models.CharField(max_length=100, null=True, blank=True)
    topic = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    contents = models.TextField
    category_index = models.IntegerField(default= -1)
    state_index = models.IntegerField(default= -1)
    image = models.TextField(null=True, blank=True)
    project_name = models.ForeignKey('mainpage.Projects', on_delete=models.CASCADE, db_column='project_name',
                                     null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'project_contents'

class User_Project(models.Model):
    project_name = models.ForeignKey('mainpage.Projects', on_delete=models.CASCADE, db_column='project_name',
                              null=True, blank=True)
    email = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='email',
                              null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user_project'

class Comments(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='email',
                              null=True, blank=True)
    contents = models.TextField
    project_name = models.ForeignKey('mainpage.Projects', on_delete=models.CASCADE, db_column='project_name',
                              null=True, blank=True)
    topic = models.ForeignKey('mainpage.Project_contents', on_delete=models.CASCADE, db_column='topic',
                                     null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'comments'
