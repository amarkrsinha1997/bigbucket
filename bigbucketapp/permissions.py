from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    message  = 'You must be the owner of this content to change.'
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user.user_detail

class IsFarmerOrShopKeeper(permissions.BasePermission):
    message  = 'You must be the owner of this content to change.'
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user.user_type == '1' or obj.user.user_type == '2' 