from django.contrib import admin

from taskmanager.models import Project, Task, User

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Task)