from django.contrib.auth.models import AbstractUser
from django.db import models




class User(AbstractUser):
    DEVELOPER = "developer"
    MANAGER = "manager"
    
    USER_ROLE = [
        (DEVELOPER, "DEVELOPER"), 
        (MANAGER, "MANAGER"),
       
    ]
    user_role = models.CharField(max_length=20, choices=USER_ROLE, default=MANAGER)
    


class Project(models.Model):
    
    name = models.TextField(blank=True, null=True)
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        related_name="manager_projects",
    )
    developers = models.ManyToManyField(User,related_name="projects")


class Task(models.Model):
   
    title = models.CharField(max_length=200, default="Task title")
    description = models.TextField(blank=True, null=True)
    is_done = models.BooleanField(default=False)
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        related_name="created_tasks",
    )    
    assignee = models.ManyToManyField(User, blank=True)



