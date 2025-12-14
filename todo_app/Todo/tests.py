from django.test import TestCase, Client
from django.urls import reverse
from .models import Task
from .form import TaskForm

# Create your tests here.

# --------------------
# Model Tests
# --------------------
class TaskModelTest(TestCase):
    def test_create_task(self):
        task = Task.objects.create(
            title="Test Task",
            description="Testing the task model",
            completed=False
        )
        self.assertEqual(task.title, "Test Task")
        self.assertFalse(task.completed)
        self.assertIsNotNone(task.created_at)

# --------------------
# Form Tests
# --------------------
class TaskFormTest(TestCase):
    def test_valid_form(self):
        data = {"title": "Form Task", "description": "Form test", "completed": False}
        form = TaskForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {"title": "", "description": "Missing title"}
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())

# --------------------
# View Tests
# --------------------
class TaskViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.task = Task.objects.create(
            title="View Task",
            description="Testing views",
            completed=False
        )

    def test_task_list_view(self):
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Task")

    def test_create_task_view(self):
        response = self.client.post(reverse("create_task"), {
            "title": "New Task",
            "description": "Created via test",
            "completed": False
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Task.objects.count(), 2)

    def test_update_task_view(self):
        response = self.client.post(reverse("update_task", args=[self.task.id]), {
            "title": "Updated Task",
            "description": "Updated via test",
            "completed": True
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")
        self.assertTrue(self.task.completed)

    def test_delete_task_view(self):
        response = self.client.post(reverse("delete_task", args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)

# --------------------
# URL Tests
# --------------------
class TaskURLTest(TestCase):
    def test_urls(self):
        self.assertEqual(reverse("task_list"), "/")
        self.assertEqual(reverse("create_task"), "/create_task/")