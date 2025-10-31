from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Event, RSVP, Review
from .serializers import EventSerializer, RSVPSerializer, ReviewSerializer
from .permissions import IsOrganizerOrReadOnly, IsInvitedOrPublicEvent
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django.db.models import Q

from events import models


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOrganizerOrReadOnly, IsInvitedOrPublicEvent]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter]
    search_fields = ['title', 'location', 'organizer__username']

    def get_queryset(self):
        # List only public or private events user can see
        user = self.request.user
        return Event.objects.filter(
            Q(is_public=True) |
            Q(invited_users=user) |
            Q(organizer=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class RSVPViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, event_pk=None):
        event = get_object_or_404(Event, pk=event_pk)
        serializer = RSVPSerializer(data=request.data)
        if serializer.is_valid():
            # Prevent duplicate RSVPs
            rsvp, created = RSVP.objects.update_or_create(
                event=event, user=request.user, defaults={'status': serializer.validated_data['status']}
            )
            return Response(RSVPSerializer(rsvp).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, event_pk=None, user_pk=None):
        rsvp = get_object_or_404(RSVP, event_id=event_pk, user_id=user_pk)
        if rsvp.user != request.user:
            return Response({"detail": "Cannot update RSVP for another user."}, status=status.HTTP_403_FORBIDDEN)
        serializer = RSVPSerializer(rsvp, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def list(self, request, event_pk=None):
        reviews = Review.objects.filter(event_id=event_pk)
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(reviews, request)
        serializer = ReviewSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request, event_pk=None):
        event = get_object_or_404(Event, pk=event_pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(event=event, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
