import os
import sys

# Ensure project root is on path
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schooltransport.setting')

try:
    import django
    django.setup()
except Exception as e:
    print('Failed to setup Django:', e)
    raise

from django.contrib.auth.models import User
from schooltransport.models import UserProfile

def ensure_role(username, expected_role):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print(f"User '{username}' does not exist")
        return

    profile, created = UserProfile.objects.get_or_create(user=user)
    if not profile.user_type:
        profile.user_type = expected_role
        profile.save()
        print(f"Set role for {username} -> {expected_role} (was blank)")
    elif profile.user_type != expected_role:
        print(f"User {username} has role '{profile.user_type}' (expected '{expected_role}')")
    else:
        print(f"User {username} already has role '{expected_role}'")

def main():
    mapping = {
        'admin1': 'admin',
        'driver1': 'driver',
        'attendant1': 'attendant',
        'guardian1': 'guardian'
    }

    print('Checking demo users and roles...')
    for u, r in mapping.items():
        ensure_role(u, r)

    print('Done.')

if __name__ == '__main__':
    main()
