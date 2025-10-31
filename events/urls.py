from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, RSVPViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='events')

rsvp_list = RSVPViewSet.as_view({'post': 'create'})
rsvp_update = RSVPViewSet.as_view({'patch': 'partial_update'})
review_list = ReviewViewSet.as_view({'get': 'list', 'post': 'create'})



urlpatterns = [
    path('', include(router.urls)),
    path('events/<int:event_pk>/rsvp/', rsvp_list, name='rsvp-create'),
    path('events/<int:event_pk>/rsvp/<int:user_pk>/', rsvp_update, name='rsvp-update'),
    path('events/<int:event_pk>/reviews/', review_list, name='review-list-create'),
]
