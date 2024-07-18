# Portal/models.py

from django.db import models
from django.contrib.auth.models import User

class ProjectRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('Requested', 'Requested'), ('In Progress', 'In Progress'), ('Completed', 'Completed')])

    def __str__(self):
        return self.project_name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.user.username} at {self.timestamp}'
    
class Milestone(models.Model):
    project = models.ForeignKey(ProjectRequest, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    image = models.ImageField(upload_to='milestone_images/', null=True, blank=True)

    def __str__(self):
        return self.title
    
    