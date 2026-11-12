from django.contrib import admin
from .models import Facility,Booking,MaintenanceTicket,SensorEvent,Approval,AuditEvent,CampusProfile
admin.site.register([Facility,Booking,MaintenanceTicket,SensorEvent,Approval,AuditEvent,CampusProfile])
