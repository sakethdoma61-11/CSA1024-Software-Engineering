from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from .models import Facility, Booking
from .services import create_booking, transition_booking

class BookingRulesTest(TestCase):
    def setUp(self):
        self.user=get_user_model().objects.create_user(username="student",password="TestPass123!")
        self.facility=Facility.objects.create(name="AI Lab",building="Block A",capacity=30)
        self.start=timezone.now()+timedelta(days=1)
    def test_booking_is_created(self):
        b=create_booking(user=self.user,facility=self.facility,purpose="Lab work",start_at=self.start,end_at=self.start+timedelta(hours=1))
        self.assertEqual(b.status,"REQUESTED")
    def test_overlapping_booking_is_rejected(self):
        create_booking(user=self.user,facility=self.facility,purpose="One",start_at=self.start,end_at=self.start+timedelta(hours=1))
        with self.assertRaises(Exception):
            create_booking(user=self.user,facility=self.facility,purpose="Two",start_at=self.start+timedelta(minutes=20),end_at=self.start+timedelta(hours=2))
    def test_invalid_transition_is_rejected(self):
        b=create_booking(user=self.user,facility=self.facility,purpose="One",start_at=self.start,end_at=self.start+timedelta(hours=1))
        with self.assertRaises(Exception): transition_booking(booking_id=b.pk,user=self.user,target="IN_USE")
