from django.conf import settings
from django.db import models
from django.utils import timezone


class CampusProfile(models.Model):
    class Role(models.TextChoices):
        STUDENT="STUDENT","Student"
        FACULTY="FACULTY","Faculty"
        DEPARTMENT_APPROVER="DEPARTMENT_APPROVER","Department approver"
        FACILITY_MANAGER="FACILITY_MANAGER","Facility manager"
        TECHNICIAN="TECHNICIAN","Maintenance technician"
        ADMIN="ADMIN","Administrator"
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="campus_profile")
    role=models.CharField(max_length=24,choices=Role.choices,default=Role.STUDENT)
    campus_code=models.CharField(max_length=40,default="MAIN")
    def __str__(self): return f"{self.user.username} ({self.role})"

class Facility(models.Model):
    name=models.CharField(max_length=120)
    building=models.CharField(max_length=120)
    capacity=models.PositiveIntegerField(default=1)
    equipment=models.JSONField(default=list, blank=True)
    is_active=models.BooleanField(default=True)
    def __str__(self): return f"{self.name} - {self.building}"

class Booking(models.Model):
    class Status(models.TextChoices):
        REQUESTED="REQUESTED","Requested"
        APPROVED="APPROVED","Approved"
        CONFIRMED="CONFIRMED","Confirmed"
        IN_USE="IN_USE","In use"
        COMPLETED="COMPLETED","Completed"
        CANCELLED="CANCELLED","Cancelled"
    facility=models.ForeignKey(Facility,on_delete=models.PROTECT,related_name="bookings")
    requester=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="bookings")
    purpose=models.CharField(max_length=250)
    start_at=models.DateTimeField()
    end_at=models.DateTimeField()
    status=models.CharField(max_length=12,choices=Status.choices,default=Status.REQUESTED)
    version=models.PositiveIntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=["start_at"]
        constraints=[models.CheckConstraint(condition=models.Q(end_at__gt=models.F("start_at")),name="booking_end_after_start")]
    def __str__(self): return f"{self.facility} / {self.start_at}"

class MaintenanceTicket(models.Model):
    class Status(models.TextChoices):
        OPEN="OPEN","Open"
        ASSIGNED="ASSIGNED","Assigned"
        IN_PROGRESS="IN_PROGRESS","In progress"
        RESOLVED="RESOLVED","Resolved"
        CLOSED="CLOSED","Closed"
    class Priority(models.TextChoices):
        LOW="LOW","Low"
        MEDIUM="MEDIUM","Medium"
        HIGH="HIGH","High"
        CRITICAL="CRITICAL","Critical"
    facility=models.ForeignKey(Facility,on_delete=models.PROTECT,related_name="tickets")
    reporter=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="reported_tickets")
    title=models.CharField(max_length=160)
    description=models.TextField()
    priority=models.CharField(max_length=10,choices=Priority.choices,default=Priority.MEDIUM)
    status=models.CharField(max_length=12,choices=Status.choices,default=Status.OPEN)
    assigned_to=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name="assigned_tickets")
    sla_due_at=models.DateTimeField(null=True,blank=True)
    resolution_note=models.TextField(blank=True)
    version=models.PositiveIntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=["-created_at"]

class SensorEvent(models.Model):
    facility=models.ForeignKey(Facility,on_delete=models.PROTECT,related_name="sensor_events")
    event_id=models.CharField(max_length=100,unique=True)
    metric=models.CharField(max_length=80)
    value=models.FloatField()
    observed_at=models.DateTimeField(default=timezone.now)
    processed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

class Approval(models.Model):
    booking=models.ForeignKey(Booking,null=True,blank=True,on_delete=models.CASCADE,related_name="approvals")
    ticket=models.ForeignKey(MaintenanceTicket,null=True,blank=True,on_delete=models.CASCADE,related_name="approvals")
    approver=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    decision=models.CharField(max_length=12,choices=[("APPROVED","Approved"),("REJECTED","Rejected")])
    reason=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

class AuditEvent(models.Model):
    actor=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL)
    entity_type=models.CharField(max_length=50)
    entity_id=models.PositiveIntegerField()
    action=models.CharField(max_length=80)
    detail=models.JSONField(default=dict,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
