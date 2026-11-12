from rest_framework import serializers
from .models import Facility, Booking, MaintenanceTicket, SensorEvent, Approval, AuditEvent

class FacilitySerializer(serializers.ModelSerializer):
    class Meta: model=Facility; fields="__all__"
class BookingSerializer(serializers.ModelSerializer):
    requester_name=serializers.CharField(source="requester.username",read_only=True)
    facility_name=serializers.CharField(source="facility.name",read_only=True)
    class Meta:
        model=Booking
        fields=["id","facility","facility_name","requester","requester_name","purpose","start_at","end_at","status","version","created_at"]
        read_only_fields=["requester","status","version","created_at"]
    def validate(self,data):
        if data.get("end_at",getattr(self.instance,"end_at",None)) <= data.get("start_at",getattr(self.instance,"start_at",None)):
            raise serializers.ValidationError("End time must be later than start time.")
        return data
class TicketSerializer(serializers.ModelSerializer):
    facility_name=serializers.CharField(source="facility.name",read_only=True)
    reporter_name=serializers.CharField(source="reporter.username",read_only=True)
    assigned_name=serializers.CharField(source="assigned_to.username",read_only=True)
    class Meta:
        model=MaintenanceTicket
        fields="__all__"
        read_only_fields=["reporter","status","version","created_at","updated_at"]
class SensorEventSerializer(serializers.ModelSerializer):
    class Meta: model=SensorEvent; fields="__all__"; read_only_fields=["processed","created_at"]
class ApprovalSerializer(serializers.ModelSerializer):
    class Meta: model=Approval; fields="__all__"; read_only_fields=["approver","created_at"]
class AuditSerializer(serializers.ModelSerializer):
    class Meta: model=AuditEvent; fields="__all__"
