#!/usr/bin/env python
"""
ENROLL DEMO FINGERPRINTS FOR ALL STUDENTS
Creates mock fingerprint enrollments so students can check in
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schooltransport.setting')
django.setup()

from schooltransport.models import Student, BiometricEnrollment

print("\n" + "="*70)
print("ENROLLING DEMO FINGERPRINTS FOR ALL STUDENTS")
print("="*70)

students = Student.objects.all()

if not students.exists():
    print("✗ No students found in database")
    exit(1)

print(f"\nFound {students.count()} students. Creating fingerprint enrollments...\n")

for student in students:
    # Create or update biometric enrollment
    biometric, created = BiometricEnrollment.objects.get_or_create(
        student=student,
        defaults={
            'fingerprint_template': f'demo_fingerprint_{student.id}_{student.user.username}'.encode(),
            'is_verified': True,
            'attempts': 1
        }
    )
    
    status = "✓ Created" if created else "✓ Already exists"
    print(f"{status}: {student.user.get_full_name()}")
    print(f"         Fingerprint ID: {biometric.id}, Verified: {biometric.is_verified}")

print("\n" + "="*70)
print("✅ ALL STUDENTS ENROLLED WITH DEMO FINGERPRINTS")
print("="*70)
print("""
📋 SUMMARY:
   - All students now have fingerprint enrollments
   - Fingerprints are verified and ready for scanning
   - You can now use the fingerprint scanner to check in students

🧪 TO TEST:
   1. Go to http://localhost:8001/admin/landing/ (login as admin)
   2. Click "Manage Buses" and register a bus with a driver & attendant
   3. Go to http://localhost:8001/attendant/ (login as attendant1)
   4. Click "Fingerprint Scanner"
   5. Click "Check In" button
   6. Student should be recognized and checked in

""")
print("="*70 + "\n")
