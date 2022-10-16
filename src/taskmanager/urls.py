from django.urls import path
from taskmanager import views


get_task_list = views.TaskView.as_view({"get": "list"})
create_task = views.TaskView.as_view({"post": "create"})
update_task = views.TaskView.as_view({"put": "update"})

urlpatterns = [
    path("projects/<int:project_id>/tasks/", create_task, name="create_task"),
    path("projects/<int:project_id>/tasks", get_task_list, name="get_project_tasks"),
    path(
        "projects/<int:project_id>/assignee/<int:assignee_id>/tasks",
        get_task_list,
        name="get_project_assignee_tasks",
    ),
    path("projects/<int:project_id>/tasks/<int:pk>/", update_task, name="update_task"),
    path("projects/signup/", views.CreateUserView.as_view(), name="signup"),
]
