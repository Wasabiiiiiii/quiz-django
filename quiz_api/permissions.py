from rest_framework import permissions
from django.contrib.auth import authenticate


class PartecipantGroup(permissions.BasePermission):
    ###
    # Check if form-data is correct and belongs to a valid user with partecipant group
    ###
    def has_permission(self, request, view):
        user = authenticate(
            username=request.data['username'], password=request.data['password'])
        if user is not None:
            if user.groups.filter(name='partecipant').exists():
                return True
        else:
            return False
