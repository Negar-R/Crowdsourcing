from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import login

from tasks.models import TaskModel
from accounts.models import UserProfile

# Create your tests here.


class TestTaskView(TestCase):

    def setUp(self):
        self.client = Client()
        self.all_task = reverse('all_task')
        self.reported_task = reverse('reported_task')
        self.assigned_task = reverse('assigned_task')
        self.task_assignment = reverse('task_assign')
        self.add_task = reverse('add_task')

        self.reported_user = User.objects.create(
            username='reported_user',
            email='reported_user@example.com'
        )
        self.reported_user.set_password('1234')
        self.reported_user.save()

        self.assigned_user = User.objects.create(
            username='assigned_user',
            email='assigned_user@example.com'
        )
        self.assigned_user.set_password('5678')
        self.assigned_user.save()

        self.task = TaskModel.objects.create(
            title='task_title',
            value=5000,
            estimation=3,
            deadline='2021-03-10',
            description='task_description',
            reporter=self.reported_user,
            
        )

        self.see_description = reverse('see_description', args=[self.task.id])

    def test_get_all_Task(self):
        response = self.client.get(self.all_task)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(TaskModel.objects.count(), 1)
        self.assertTemplateUsed(response, 'get_task.html')

    def test_see_task_description(self):
        response = self.client.get(self.see_description)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['description'], 'task_description')
        self.assertTemplateUsed(response, 'show_description.html')

    def test_get_reported_task(self):
        response = self.client.get(self.reported_task)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func.__name__,
                         'getReportedTask')
        self.assertEqual(TaskModel.objects.filter(
                         reporter=self.reported_user).count(), 1)

    def test_assignment_task(self):
        self.client.login(username='assigned_user',
                          password='5678')

        post_data = {
            'assignee': self.assigned_user.username,
            'task_id': self.task.id
        }
        response = self.client.post(self.task_assignment, data=post_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__,
                         'assignTask')
        self.assertEqual(
            TaskModel.objects.get(id=self.task.id).assignee.username,
            self.assigned_user.username)
    
    def test_add_task_GET(self):
        UserProfile.objects.create(user=self.reported_user,
                                   user_type=UserProfile.AGENT)
        self.client.login(username='reported_user',
                          password='1234')
        response = self.client.get(self.add_task)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_form.html')

    def test_add_task_POST(self):
        UserProfile.objects.create(user=self.reported_user,
                                   user_type=UserProfile.AGENT)
        self.client.login(username='reported_user',
                          password='1234')
        
        post_data = {
            'title': 'added_task_title',
            'value': 3000,
            'estimation': 8,
            'deadline': '2020-12-20',
            'description': 'added_task_description'
        }
        response = self.client.post(self.add_task, data=post_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            TaskModel.objects.get(title='added_task_title').reporter.username,
            self.reported_user.username)
        self.assertEqual(TaskModel.objects.count(), 2)