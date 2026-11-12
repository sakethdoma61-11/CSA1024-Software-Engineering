from django.db import IntegrityError
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Facility, Booking, MaintenanceTicket, SensorEvent, AuditEvent
from .serializers import FacilitySerializer, BookingSerializer, TicketSerializer, SensorEventSerializer, AuditSerializer
from .permissions import IsManagerOrAdmin, IsTechnicianOrManager
from .services import create_booking, transition_booking, transition_ticket

class HealthViewSet(viewsets.ViewSet):
    permission_classes=[AllowAny]
    def list(self,request): return Response({"status":"ok","service":"smart-campus-api","time":timezone.now()})

class FacilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Facility.objects.filter(is_active=True)
    serializer_class=FacilitySerializer

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class=BookingSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        qs=Booking.objects.select_related("facility","requester")
        if self.request.user.is_staff or getattr(self.request.user,"campus_role","") in {"FACILITY_MANAGER","ADMIN","DEPARTMENT_APPROVER"}: return qs
        return qs.filter(requester=self.request.user)
    def perform_create(self,serializer):
        data=serializer.validated_data
        obj=create_booking(user=self.request.user,facility=data["facility"],purpose=data["purpose"],start_at=data["start_at"],end_at=data["end_at"])
        serializer.instance=obj
    @action(detail=True,methods=["post"])
    def transition(self,request,pk=None):
        target=request.data.get("target","")
        obj=transition_booking(booking_id=pk,user=request.user,target=target,reason=request.data.get("reason",""))
        return Response(self.get_serializer(obj).data)

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class=TicketSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        qs=MaintenanceTicket.objects.select_related("facility","reporter","assigned_to")
        if self.request.user.is_staff or getattr(self.request.user,"campus_role","") in {"TECHNICIAN","FACILITY_MANAGER","ADMIN"}: return qs
        return qs.filter(reporter=self.request.user)
    def perform_create(self,serializer):
        obj=serializer.save(reporter=self.request.user)
        AuditEvent.objects.create(actor=self.request.user,entity_type="MaintenanceTicket",entity_id=obj.pk,action="TICKET_CREATED")
    @action(detail=True,methods=["post"])
    def transition(self,request,pk=None):
        obj=transition_ticket(ticket_id=pk,user=request.user,target=request.data.get("target",""),note=request.data.get("note",""))
        return Response(self.get_serializer(obj).data)

class SensorEventViewSet(viewsets.ModelViewSet):
    queryset=SensorEvent.objects.select_related("facility")
    serializer_class=SensorEventSerializer
    permission_classes=[IsTechnicianOrManager]
    def perform_create(self,serializer):
        obj=serializer.save()
        # Example deterministic rule: high temperature threshold creates a maintenance ticket.
        if obj.metric.lower()=="temperature" and obj.value >= 45:
            MaintenanceTicket.objects.get_or_create(facility=obj.facility,title=f"Sensor alert: {obj.metric}",
                status="OPEN",defaults={"reporter":self.request.user,"description":f"Threshold event {obj.event_id}: {obj.value}","priority":"HIGH"})
        AuditEvent.objects.create(actor=self.request.user,entity_type="SensorEvent",entity_id=obj.pk,action="SENSOR_RECORDED")

class AuditViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=AuditEvent.objects.select_related("actor")
    serializer_class=AuditSerializer
    permission_classes=[IsManagerOrAdmin]
