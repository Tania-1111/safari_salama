#!/usr/bin/env python
import os
import sys
import django

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schooltransport.setting')

try:
    django.setup()
except Exception as e:
    print(f'Failed to setup Django: {e}')
    raise

from schooltransport.models import Student, BiometricEnrollment

def enroll_demo_fingerprints():
    """Auto-enroll demo students with dummy fingerprints"""
    students = Student.objects.all()
    
    print(f'Enrolling fingerprints for {students.count()} students...')
    
    for i, student in enumerate(students, 1):
        # Generate dummy fingerprint data
        fingerprint_data = f'fp_demo_{student.id}_{student.user.username}'
        
        biometric, created = BiometricEnrollment.objects.get_or_create(
            student=student,
            defaults={
                'fingerprint_template': fingerprint_data.encode(),
                'is_verified': True
            }
        )
        
        if created:
            print(f'  ✅ Enrolled: {student.user.get_full_name()} (ID: {student.id})')
        else:
            print(f'  ℹ️  Already enrolled: {student.user.get_full_name()}')
    
    print('Done!')

if __name__ == '__main__':
    enroll_demo_fingerprints()
