from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from campus.models import Facility, CampusProfile

class Command(BaseCommand):
    help="Create local demonstration users and facilities. Development only."
    def handle(self,*args,**kwargs):
        User=get_user_model()
        user,created=User.objects.get_or_create(username="student",defaults={"email":"student@example.test"})
        if created: user.set_password("CampusDemo123!"); user.save()
        CampusProfile.objects.update_or_create(user=user,defaults={"role":"STUDENT","campus_code":"MAIN"})
        manager,created=User.objects.get_or_create(username="manager",defaults={"email":"manager@example.test","is_staff":True})
        if created: manager.set_password("ManagerDemo123!"); manager.save()
        CampusProfile.objects.update_or_create(user=manager,defaults={"role":"FACILITY_MANAGER","campus_code":"MAIN"})
        tech,created=User.objects.get_or_create(username="technician",defaults={"email":"technician@example.test"})
        if created: tech.set_password("TechDemo123!"); tech.save()
        CampusProfile.objects.update_or_create(user=tech,defaults={"role":"TECHNICIAN","campus_code":"MAIN"})
        facilities=[
            ("AI Innovation Lab","Block A",30,["Computers","Projector"]),
            ("Seminar Hall","Block B",120,["Projector","Audio"]),
            ("Electronics Workshop","Block C",24,["Workbenches","Sensors"]),
            ("Central Library Room","Library",16,["Wi-Fi","Display"]),
        ]
        for name,building,capacity,equipment in facilities:
            Facility.objects.get_or_create(name=name,building=building,defaults={"capacity":capacity,"equipment":equipment})
        self.stdout.write(self.style.SUCCESS("Demo seed complete. Users: student / CampusDemo123!, manager / ManagerDemo123!, technician / TechDemo123!"))
