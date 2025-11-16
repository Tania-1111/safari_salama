#!/usr/bin/env python
"""
Quick Start Script for Safari Salama
Run this to set up the project quickly
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schooltransport.setting')
django.setup()

from django.contrib.auth.models import User
from schooltransport.models import UserProfile, School, Bus, Student, Route, RouteStop
from django.utils import timezone

def create_demo_data():
    """Create sample data for testing"""
    
    print("Creating demo data...")
    
    # 1. Create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@safarisalama.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("✓ Created admin user")
    
    # 2. Create admin profile
    admin_profile, created = UserProfile.objects.get_or_create(
        user=admin_user,
        defaults={
            'user_type': 'admin',
            'phone_number': '+254712345678',
            'verified': True,
        }
    )
    
    # 3. Create school
    school, created = School.objects.get_or_create(
        admin=admin_user,
        defaults={
            'name': 'Nairobi Academy',
            'location': 'Westlands, Nairobi',
            'latitude': -1.2865,
            'longitude': 36.8172,
            'phone_number': '+254712345678',
            'email': 'info@nairobiaca.ac.ke',
            'registration_number': 'SCHOOL/001/2024',
        }
    )
    if created:
        print("✓ Created school")
    
    # 4. Create driver
    driver_user, created = User.objects.get_or_create(
        username='driver1',
        defaults={
            'email': 'driver@safarisalama.com',
            'first_name': 'John',
            'last_name': 'Driver',
        }
    )
    if created:
        driver_user.set_password('driver123')
        driver_user.save()
        print("✓ Created driver user")
    
    driver_profile, created = UserProfile.objects.get_or_create(
        user=driver_user,
        defaults={
            'user_type': 'driver',
            'phone_number': '+254712345679',
            'verified': True,
        }
    )
    
    # 5. Create bus
    bus, created = Bus.objects.get_or_create(
        school=school,
        registration_number='KCA-123A',
        defaults={
            'driver': driver_user,
            'capacity': 50,
            'current_latitude': -1.2865,
            'current_longitude': 36.8172,
            'status': 'active',
        }
    )
    if created:
        print("✓ Created bus")
    
    # 6. Create guardian
    guardian_user, created = User.objects.get_or_create(
        username='guardian1',
        defaults={
            'email': 'guardian@safarisalama.com',
            'first_name': 'Mary',
            'last_name': 'Guardian',
        }
    )
    if created:
        guardian_user.set_password('guardian123')
        guardian_user.save()
        print("✓ Created guardian user")
    
    guardian_profile, created = UserProfile.objects.get_or_create(
        user=guardian_user,
        defaults={
            'user_type': 'guardian',
            'phone_number': '+254712345680',
            'verified': True,
        }
    )
    
    # 7. Create student
    student_user, created = User.objects.get_or_create(
        username='student1',
        defaults={
            'email': 'student@safarisalama.com',
            'first_name': 'David',
            'last_name': 'Student',
        }
    )
    if created:
        student_user.set_password('student123')
        student_user.save()
        print("✓ Created student user")
    
    student_profile, created = UserProfile.objects.get_or_create(
        user=student_user,
        defaults={
            'user_type': 'student',
            'phone_number': '+254712345681',
            'verified': True,
        }
    )
    
    # 8. Create student record
    from datetime import datetime, date
    student, created = Student.objects.get_or_create(
        user=student_user,
        school=school,
        defaults={
            'registration_number': 'STU/2024/001',
            'date_of_birth': date(2010, 5, 15),
            'class_name': 'Form 1A',
            'guardian': guardian_user,
            'bus': bus,
            'parent_phone': '+254712345680',
            'biometric_enrolled': False,
        }
    )
    if created:
        print("✓ Created student record")
    
    # 9. Create route
    route, created = Route.objects.get_or_create(
        school=school,
        bus=bus,
        defaults={
            'name': 'Westlands to School',
            'description': 'Main route from Westlands to school',
            'start_location': 'Westlands, Nairobi',
            'end_location': 'Nairobi Academy',
            'estimated_duration': 30,
            'is_active': True,
        }
    )
    if created:
        print("✓ Created route")
    
    # 10. Create route stops
    stops = [
        {
            'name': 'Westlands Bus Stop',
            'latitude': -1.2680,
            'longitude': 36.7900,
            'order': 1,
            'estimated_arrival_time': 0,
        },
        {
            'name': 'Kilimani Pickup',
            'latitude': -1.2800,
            'longitude': 36.7950,
            'order': 2,
            'estimated_arrival_time': 5,
        },
        {
            'name': 'Parklands Stop',
            'latitude': -1.2850,
            'longitude': 36.8050,
            'order': 3,
            'estimated_arrival_time': 10,
        },
        {
            'name': 'Nairobi Academy',
            'latitude': -1.2865,
            'longitude': 36.8172,
            'order': 4,
            'estimated_arrival_time': 30,
        },
    ]
    
    for stop_data in stops:
        stop, created = RouteStop.objects.get_or_create(
            route=route,
            name=stop_data['name'],
            defaults={
                'latitude': stop_data['latitude'],
                'longitude': stop_data['longitude'],
                'order': stop_data['order'],
                'estimated_arrival_time': stop_data['estimated_arrival_time'],
            }
        )
    
    print("✓ Created route stops")
    
    print("\n✅ Demo data created successfully!")
    print("\nTest Credentials:")
    print("=" * 50)
    print("Admin:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nDriver:")
    print("  Username: driver1")
    print("  Password: driver123")
    print("  Bus: KCA-123A")
    print("\nGuardian:")
    print("  Username: guardian1")
    print("  Password: guardian123")
    print("  Student: David Student (Form 1A)")
    print("\nStudent:")
    print("  Username: student1")
    print("  Password: student123")
    print("=" * 50)

if __name__ == '__main__':
    try:
        create_demo_data()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
