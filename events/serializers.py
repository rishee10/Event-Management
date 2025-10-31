from rest_framework import serializers
from .models import UserProfile, Event, RSVP, Review
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'full_name', 'bio', 'location', 'profile_picture']

class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'organizer', 'location', 'start_time', 'end_time', 'is_public', 'created_at', 'updated_at']

class RSVPSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = RSVP
        fields = ['id', 'event', 'user', 'status']
        read_only_fields=['event', 'user']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'event', 'user', 'rating', 'comment', 'created_at']
        read_only_fields=['event', 'user', 'created_at']
        
