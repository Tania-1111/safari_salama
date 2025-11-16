from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Root route - send users to appropriate landing or login
    path('', views.home, name='home'),
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    # compatibility URL used by Django's login_required default redirect
    path('accounts/login/', views.login_view, name='accounts_login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Guardian URLs
    path('guardian/dashboard/', views.guardian_dashboard, name='guardian_dashboard'),
    path('guardian/', views.guardian_landing, name='guardian_landing'),
    path('guardian/student/<int:student_id>/status/', views.student_status, name='student_status'),
    
    # Driver URLs
    path('driver/dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('driver/', views.driver_landing, name='driver_landing'),
    path('driver/trips/', views.driver_trip_history, name='driver_trips'),
    path('driver/location/update/', views.update_bus_location, name='update_bus_location'),
    path('driver/bus/<int:bus_id>/route/', views.get_bus_route, name='get_bus_route'),
    
    # Attendant URLs
    path('attendant/', views.attendant_landing, name='attendant_landing'),
    
    # Biometric & Attendance
    path('biometric/enroll/', views.enroll_fingerprint, name='enroll_fingerprint'),
    path('biometric/verify/', views.verify_fingerprint, name='verify_fingerprint'),
    path('biometric/scanner/', views.fingerprint_scanner, name='fingerprint_scanner'),
    path('attendance/checkin/', views.verify_and_checkin, name='verify_and_checkin'),
    path('attendance/checkout/', views.verify_and_checkout, name='verify_and_checkout'),
    
    # Notifications
    path('notifications/', views.get_notifications, name='get_notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    
    # Messaging
    path('messages/send/', views.send_message, name='send_message'),
    path('messages/get/', views.get_messages, name='get_messages'),
    
    # API endpoints
    path('api/bus/<int:bus_id>/attendant/', views.get_bus_attendant, name='get_bus_attendant'),
    
    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/landing/', views.admin_dashboard, name='admin_landing'),
    path('admin/students/', views.manage_students, name='manage_students'),
    path('admin/buses/', views.manage_buses, name='manage_buses'),
    path('admin/users/', views.manage_users, name='manage_users'),
    path('admin/attendance/', views.view_attendance_reports, name='attendance_reports'),
    path('guardian/trips/', views.guardian_trip_history, name='guardian_trips'),
]
