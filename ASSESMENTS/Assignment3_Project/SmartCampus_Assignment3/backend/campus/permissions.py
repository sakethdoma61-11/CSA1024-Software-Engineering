from rest_framework.permissions import BasePermission
from .role_utils import campus_role

class IsCampusUser(BasePermission):
    def has_permission(self,request,view):
        return bool(request.user and request.user.is_authenticated)

class IsManagerOrAdmin(BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and (request.user.is_staff or campus_role(request.user) in {"FACILITY_MANAGER","ADMIN","DEPARTMENT_APPROVER"})

class IsTechnicianOrManager(BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and (request.user.is_staff or campus_role(request.user) in {"TECHNICIAN","FACILITY_MANAGER","ADMIN"})
