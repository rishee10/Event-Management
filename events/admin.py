# Register your models here.
from django.contrib import admin
from .models import UserProfile, Event, RSVP, Review

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'location')
    search_fields = ('full_name', 'user__username', 'location')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'location', 'start_time', 'end_time', 'is_public')
    list_filter = ('is_public', 'location', 'start_time')
    search_fields = ('title', 'organizer__username', 'location')

@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'status')
    list_filter = ('status',)
    search_fields = ('event__title', 'user__username')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('event__title', 'user__username', 'comment')
