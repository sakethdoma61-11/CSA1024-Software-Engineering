from rest_framework.routers import DefaultRouter
from .views import HealthViewSet, FacilityViewSet, BookingViewSet, TicketViewSet, SensorEventViewSet, AuditViewSet
router=DefaultRouter()
router.register("health",HealthViewSet,basename="health")
router.register("facilities",FacilityViewSet,basename="facilities")
router.register("bookings",BookingViewSet,basename="bookings")
router.register("tickets",TicketViewSet,basename="tickets")
router.register("sensor-events",SensorEventViewSet,basename="sensor-events")
router.register("audit",AuditViewSet,basename="audit")
urlpatterns=router.urls
