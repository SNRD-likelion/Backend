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
    project_name = models.ForeignKey('mainpage.Projects', related_name='+', on_delete=models.CASCADE, db_column='project_name',
                                     null=True, blank=True)
    project_id = models.ForeignKey('mainpage.Projects', related_name='+', on_delete=models.CASCADE, db_column='project_id',
                                   null=True, blank=True)
    using = models.IntegerField(default= 0) # 누가 수정중이면 1, 수정가능하면 0

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'project_contents'

class User_Project(models.Model):
    project_id = models.ForeignKey('mainpage.Projects', on_delete=models.CASCADE, db_column='project_id', null=True, blank=True)
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
    project_id = models.ForeignKey('mainpage.Projects', on_delete=models.CASCADE, db_column='project_id', null=True, blank=True)
    topic = models.ForeignKey('mainpage.Project_contents', related_name='+', on_delete=models.CASCADE, db_column='topic',
                                     null=True, blank=True)
    state = models.ForeignKey('mainpage.Project_contents', related_name='+', on_delete=models.CASCADE, db_column='state', null=True, blank=True)
    category = models.ForeignKey('mainpage.Project_contents', related_name='+', on_delete=models.CASCADE, db_column='category',
                                 null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'comments'
