from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Task


class TaskAPITestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpassword'
        )

        self.client = APIClient()

        self.task = Task.objects.create(
            title='Learn Django',
            description='Study Django and REST framework',
            status='todo',
            owner=self.user
        )

    def test_unauthenticated_user_cannot_access_api(self):
        response = self.client.get('/api/tasks/')

        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_can_list_tasks(self):
        self.client.login(
            username='testuser',
            password='testpassword'
        )

        response = self.client.get('/api/tasks/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Learn Django')

    def test_authenticated_user_can_create_task(self):
        self.client.login(
            username='testuser',
            password='testpassword'
        )

        data = {
            'title': 'Build API',
            'description': 'Create the task API using DRF',
            'status': 'todo',
        }

        response = self.client.post(
            '/api/tasks/',
            data,
            format='json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(
            Task.objects.get(title='Build API').owner,
            self.user
        )

    def test_user_can_retrieve_task(self):
        self.client.login(
            username='testuser',
            password='testpassword'
        )

        response = self.client.get(
            f'/api/tasks/{self.task.id}/'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Learn Django')

    def test_user_can_update_task(self):
        self.client.login(
            username='testuser',
            password='testpassword'
        )

        data = {
            'title': 'Learn Django REST Framework',
            'description': 'Study Django and DRF',
            'status': 'in_progress',
        }

        response = self.client.put(
            f'/api/tasks/{self.task.id}/',
            data,
            format='json'
        )

        self.assertEqual(response.status_code, 200)

        self.task.refresh_from_db()

        self.assertEqual(
            self.task.title,
            'Learn Django REST Framework'
        )
        self.assertEqual(
            self.task.status,
            'in_progress'
        )

    def test_user_can_delete_task(self):
        self.client.login(
            username='testuser',
            password='testpassword'
        )

        response = self.client.delete(
            f'/api/tasks/{self.task.id}/'
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Task.objects.count(), 0)

    def test_search_title(self):
        self.client.login(
            username='testuser',
            password='testpassword'
        )

        response = self.client.get(
            '/api/tasks/?search=Django'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Learn Django')

    def test_search_description(self):
        self.client.login(
            username='testuser',
            password='testpassword'
        )

        response = self.client.get(
            '/api/tasks/?search=REST'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Learn Django')

    def test_all_users_can_see_all_tasks(self):
        Task.objects.create(
            title='Other User Task',
            description='A task created by another user',
            status='done',
            owner=self.other_user
        )

        self.client.login(
            username='testuser',
            password='testpassword'
        )

        response = self.client.get('/api/tasks/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
