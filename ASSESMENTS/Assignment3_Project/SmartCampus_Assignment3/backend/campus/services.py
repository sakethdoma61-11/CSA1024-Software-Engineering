from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import Booking, AuditEvent, Approval, MaintenanceTicket
from .role_utils import campus_role

BOOKING_TRANSITIONS={
"REQUESTED":{"APPROVED","CANCELLED"},
"APPROVED":{"CONFIRMED","CANCELLED"},
"CONFIRMED":{"IN_USE","CANCELLED"},
"IN_USE":{"COMPLETED"},
"COMPLETED":set(),"CANCELLED":set()
}
TICKET_TRANSITIONS={"OPEN":{"ASSIGNED","CLOSED"},"ASSIGNED":{"IN_PROGRESS","OPEN"},
"IN_PROGRESS":{"RESOLVED","ASSIGNED"},"RESOLVED":{"CLOSED","IN_PROGRESS"},"CLOSED":set()}

def overlaps(facility,start,end,exclude_id=None):
    qs=Booking.objects.select_for_update().filter(facility=facility).exclude(status__in=["CANCELLED","COMPLETED"]).filter(start_at__lt=end,end_at__gt=start)
    if exclude_id: qs=qs.exclude(pk=exclude_id)
    return qs.exists()

@transaction.atomic
def create_booking(*,user,facility,purpose,start_at,end_at):
    if end_at <= start_at: raise ValidationError("End time must be later than start time.")
    if not facility.is_active: raise ValidationError("Facility is not available.")
    # Lock the facility row so competing requests serialize before checking overlaps.
    from .models import Facility
    Facility.objects.select_for_update().get(pk=facility.pk)
    if overlaps(facility,start_at,end_at): raise ValidationError("Facility already has an overlapping booking.")
    booking=Booking.objects.create(requester=user,facility=facility,purpose=purpose,start_at=start_at,end_at=end_at)
    AuditEvent.objects.create(actor=user,entity_type="Booking",entity_id=booking.pk,action="BOOKING_REQUESTED")
    return booking

@transaction.atomic
def transition_booking(*,booking_id,user,target,reason=""):
    booking=Booking.objects.select_for_update().get(pk=booking_id)
    allowed=BOOKING_TRANSITIONS.get(booking.status,set())
    if target not in allowed: raise ValidationError(f"Invalid booking transition: {booking.status} -> {target}")
    if target=="APPROVED" and not (user.is_staff or campus_role(user) in {"FACILITY_MANAGER","DEPARTMENT_APPROVER","ADMIN"}):
        raise PermissionDenied("Only an authorized approver can approve bookings.")
    booking.status=target; booking.version+=1; booking.save(update_fields=["status","version","updated_at"])
    if target in {"APPROVED","CANCELLED"}:
        Approval.objects.create(booking=booking,approver=user,decision="APPROVED" if target=="APPROVED" else "REJECTED",reason=reason)
    AuditEvent.objects.create(actor=user,entity_type="Booking",entity_id=booking.pk,action=f"BOOKING_{target}",detail={"version":booking.version})
    return booking

@transaction.atomic
def transition_ticket(*,ticket_id,user,target,assignee=None,note=""):
    ticket=MaintenanceTicket.objects.select_for_update().get(pk=ticket_id)
    if target not in TICKET_TRANSITIONS.get(ticket.status,set()): raise ValidationError(f"Invalid ticket transition: {ticket.status} -> {target}")
    if target in {"ASSIGNED","IN_PROGRESS","RESOLVED","CLOSED"} and not (user.is_staff or campus_role(user) in {"TECHNICIAN","FACILITY_MANAGER","ADMIN"}):
        raise PermissionDenied("Technician or manager role required.")
    ticket.status=target; ticket.version+=1
    if assignee is not None: ticket.assigned_to=assignee
    if note: ticket.resolution_note=note
    ticket.save()
    AuditEvent.objects.create(actor=user,entity_type="MaintenanceTicket",entity_id=ticket.pk,action=f"TICKET_{target}",detail={"version":ticket.version})
    return ticket
