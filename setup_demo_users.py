#!/usr/bin/env python
"""Create demo users and sample data for Safari Salama project."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schooltransport.setting')
django.setup()

from django.contrib.auth.models import User
from schooltransport.models import UserProfile, School, Bus, Student

# Admin user first (required for School)
admin, created = User.objects.get_or_create(username='admin1', defaults={'email': 'admin@test.com'})
if created:
    admin.set_password('admin123')
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    UserProfile.objects.get_or_create(user=admin, defaults={'user_type': 'admin'})

# Create or get school with admin
school, _ = School.objects.get_or_create(
    name='Demo School',
    defaults={
        'admin': admin,
        'location': 'Nairobi, Kenya',
        'latitude': -1.2921,
        'longitude': 36.8219,
        'phone_number': '0722123456',
        'email': 'school@demo.com',
        'registration_number': 'DEMO-001'
    }
)

# Driver
driver, created = User.objects.get_or_create(username='driver1', defaults={'email': 'driver@test.com'})
if created:
    driver.set_password('driver123')
    driver.save()
    UserProfile.objects.get_or_create(user=driver, defaults={'user_type': 'driver'})

# Attendant
attendant, created = User.objects.get_or_create(username='attendant1', defaults={'email': 'attendant@test.com'})
if created:
    attendant.set_password('attendant123')
    attendant.save()
    UserProfile.objects.get_or_create(user=attendant, defaults={'user_type': 'attendant'})

# Guardian
guardian, created = User.objects.get_or_create(username='guardian1', defaults={'email': 'guardian@test.com'})
if created:
    guardian.set_password('guardian123')
    guardian.save()
    UserProfile.objects.get_or_create(user=guardian, defaults={'user_type': 'guardian'})

# Admin
admin, created = User.objects.get_or_create(username='admin1', defaults={'email': 'admin@test.com'})
if created:
    admin.set_password('admin123')
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    UserProfile.objects.get_or_create(user=admin, defaults={'user_type': 'admin'})

# Driver
driver, created = User.objects.get_or_create(username='driver1', defaults={'email': 'driver@test.com'})
if created:
    driver.set_password('driver123')
    driver.save()
    UserProfile.objects.get_or_create(user=driver, defaults={'user_type': 'driver'})

# Attendant
attendant, created = User.objects.get_or_create(username='attendant1', defaults={'email': 'attendant@test.com'})
if created:
    attendant.set_password('attendant123')
    attendant.save()
    UserProfile.objects.get_or_create(user=attendant, defaults={'user_type': 'attendant'})

# Guardian
guardian, created = User.objects.get_or_create(username='guardian1', defaults={'email': 'guardian@test.com'})
if created:
    guardian.set_password('guardian123')
    guardian.save()
    UserProfile.objects.get_or_create(user=guardian, defaults={'user_type': 'guardian'})

# Create bus and assign driver
bus, _ = Bus.objects.get_or_create(registration_number='KAA-123', defaults={'school': school})
bus.driver = driver
bus.save()

# Create students and assign to guardian and bus
from datetime import date
for i in range(1,6):
    username = f'student{i}'
    user, created = User.objects.get_or_create(username=username, defaults={'email': f'{username}@test.com'})
    if created:
        user.set_password('student123')
        user.save()
    student_obj, _ = Student.objects.get_or_create(
        user=user,
        defaults={
            'class_name': '1A',
            'guardian': guardian,
            'bus': bus,
            'school': school,
            'date_of_birth': date(2010, 1, i),
            'registration_number': f'STU-{school.id:03d}-{i:03d}',
            'parent_phone': '0722123456',
            'biometric_type': 'fingerprint',
            'biometric_enrolled': False
        }
    )

print('Demo users and sample data created: admin1, driver1, attendant1, guardian1, student1..5')
