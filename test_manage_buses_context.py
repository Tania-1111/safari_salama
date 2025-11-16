import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schooltransport.setting')
django.setup()

from django.contrib.auth.models import User
from schooltransport.models import School, Route

# Get admin
admin = User.objects.get(username='admin1')
school = School.objects.get(admin=admin)

# Get context data like the view does
drivers = User.objects.filter(profile__user_type='driver')
attendants = User.objects.filter(profile__user_type='attendant')
routes = Route.objects.filter(school=school)

print(f'School: {school.name}')
print(f'Drivers: {drivers.count()}')
for d in drivers:
    print(f'  - {d.id}: {d.get_full_name()} ({d.username})')

print(f'\nAttendants: {attendants.count()}')
for a in attendants:
    print(f'  - {a.id}: {a.get_full_name()} ({a.username})')

print(f'\nRoutes: {routes.count()}')
for r in routes:
    print(f'  - {r.id}: {r.name} ({r.start_location} → {r.end_location})')
