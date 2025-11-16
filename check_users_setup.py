import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schooltransport.setting')
django.setup()

from django.contrib.auth.models import User
from schooltransport.models import UserProfile

# Check existing users
drivers = User.objects.filter(profile__user_type='driver')
attendants = User.objects.filter(profile__user_type='attendant')
guardians = User.objects.filter(profile__user_type='guardian')

print(f'\nDrivers: {drivers.count()}')
for driver in drivers:
    print(f'  - {driver.get_full_name()} ({driver.username})')

print(f'\nAttendants: {attendants.count()}')
for attendant in attendants:
    print(f'  - {attendant.get_full_name()} ({attendant.username})')

print(f'\nGuardians: {guardians.count()}')
for guardian in guardians:
    print(f'  - {guardian.get_full_name()} ({guardian.username})')
