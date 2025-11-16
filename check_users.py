#!/usr/bin/env python
"""Check users in database by role"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schooltransport.setting')
django.setup()

from django.contrib.auth.models import User
from schooltransport.models import UserProfile

print('\n' + '='*60)
print('DATABASE USER INVENTORY')
print('='*60)

print('\n📊 TOTAL USERS:', User.objects.count())

print('\n' + '-'*60)
print('👤 ALL USERS:')
print('-'*60)
for user in User.objects.all().order_by('username'):
    try:
        profile = user.profile
        role = profile.user_type
    except:
        role = 'NO PROFILE'
    print(f'  {user.username:15} | {user.get_full_name():25} | Role: {role}')

print('\n' + '-'*60)
print('🚗 DRIVERS:')
print('-'*60)
drivers = User.objects.filter(profile__user_type='driver')
print(f'Count: {drivers.count()}')
if drivers.count() == 0:
    print('  ❌ No drivers found!')
else:
    for d in drivers:
        print(f'  ✓ {d.id:3} | {d.get_full_name():25} ({d.username})')

print('\n' + '-'*60)
print('📋 ATTENDANTS:')
print('-'*60)
attendants = User.objects.filter(profile__user_type='attendant')
print(f'Count: {attendants.count()}')
if attendants.count() == 0:
    print('  ❌ No attendants found!')
else:
    for a in attendants:
        print(f'  ✓ {a.id:3} | {a.get_full_name():25} ({a.username})')

print('\n' + '-'*60)
print('👨‍👩‍👧 GUARDIANS:')
print('-'*60)
guardians = User.objects.filter(profile__user_type='guardian')
print(f'Count: {guardians.count()}')
if guardians.count() == 0:
    print('  ❌ No guardians found!')
else:
    for g in guardians:
        print(f'  ✓ {g.id:3} | {g.get_full_name():25} ({g.username})')

print('\n' + '-'*60)
print('🎓 STUDENTS:')
print('-'*60)
students = User.objects.filter(profile__user_type='student')
print(f'Count: {students.count()}')
if students.count() == 0:
    print('  ❌ No students found!')
else:
    for s in students:
        print(f'  ✓ {s.id:3} | {s.get_full_name():25} ({s.username})')

print('\n' + '-'*60)
print('👨‍💼 ADMINS:')
print('-'*60)
admins = User.objects.filter(profile__user_type='admin')
print(f'Count: {admins.count()}')
if admins.count() == 0:
    print('  ❌ No admins found!')
else:
    for ad in admins:
        print(f'  ✓ {ad.id:3} | {ad.get_full_name():25} ({ad.username})')

print('\n' + '='*60 + '\n')
