from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Event, RSVP, Review
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
import pytz

class EventManagementAPITests(APITestCase):

    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='pass1234')
        self.user2 = User.objects.create_user(username='user2', password='pass1234')

        # Generate JWT token for user1
        refresh = RefreshToken.for_user(self.user1)
        self.token = str(refresh.access_token)
        self.auth_header = f'Bearer {self.token}'

        # Sample event data
        self.event_data = {
            "title": "Test Event",
            "description": "Event description",
            "location": "Test Location",
            "start_time": (datetime.now(pytz.utc) + timedelta(days=1)).isoformat(),
            "end_time": (datetime.now(pytz.utc) + timedelta(days=2)).isoformat(),
            "is_public": True
        }

    def test_create_event(self):
        url = reverse('events-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.post(url, self.event_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.event_data['title'])
        self.assertEqual(response.data['organizer']['username'], self.user1.username)

    def test_list_events(self):
        # Create an event first
        Event.objects.create(
            organizer=self.user1,
            title="Existing Event",
            description="Some description",
            location="Some Location",
            start_time=datetime.now(pytz.utc),
            end_time=datetime.now(pytz.utc) + timedelta(hours=2),
            is_public=True
        )
        url = reverse('events-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 1)

    def test_rsvp_create(self):
        event = Event.objects.create(
            organizer=self.user1,
            title="RSVP Event",
            description="RSVP desc",
            location="Location",
            start_time=datetime.now(pytz.utc),
            end_time=datetime.now(pytz.utc) + timedelta(hours=3),
            is_public=True
        )

        url = reverse('rsvp-create', kwargs={'event_pk': event.pk})
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.post(url, {'status': 'Going'}, format='json')
        print("RSVP create errors:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'Going')
        self.assertEqual(response.data['user']['username'], self.user1.username)
    
    def test_review_create_and_list(self):
        event = Event.objects.create(
            organizer=self.user1,
            title="Review Event",
            description="Review desc",
            location="Location",
            start_time=datetime.now(pytz.utc),
            end_time=datetime.now(pytz.utc) + timedelta(hours=5),
            is_public=True
        )

        create_url = reverse('review-list-create', kwargs={'event_pk': event.pk})
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)

        review_data = {"rating": 5, "comment": "Great event!"}
        response = self.client.post(create_url, review_data, format='json')
        print("Review create errors:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 5)

        # List reviews
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 1)


