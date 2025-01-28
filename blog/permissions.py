from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only authors to edit their posts.
    Readers can only view and comment.
    """

    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list', 'comment']:
            return True

        # Check if the user is authenticated and has the correct role
        if request.user.is_authenticated:
            if request.user.role == 'author':
                return True
            elif request.user.role == 'reader' and view.action in ['create']:
                return False
            return False
        return False

    def has_object_permission(self, request, view, obj):
        # Allow authors to update, delete their own posts
        if view.action in ['update', 'partial_update', 'destroy']:
            return obj.author == request.user
        return True
