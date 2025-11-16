#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schooltransport.setting')
django.setup()

from django.contrib.auth.models import User
from schooltransport.models import UserProfile

print("\n" + "="*60)
print("DATABASE USERS CHECK")
print("="*60)

# Check Drivers
print("\n🚗 DRIVERS:")
drivers = User.objects.filter(profile__user_type='driver')
if drivers.exists():
    for driver in drivers:
        print(f"  ✓ {driver.get_full_name()} (username: {driver.username}, email: {driver.email})")
else:
    print("  ✗ No drivers found in database")

# Check Attendants
print("\n📋 ATTENDANTS:")
attendants = User.objects.filter(profile__user_type='attendant')
if attendants.exists():
    for attendant in attendants:
        print(f"  ✓ {attendant.get_full_name()} (username: {attendant.username}, email: {attendant.email})")
else:
    print("  ✗ No attendants found in database")

# Check Guardians
print("\n👨‍👩‍👧 GUARDIANS:")
guardians = User.objects.filter(profile__user_type='guardian')
if guardians.exists():
    for guardian in guardians:
        print(f"  ✓ {guardian.get_full_name()} (username: {guardian.username}, email: {guardian.email})")
else:
    print("  ✗ No guardians found in database")

# Summary
print("\n" + "="*60)
print("SUMMARY:")
print(f"  Total Drivers: {drivers.count()}")
print(f"  Total Attendants: {attendants.count()}")
print(f"  Total Guardians: {guardians.count()}")
print(f"  Total Users: {User.objects.count()}")
print("="*60 + "\n")
