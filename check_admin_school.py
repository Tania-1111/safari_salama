import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schooltransport.setting')
django.setup()

from django.contrib.auth.models import User
from schooltransport.models import School, UserProfile

# Find admin user
admin_users = User.objects.filter(profile__user_type='admin')
print(f'Admin users: {admin_users.count()}')

for admin in admin_users:
    print(f'\nAdmin: {admin.get_full_name()} ({admin.username})')
    try:
        school = School.objects.get(admin=admin)
        print(f'  School: {school.name}')
    except School.DoesNotExist:
        print(f'  ❌ No school found for this admin!')
