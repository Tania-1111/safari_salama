from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils import timezone
import json
import requests
from datetime import timedelta

from .models import (
    UserProfile, School, Bus, Student, StudentAttendance,
    BusLocation, Notification, Route, RouteStop
)
from .serializers import (
    UserProfileSerializer, BusSerializer, StudentSerializer,
    BusLocationSerializer, NotificationSerializer
)


def home(request):
    """Root entry: redirect users to their role landing or to login."""
    if not request.user.is_authenticated:
        return redirect('login')

    # Try to detect user role via profile (user.profile.user_type)
    try:
        role = request.user.profile.user_type
    except Exception:
        role = None

    if role == 'driver':
        return redirect('driver_landing')
    if role == 'guardian':
        return redirect('guardian_landing')
    if role == 'attendant':
        return redirect('attendant_landing')
    if role == 'admin':
        return redirect('admin_landing')

    # default
    return redirect('login')


# ==================== AUTHENTICATION VIEWS ====================

def register(request):
    """Register new users (Guardian, Driver, Attendant, Admin)"""
    if request.method == 'POST':
        from django.contrib import messages
        
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()
        role = request.POST.get('role', '').strip()
        
        # Validation
        if not all([first_name, last_name, username, email, password, role]):
            messages.error(request, 'All fields are required!')
            return redirect('login')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match!')
            return redirect('login')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters!')
            return redirect('login')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('login')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('login')
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create user profile
            profile = UserProfile.objects.create(
                user=user,
                user_type=role
            )
            
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return redirect('login')
    
    return render(request, 'login.html')


def login_view(request):
    """Login users"""
    from django.contrib import messages
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not username or not password:
            messages.error(request, 'Username and password are required!')
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('login')
    
    return render(request, 'login.html')


def logout_view(request):
    """Logout user"""
    logout(request)
    return redirect('login')


# ==================== GUARDIAN VIEWS ====================

@login_required
def guardian_dashboard(request):
    """Guardian dashboard showing their students and bus tracking"""
    guardian = request.user
    students = Student.objects.filter(guardian=guardian)
    
    context = {
        'students': students,
        'buses': [student.bus for student in students if student.bus]
    }
    return render(request, 'guardian/dashboard.html', context)


@login_required
def guardian_landing(request):
    """Landing page for guardians (profile, students, trip history)"""
    guardian = request.user
    students = Student.objects.filter(guardian=guardian)
    context = {
        'user': guardian,
        'students': students,
    }
    return render(request, 'guardian/landing.html', context)


@login_required
def student_status(request, student_id):
    """Get real-time status of a student's bus with GUI"""
    student = get_object_or_404(Student, id=student_id, guardian=request.user)
    
    if not student.bus:
        return render(request, 'guardian/student_status.html', {
            'student': student,
            'error': 'No bus assigned',
            'status': 'NOT_ASSIGNED'
        })
    
    bus = student.bus
    today = timezone.now().date()
    
    # Get today's attendance record (from fingerprint device)
    try:
        attendance_today = StudentAttendance.objects.filter(
            student=student,
            bus=bus,
            date=today
        ).latest('timestamp')
        status = attendance_today.status  # 'boarded' or 'alighted'
        boarded_time = attendance_today.timestamp
        biometric_verified = attendance_today.biometric_verified
        biometric_confidence = attendance_today.biometric_confidence
    except Exception:
        status = 'absent'
        boarded_time = None
        biometric_verified = False
        biometric_confidence = 0.0
    
    # Get latest bus location
    try:
        latest_location = bus.location_history.latest('timestamp')
        current_location = {
            'latitude': latest_location.latitude,
            'longitude': latest_location.longitude,
            'timestamp': latest_location.timestamp
        }
    except Exception:
        current_location = None
    
    # Get bus route info - safely without querying the database
    route = None
    route_name = "Not assigned"
    
    context = {
        'student': student,
        'bus': bus,
        'status': status.upper() if status else 'ABSENT',
        'boarded_time': boarded_time,
        'biometric_verified': biometric_verified,
        'biometric_confidence': biometric_confidence,
        'current_location': current_location,
        'route': route,
        'route_name': route_name,
        'today': today
    }
    
    return render(request, 'guardian/student_status.html', context)


# ==================== DRIVER VIEWS ====================

@login_required
def driver_dashboard(request):
    """Driver dashboard"""
    driver = request.user
    bus = get_object_or_404(Bus, driver=driver)
    
    context = {
        'bus': bus,
        'students': bus.students.all(),
        'route': bus.routes.first(),
        'google_maps_api_key': 'YOUR_GOOGLE_MAPS_API_KEY'
    }
    return render(request, 'driver/dashboard.html', context)


@login_required
def driver_landing(request):
    """Landing page for drivers (profile, start trip, students list, trip history)"""
    driver = request.user
    bus = Bus.objects.filter(driver=driver).first()
    students = bus.students.all() if bus else []
    context = {
        'user': driver,
        'bus': bus,
        'students': students,
        'google_maps_api_key': 'YOUR_GOOGLE_MAPS_API_KEY'
    }
    return render(request, 'driver/landing.html', context)


@login_required
def attendant_landing(request):
    """Landing page for attendants (bus, students, attendance tracking)"""
    attendant = request.user
    bus = Bus.objects.filter(attendant=attendant).first()
    students = bus.students.all() if bus else []
    context = {
        'user': attendant,
        'bus': bus,
        'students': students,
    }
    return render(request, 'attendant/landing.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def update_bus_location(request):
    """
    Receive GPS coordinates from driver's device
    Expected JSON: {
        "bus_id": 1,
        "latitude": 1.2345,
        "longitude": 36.7890,
        "accuracy": 5.0,
        "speed": 45.5,
        "heading": 180.0
    }
    """
    try:
        data = json.loads(request.body)
        bus = Bus.objects.get(id=data['bus_id'])
        
        # Create location history record
        location = BusLocation.objects.create(
            bus=bus,
            latitude=data['latitude'],
            longitude=data['longitude'],
            accuracy=data.get('accuracy'),
            speed=data.get('speed'),
            heading=data.get('heading')
        )
        
        # Update bus current location
        bus.current_latitude = data['latitude']
        bus.current_longitude = data['longitude']
        bus.save()
        
        return JsonResponse({
            'message': 'Location updated successfully',
            'location_id': location.id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def get_bus_route(request, bus_id):
    """Get the current bus route with all stops"""
    bus = get_object_or_404(Bus, id=bus_id, driver=request.user)
    route = bus.routes.filter(is_active=True).first()
    
    if not route:
        return JsonResponse({'error': 'No active route'}, status=404)
    
    stops = route.stops.all()
    
    return JsonResponse({
        'route': {
            'id': route.id,
            'name': route.name,
            'start': route.start_location,
            'end': route.end_location,
            'estimated_duration': route.estimated_duration
        },
        'stops': [
            {
                'id': stop.id,
                'name': stop.name,
                'latitude': stop.latitude,
                'longitude': stop.longitude,
                'order': stop.order,
                'estimated_arrival_time': stop.estimated_arrival_time
            }
            for stop in stops
        ]
    })


# ==================== BIOMETRIC & ATTENDANCE VIEWS ====================

@csrf_exempt
@require_http_methods(["POST"])
def enroll_biometric(request):
    """
    Enroll student biometric data
    Expected JSON: {
        "student_id": 1,
        "biometric_data": "base64_encoded_data",
        "biometric_type": "fingerprint"
    }
    """
    try:
        data = json.loads(request.body)
        student = Student.objects.get(id=data['student_id'])
        
        # Store biometric template (in production, use a proper biometric library)
        student.biometric_template = {'data': data['biometric_data']}
        student.biometric_type = data['biometric_type']
        student.biometric_enrolled = True
        student.save()
        
        return JsonResponse({
            'message': 'Biometric enrolled successfully',
            'student_id': student.id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def verify_and_checkin(request):
    """
    Verify biometric and record student attendance (boarding)
    Expected JSON: {
        "student_biometric": "base64_encoded_data",
        "bus_id": 1,
        "location_latitude": 1.2345,
        "location_longitude": 36.7890
    }
    """
    try:
        data = json.loads(request.body)
        
        # Find student by biometric (simplified - in production use ML matching)
        bus = Bus.objects.get(id=data['bus_id'])
        
        # This is a simplified matching - use a proper biometric library
        biometric_confidence = 95.0  # Placeholder
        
        # Find matching student
        students = bus.students.filter(biometric_enrolled=True)
        matched_student = None
        
        for student in students:
            # In production, use actual biometric matching algorithm
            # For now, assume we matched based on the biometric data
            matched_student = student
            break
        
        if not matched_student:
            return JsonResponse({'error': 'Student not recognized'}, status=404)
        
        # Create attendance record
        attendance = StudentAttendance.objects.create(
            student=matched_student,
            bus=bus,
            status='boarded',
            latitude=data.get('location_latitude'),
            longitude=data.get('location_longitude'),
            biometric_verified=True,
            biometric_confidence=biometric_confidence
        )
        
        # Send notification to guardian
        send_notification_to_guardian(
            matched_student,
            f"{matched_student.user.get_full_name()} has boarded bus {bus.registration_number}",
            'boarded'
        )
        
        return JsonResponse({
            'message': 'Student checked in successfully',
            'student_id': matched_student.id,
            'student_name': matched_student.user.get_full_name(),
            'confidence': biometric_confidence
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def verify_and_checkout(request):
    """
    Verify biometric and record student alighting
    Expected JSON: {
        "student_biometric": "base64_encoded_data",
        "bus_id": 1,
        "location_latitude": 1.2345,
        "location_longitude": 36.7890
    }
    """
    try:
        data = json.loads(request.body)
        bus = Bus.objects.get(id=data['bus_id'])
        
        # Find matching student (simplified)
        matched_student = None
        for student in bus.students.filter(biometric_enrolled=True):
            # Check if student has an active boarded status
            if student.attendance_logs.filter(status='boarded').exists():
                matched_student = student
                break
        
        if not matched_student:
            return JsonResponse({'error': 'Student not found'}, status=404)
        
        # Create attendance record for alighting
        attendance = StudentAttendance.objects.create(
            student=matched_student,
            bus=bus,
            status='alighted',
            latitude=data.get('location_latitude'),
            longitude=data.get('location_longitude'),
            biometric_verified=True,
            biometric_confidence=95.0
        )
        
        # Send notification to guardian
        send_notification_to_guardian(
            matched_student,
            f"{matched_student.user.get_full_name()} has alighted from bus {bus.registration_number}",
            'alighted'
        )
        
        return JsonResponse({
            'message': 'Student checked out successfully',
            'student_id': matched_student.id,
            'student_name': matched_student.user.get_full_name()
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ==================== NOTIFICATION VIEWS ====================

def send_notification_to_guardian(student, message, notification_type):
    """
    Send notification to student's guardian
    Supports: Email, SMS (via Twilio), and Push Notifications (via Firebase)
    """
    guardian = student.guardian
    
    if not guardian:
        return
    
    # Create notification in database
    notification = Notification.objects.create(
        recipient=guardian,
        student=student,
        title=f"Student Transportation Alert",
        message=message,
        notification_type=notification_type
    )
    
    # Send email
    send_email_notification(guardian, message)
    
    # Send SMS (optional)
    if guardian.profile.phone_number:
        send_sms_notification(guardian.profile.phone_number, message)
    
    # Send push notification if FCM token exists
    if notification.fcm_token:
        send_push_notification(notification.fcm_token, message)


def send_email_notification(user, message):
    """Send email notification"""
    from django.core.mail import send_mail
    
    try:
        send_mail(
            'Student Transportation Alert',
            message,
            'noreply@safarisalama.com',
            [user.email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Email notification error: {e}")


def send_sms_notification(phone_number, message):
    """
    Send SMS notification using Twilio
    Install: pip install twilio
    """
    try:
        from twilio.rest import Client
        
        # Get Twilio credentials from environment
        account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
        auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
        twilio_phone = 'YOUR_TWILIO_PHONE_NUMBER'
        
        client = Client(account_sid, auth_token)
        message_obj = client.messages.create(
            body=message[:160],  # SMS limit
            from_=twilio_phone,
            to=phone_number
        )
    except Exception as e:
        print(f"SMS notification error: {e}")


def send_push_notification(fcm_token, message):
    """
    Send push notification using Firebase Cloud Messaging
    Install: pip install firebase-admin
    """
    try:
        import firebase_admin
        from firebase_admin import messaging
        
        message_obj = messaging.Message(
            notification=messaging.Notification(
                title='Student Transportation',
                body=message
            ),
            token=fcm_token,
        )
        
        response = messaging.send(message_obj)
    except Exception as e:
        print(f"Push notification error: {e}")


@login_required
def get_notifications(request):
    """Get user's notifications"""
    notifications = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).order_by('-created_at')[:10]
    
    serializer = NotificationSerializer(notifications, many=True)
    return JsonResponse({'notifications': serializer.data})


@login_required
def mark_notification_read(request, notification_id):
    """Mark notification as read"""
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient=request.user
    )
    
    notification.is_read = True
    notification.read_at = timezone.now()
    notification.save()
    
    return JsonResponse({'message': 'Notification marked as read'})


# ==================== ADMIN VIEWS ====================

@login_required
def admin_dashboard(request):
    """School admin dashboard"""
    if request.user.profile.user_type != 'admin':
        return redirect('login')
    
    school = School.objects.get(admin=request.user)
    
    context = {
        'school': school,
        'total_students': school.students.count(),
        'total_buses': school.buses.count(),
        'total_drivers': school.buses.values('driver').distinct().count(),
        'today_attendance': StudentAttendance.objects.filter(
            student__school=school,
            date=timezone.now().date()
        ).count()
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
def driver_trip_history(request):
    """Driver trip history (shows StudentAttendance entries for the driver's bus)"""
    driver = request.user
    bus = Bus.objects.filter(driver=driver).first()
    if not bus:
        return render(request, 'driver/trip_history.html', {'trips': []})

    trips = StudentAttendance.objects.filter(bus=bus).select_related('student').order_by('-timestamp')[:100]
    return render(request, 'driver/trip_history.html', {'trips': trips, 'bus': bus})


@login_required
def guardian_trip_history(request):
    """Guardian trip history (shows StudentAttendance entries for guardian's students)"""
    guardian = request.user
    students = Student.objects.filter(guardian=guardian)
    trips = StudentAttendance.objects.filter(student__in=students).select_related('student', 'bus').order_by('-timestamp')[:100]
    return render(request, 'guardian/trip_history.html', {'trips': trips})


@login_required
def manage_students(request):
    """Manage students (admin only)"""
    if request.user.profile.user_type != 'admin':
        return redirect('login')
    
    school = School.objects.get(admin=request.user)
    students = school.students.all()
    guardians = User.objects.filter(profile__user_type='guardian')
    buses = school.buses.all()
    
    if request.method == 'POST':
        # Handle adding new student
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        enrollment_number = request.POST.get('enrollment_number', '').strip()
        class_name = request.POST.get('class_name', '').strip()
        guardian_id = request.POST.get('guardian_id')
        bus_id = request.POST.get('bus_id')
        dob = request.POST.get('dob')
        
        if all([first_name, last_name, enrollment_number, class_name]):
            try:
                # Create user account
                username = enrollment_number.lower()
                user = User.objects.create_user(
                    username=username,
                    email=f"{username}@safarisal ama.local",
                    first_name=first_name,
                    last_name=last_name,
                    password='student123'  # Default password
                )
                
                # Create student record
                student = Student.objects.create(
                    user=user,
                    school=school,
                    registration_number=enrollment_number,
                    class_name=class_name,
                    date_of_birth=dob if dob else None,
                    bus_id=bus_id if bus_id else None
                )
                
                # Link guardian if provided
                if guardian_id:
                    guardian = User.objects.get(id=guardian_id)
                    student.guardian = guardian
                    student.save()
                
                from django.contrib import messages
                messages.success(request, f'Student {first_name} {last_name} added successfully!')
                return redirect('manage_students')
            except Exception as e:
                from django.contrib import messages
                messages.error(request, f'Error adding student: {str(e)}')
    
    context = {
        'students': students,
        'guardians': guardians,
        'buses': buses,
        'school': school
    }
    return render(request, 'admin/manage_students.html', context)


@login_required
def manage_buses(request):
    """Manage buses (admin only)"""
    if request.user.profile.user_type != 'admin':
        return redirect('login')
    
    school = School.objects.get(admin=request.user)
    buses = school.buses.all()
    # Only show drivers and attendants not yet assigned to a bus
    drivers = User.objects.filter(profile__user_type='driver')
    attendants = User.objects.filter(profile__user_type='attendant')
    routes = Route.objects.filter(school=school)
    
    if request.method == 'POST':
        # Handle adding new bus
        registration_number = request.POST.get('registration_number', '').strip().upper()
        capacity = request.POST.get('capacity', '50')
        driver_id = request.POST.get('driver_id')
        attendant_id = request.POST.get('attendant_id')
        route_id = request.POST.get('route_id')
        
        if registration_number and capacity:
            try:
                # Create or update bus
                bus, created = Bus.objects.get_or_create(
                    registration_number=registration_number,
                    defaults={
                        'school': school,
                        'capacity': int(capacity),
                    }
                )
                
                # Assign driver if selected
                if driver_id:
                    driver = User.objects.get(id=driver_id)
                    bus.driver = driver
                
                # Assign attendant if selected
                if attendant_id:
                    attendant = User.objects.get(id=attendant_id)
                    bus.attendant = attendant
                
                bus.capacity = int(capacity)
                bus.save()
                
                # Assign route if selected
                if route_id:
                    route = Route.objects.get(id=route_id, school=school)
                    route.bus = bus
                    route.save()
                
                from django.contrib import messages
                if created:
                    messages.success(request, f'Bus {registration_number} registered successfully with driver and attendant!')
                else:
                    messages.success(request, f'Bus {registration_number} updated successfully!')
                return redirect('manage_buses')
            except Exception as e:
                from django.contrib import messages
                messages.error(request, f'Error adding bus: {str(e)}')
    
    context = {
        'buses': buses,
        'drivers': drivers,
        'attendants': attendants,
        'routes': routes,
        'school': school
    }
    return render(request, 'admin/manage_buses.html', context)


@login_required
def manage_users(request):
    """Manage user accounts (admin only)"""
    if request.user.profile.user_type != 'admin':
        return redirect('login')
    
    school = School.objects.get(admin=request.user)
    drivers = User.objects.filter(profile__user_type='driver')
    attendants = User.objects.filter(profile__user_type='attendant')
    guardians = User.objects.filter(profile__user_type='guardian')
    
    if request.method == 'POST':
        # Handle adding new user
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        role = request.POST.get('role', 'guardian')  # driver, attendant, guardian
        password = request.POST.get('password', 'password123')
        
        if all([first_name, last_name, email, username]):
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                from .models import UserProfile, Driver, Attendant, Guardian
                
                # Create UserProfile for tracking user type
                profile, _ = UserProfile.objects.get_or_create(user=user)
                profile.user_type = role
                profile.save()
                
                # Create role-specific profile based on role selected
                if role == 'driver':
                    Driver.objects.get_or_create(user=user, school=school)
                elif role == 'attendant':
                    Attendant.objects.get_or_create(user=user, school=school)
                elif role == 'guardian':
                    Guardian.objects.get_or_create(user=user, school=school)
                
                from django.contrib import messages
                messages.success(request, f'{role.title()} {first_name} {last_name} created successfully!')
                return redirect('manage_users')
            except Exception as e:
                from django.contrib import messages
                messages.error(request, f'Error creating user: {str(e)}')
    
    context = {
        'drivers': drivers,
        'attendants': attendants,
        'guardians': guardians,
        'school': school
    }
    return render(request, 'admin/manage_users.html', context)


    return render(request, 'admin/manage_students.html', {'students': students})


@login_required


@login_required
def view_attendance_reports(request):
    """View attendance reports (admin only)"""
    if request.user.profile.user_type != 'admin':
        return redirect('login')
    
    school = School.objects.get(admin=request.user)
    date = request.GET.get('date', timezone.now().date())
    
    attendance = StudentAttendance.objects.filter(
        student__school=school,
        date=date
    ).select_related('student', 'bus')
    
    return render(request, 'admin/attendance_reports.html', {'attendance': attendance})


# ==================== BIOMETRIC VIEWS ====================

def simulate_fingerprint_match(captured, stored):
    """Simulate fingerprint matching with confidence score"""
    if not stored or not captured:
        return 0.0
    
    matches = sum(1 for a, b in zip(str(captured), str(stored)) if a == b)
    max_len = max(len(str(captured)), len(str(stored)))
    similarity = (matches / max_len) * 100 if max_len > 0 else 0
    return min(similarity, 100)


@csrf_exempt
@require_http_methods(["POST"])
def enroll_fingerprint(request):
    """Enroll a student's fingerprint"""
    try:
        data = json.loads(request.body)
        student_id = data.get('student_id')
        fingerprint_data = data.get('fingerprint_data')
        
        student = Student.objects.get(id=student_id)
        
        from .models import BiometricEnrollment
        biometric, created = BiometricEnrollment.objects.get_or_create(student=student)
        biometric.fingerprint_template = fingerprint_data.encode() if isinstance(fingerprint_data, str) else fingerprint_data
        biometric.is_verified = True
        biometric.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Fingerprint enrolled for {student.user.get_full_name()}',
            'student_id': student_id
        })
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def verify_fingerprint(request):
    """Verify fingerprint and mark student attendance"""
    try:
        data = json.loads(request.body)
        fingerprint_data = data.get('fingerprint_data')
        action = data.get('action', 'checkin')
        bus_id = data.get('bus_id', 1)
        
        from .models import BiometricEnrollment, BiometricLog
        
        biometrics = BiometricEnrollment.objects.filter(is_verified=True)
        matched_student = None
        match_score = 0.0
        
        for biometric in biometrics:
            stored_template = biometric.fingerprint_template.decode() if biometric.fingerprint_template else ""
            similarity = simulate_fingerprint_match(fingerprint_data, stored_template)
            
            if similarity > 85:
                matched_student = biometric.student
                match_score = similarity
                break
        
        if not matched_student:
            return JsonResponse({
                'success': False,
                'error': 'Fingerprint not recognized. Please try again.',
                'action': action
            }, status=401)
        
        # Log biometric scan
        BiometricLog.objects.create(
            student=matched_student,
            match_score=match_score,
            status='match',
            location=f'Bus {bus_id}',
            scan_type=action
        )
        
        # Create/update attendance
        today = timezone.now().date()
        attendance, created = StudentAttendance.objects.get_or_create(
            student=matched_student,
            date=today,
            bus_id=bus_id
        )
        
        if action == 'checkin':
            attendance.boarded = True
            message = f'{matched_student.user.get_full_name()} boarded successfully'
        else:
            attendance.alighted = True
            message = f'{matched_student.user.get_full_name()} alighted successfully'
        
        attendance.save()
        
        return JsonResponse({
            'success': True,
            'message': message,
            'student_name': matched_student.user.get_full_name(),
            'student_id': matched_student.id,
            'match_score': match_score,
            'action': action
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["GET"])
def fingerprint_scanner(request):
    """Display fingerprint scanner interface"""
    bus_id = request.GET.get('bus_id', 1)
    
    from .models import BiometricEnrollment
    enrolled_students = Student.objects.filter(biometric_enrollment__is_verified=True)
    
    context = {
        'bus_id': bus_id,
        'enrolled_students': enrolled_students,
        'page_title': 'Fingerprint Scanner'
    }
    return render(request, 'fingerprint_scanner.html', context)


# ==================== MESSAGING VIEWS ====================

@login_required
@require_http_methods(["POST"])
def send_message(request):
    """Send a message from guardian to attendant"""
    try:
        data = json.loads(request.body)
        recipient_id = data.get('recipient_id')
        message_text = data.get('message_text', '').strip()
        bus_id = data.get('bus_id')
        
        if not message_text:
            return JsonResponse({'success': False, 'error': 'Message cannot be empty'}, status=400)
        
        if not recipient_id:
            return JsonResponse({'success': False, 'error': 'Recipient not specified'}, status=400)
        
        try:
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Recipient not found'}, status=404)
        
        # Create message
        from .models import Message
        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            message_text=message_text,
            bus_id=bus_id
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Message sent successfully',
            'message_id': message.id
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_http_methods(["GET"])
def get_messages(request):
    """Get conversation with a specific user"""
    try:
        recipient_id = request.GET.get('recipient_id')
        
        if not recipient_id:
            return JsonResponse({'success': False, 'error': 'Recipient not specified'}, status=400)
        
        from .models import Message
        
        # Get all messages between current user and recipient
        messages = Message.objects.filter(
            Q(sender=request.user, recipient_id=recipient_id) |
            Q(sender_id=recipient_id, recipient=request.user)
        ).order_by('timestamp')
        
        # Mark received messages as read
        unread_messages = messages.filter(recipient=request.user, is_read=False)
        unread_messages.update(is_read=True, read_at=timezone.now())
        
        # Serialize messages
        message_list = []
        for msg in messages:
            message_list.append({
                'id': msg.id,
                'sender_id': msg.sender.id,
                'sender_name': msg.sender.get_full_name(),
                'recipient_id': msg.recipient.id,
                'message_text': msg.message_text,
                'timestamp': msg.timestamp.isoformat(),
                'is_read': msg.is_read
            })
        
        return JsonResponse({
            'success': True,
            'messages': message_list
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_http_methods(["GET"])
def get_bus_attendant(request, bus_id):
    """Get attendant information for a bus"""
    try:
        bus = Bus.objects.get(id=bus_id)
        
        if not bus.attendant:
            return JsonResponse({
                'success': False,
                'error': 'No attendant assigned to this bus'
            }, status=404)
        
        return JsonResponse({
            'success': True,
            'attendant': {
                'id': bus.attendant.id,
                'name': bus.attendant.get_full_name(),
                'phone': bus.attendant.profile.phone_number if hasattr(bus.attendant, 'profile') else None
            }
        })
    
    except Bus.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Bus not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

