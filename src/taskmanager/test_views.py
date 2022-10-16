import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from taskmanager.models import Task, User, Project
from taskmanager.serializers import TaskSerializer
from taskmanager.utils import JSONResponse

def print_test_data(func):
    """
    The function is a decorator for prints function name at start test and
    success status after finishing the function test.
    """
    def inner1(*args, **kwargs):
        print(f"\n[TEST] {func.__name__}  ::",end=" ")
        try:
            func(*args, **kwargs)
            print("PASSED")
        except Exception as e:
            print("FAILED")
            raise e

    return inner1


class AccountTests(APITestCase):
    """
    Test cases about User accounts, signup, and login
    """
    def setUp(self) -> None:
        self.url = reverse("signup")
        

    @print_test_data
    def test_signup_valid_user(self):
        """
        Ensure we can signup a new user.
        """
        username = "developer-1"
        password = "pass"
        dev_role = "developer"
        
        data = {
            "username": username,
            "password": password,
            "user_role": dev_role,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, username)

    @print_test_data
    def test_signup_invalid_user(self):
        """
        Ensure user can not signup with wrong data.
        """
        data = {
            "username": "",
            "password": "",
            "user_role": "wrong",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TaskTests(APITestCase):
    """
    Test cases are about create, retrive, and update tasks.
    
    The test data structure is like below:
        manager_1: {
            projects:[
                manager_1_proj_1:{
                    developers:[developer_1, developer_2],
                    tasks:[
                        task_11:{
                            assignee:[developer_1 ]
                        },
                        task_12
                    ]
                }
                manager_1_proj_2:{
                    developers:[ developer_3 ],
                    tasks:[]
                }
            ]
        }
        manager_2: {
            projects:[]
        }

    """

    def setUp(self):
        # Creating managers::
        self.manager_1_data = {
            "username": "manager-1",
            "password": "pass",
            "user_role": "manager",
        }
        self.manager_2_data = {
            "username": "manager-2",
            "password": "pass",
            "user_role": "manager",
        }
        self.manager_1 = User.objects.create_user(
            username=self.manager_1_data["username"],
            password=self.manager_1_data["password"],
            user_role=self.manager_1_data["user_role"],
        )
        self.manager_2 = User.objects.create_user(
            username=self.manager_2_data["username"],
            password=self.manager_2_data["password"],
            user_role=self.manager_2_data["user_role"],
        )

        # Creating developers::
        self.developer_1_data = {
            "username": "developer-1",
            "password": "pass",
            "user_role": "developer",
        }
        self.developer_2_data = {
            "username": "developer-2",
            "password": "pass",
            "user_role": "developer",
        }
        self.developer_3_data = {
            "username": "developer-3",
            "password": "pass",
            "user_role": "developer",
        }
        self.developer_1 = User.objects.create_user(
            username=self.developer_1_data["username"],
            password=self.developer_1_data["password"],
            user_role=self.developer_1_data["user_role"],
        )
        self.developer_2 = User.objects.create_user(
            username=self.developer_2_data["username"],
            password=self.developer_2_data["password"],
            user_role=self.developer_2_data["user_role"],
        )
        self.developer_3 = User.objects.create_user(
            username=self.developer_3_data["username"],
            password=self.developer_3_data["password"],
            user_role=self.developer_3_data["user_role"],
        )

        # Creating projects
        self.manager_1_proj_1 = self.manager_1.manager_projects.create(name="proj-11")
        self.manager_1_proj_2 = self.manager_1.manager_projects.create(name="proj-12")

        # Add developers to the projects
        self.manager_1_proj_1.developers.add(self.developer_1)
        self.manager_1_proj_1.developers.add(self.developer_2)
        self.manager_1_proj_2.developers.add(self.developer_3)

        # Creating tasks
        self.task_11 = self.manager_1_proj_1.tasks.create(
            title="task-11", creator=self.manager_1
        )
        self.task_12 = self.manager_1_proj_1.tasks.create(
            title="task-12", creator=self.manager_1
        )

        # Assign tasks to assignee
        self.task_11.assignee.add(self.developer_1)

    @print_test_data
    def test_get_project_all_tasks_by_manager(self):
        """
        Test getting project tasks with the project manager.
        """
        manager_1_proj_tasks = Task.objects.filter(project=self.manager_1_proj_1)
        serializer = TaskSerializer(manager_1_proj_tasks, many=True)
        
        self.client.login(
            username=self.manager_1_data["username"],
            password=self.manager_1_data["password"],
        )
        response = self.client.get(
            reverse(
                "get_project_tasks", kwargs={"project_id": self.manager_1_proj_1.pk}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    @print_test_data
    def test_get_project_all_tasks_by_its_developer(self):
        """
        Test getting project tasks by a developer that is one of the project developers.
        """
        manager_1_proj_tasks = Task.objects.filter(project=self.manager_1_proj_1)
        serializer = TaskSerializer(manager_1_proj_tasks, many=True)
        self.client.login(
            username=self.developer_1_data["username"],
            password=self.developer_1_data["password"],
        )
        response = self.client.get(
            reverse(
                "get_project_tasks", kwargs={"project_id": self.manager_1_proj_1.pk}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    @print_test_data
    def test_prevent_get_project_all_tasks_by_stranger_manager(self):
        """
        Test prevent getting tasks with a manager that is not the project creator.
        """
        self.client.login(
            username=self.manager_2_data["username"],
            password=self.manager_2_data["password"],
        )
        response = self.client.get(
            reverse(
                "get_project_tasks", kwargs={"project_id": self.manager_1_proj_1.pk}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, JSONResponse.PERMISSION_DENIED)

    @print_test_data
    def test_get_projects_assignee_all_tasks_by_project_manager(self):
        """
        Test getting a project assignee tasks by project manager.
        """
        manager_1_proj_tasks = Task.objects.filter(
            project=self.manager_1_proj_1
        ).filter(assignee__id=self.developer_1.id)

        serializer = TaskSerializer(manager_1_proj_tasks, many=True)
        self.client.login(
            username=self.manager_1_data["username"],
            password=self.manager_1_data["password"],
        )

        response = self.client.get(
            reverse(
                "get_project_assignee_tasks",
                kwargs={
                    "project_id": self.manager_1_proj_1.pk,
                    "assignee_id": self.developer_1.id,
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    @print_test_data
    def test_create_project_task_by_its_manager(self):
        """
        Test creating a project task by the project manager.
        """
        self.client.login(
            username=self.manager_1_data["username"],
            password=self.manager_1_data["password"],
        )
        task_data = {
            "title":"new-task",
            "description":"It is a new task",
        }
        response = self.client.post(
            reverse(
                "create_task",
                kwargs={
                    "project_id": self.manager_1_proj_1.id
                },
            ),
            data=json.dumps(task_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @print_test_data
    def test_create_project_task_by_its_developer(self):
        """
        Test creating a task for a project by a project developer.
        """
        self.client.login(
            username=self.developer_1_data["username"],
            password=self.developer_1_data["password"],
        )
        task_data = {
            "title":"new-task",
            "description":"It is a new task",
        }
        response = self.client.post(
            reverse(
                "create_task",
                kwargs={
                    "project_id": self.manager_1_proj_1.id
                },
            ),
            data=json.dumps(task_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @print_test_data
    def test_prevent_creating_project_task_by_stranger_manager(self):
        """
        Test prevent of creating a task for a project by stranger manager.
        """
        self.client.login(
            username=self.manager_2_data["username"],
            password=self.manager_2_data["password"],
        )
        task_data = {
            "title":"new-task",
            "description":"It is a new task",
        }
        response = self.client.post(
            reverse(
                "create_task",
                kwargs={
                    "project_id": self.manager_1_proj_1.id
                },
            ),
            data=json.dumps(task_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, JSONResponse.PERMISSION_DENIED)
    
    @print_test_data
    def test_prevent_creating_project_task_by_stranger_developer(self):
        """
        Test prevent of creating a task for a project by stranger developer.
        """
        self.client.login(
            username=self.developer_3_data["username"],
            password=self.developer_3_data["password"],
        )
        task_data = {
            "title":"new-task",
            "description":"It is a new task",
        }
        response = self.client.post(
            reverse(
                "create_task",
                kwargs={
                    "project_id": self.manager_1_proj_1.id
                },
            ),
            data=json.dumps(task_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, JSONResponse.PERMISSION_DENIED)
    
    @print_test_data
    def test_assign_task_to_another_assignee_by_project_manager(self):
        """
        Test creating a task for a project by a project developer.
        """
        self.client.login(
            username=self.developer_1_data["username"],
            password=self.developer_1_data["password"],
        )
        task_data = {
            "assignee":[self.developer_2.id]
        }
        response = self.client.put(
            reverse(
                "update_task",
                kwargs={
                    "project_id": self.manager_1_proj_1.id,
                    "pk":self.task_12.id
                },
            ),
            data=json.dumps(task_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @print_test_data
    def test_preventing_assign_task_to_stranger_assignee_by_project_manager(self):
        """
        Test creating a task for a project by a project developer.
        """
        self.client.login(
            username=self.developer_1_data["username"],
            password=self.developer_1_data["password"],
        )
        task_data = {
            "assignee":[self.developer_3.id]
        }
        response = self.client.put(
            reverse(
                "update_task",
                kwargs={
                    "project_id": self.manager_1_proj_1.id,
                    "pk":self.task_12.id
                },
            ),
            data=json.dumps(task_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, JSONResponse.ASSIGNE_IS_NOT_PROJ_MEMBER)