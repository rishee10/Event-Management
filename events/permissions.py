from rest_framework.permissions import BasePermission

class IsOrganizerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow GET requests
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Only organizer can edit/delete
        return obj.organizer == request.user

class IsInvitedOrPublicEvent(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.is_public:
            return True
        # Check if user is invited for private event
        return request.user in obj.invited_users.all() or request.user == obj.organizer
