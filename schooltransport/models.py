from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

# User Types
USER_TYPES = (
    ('guardian', 'Guardian'),
    ('driver', 'Driver'),
    ('attendant', 'Attendant'),
    ('admin', 'School Admin'),
    ('student', 'Student'),
)

# Bus Status
BUS_STATUS = (
    ('inactive', 'Inactive'),
    ('active', 'Active'),
    ('on_route', 'On Route'),
    ('at_school', 'At School'),
)

# Attendance Status
ATTENDANCE_STATUS = (
    ('boarded', 'Boarded'),
    ('alighted', 'Alighted'),
)


class UserProfile(models.Model):
    """Extended user profile to store user type and additional information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_user_type_display()}"

    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class School(models.Model):
    """School information"""
    admin = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'profile__user_type': 'admin'})
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    latitude = models.FloatField()  # School GPS coordinate
    longitude = models.FloatField()  # School GPS coordinate
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    registration_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'schools'


class Bus(models.Model):
    """Bus information and tracking"""
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='buses')
    driver = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, 
                                   limit_choices_to={'profile__user_type': 'driver'},
                                   related_name='driven_bus')
    attendant = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True,
                                      limit_choices_to={'profile__user_type': 'attendant'},
                                      related_name='attended_bus')
    registration_number = models.CharField(max_length=50, unique=True)
    capacity = models.IntegerField(default=50)
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=BUS_STATUS, default='inactive')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.registration_number} - {self.school.name}"

    class Meta:
        db_table = 'buses'


class Student(models.Model):
    """Student information and biometric data"""
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    guardian = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                 limit_choices_to={'profile__user_type': 'guardian'},
                                 related_name='students')
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    registration_number = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField()
    class_name = models.CharField(max_length=50)  # e.g., "Form 1A"
    
    # Biometric data
    biometric_template = models.JSONField(default=dict, blank=True)  # Store fingerprint/facial recognition data
    biometric_type = models.CharField(max_length=20, choices=[('fingerprint', 'Fingerprint'), ('facial', 'Facial')],
                                      default='fingerprint')
    biometric_enrolled = models.BooleanField(default=False)
    
    # Contact
    parent_phone = models.CharField(max_length=15)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.registration_number}"

    class Meta:
        db_table = 'students'


class StudentAttendance(models.Model):
    """Track student boarding and alighting events"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_logs')
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, related_name='attendance_logs')
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS)
    
    # Location where the event occurred
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    location_name = models.CharField(max_length=255, blank=True, null=True)
    
    # Biometric verification
    biometric_verified = models.BooleanField(default=False)
    biometric_confidence = models.FloatField(default=0.0)  # 0-100 confidence score
    
    timestamp = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.status} - {self.timestamp}"

    class Meta:
        db_table = 'student_attendance'
        ordering = ['-timestamp']


class BusLocation(models.Model):
    """Track bus GPS coordinates in real-time"""
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='location_history')
    latitude = models.FloatField()
    longitude = models.FloatField()
    accuracy = models.FloatField(null=True, blank=True)  # GPS accuracy in meters
    speed = models.FloatField(null=True, blank=True)  # Speed in km/h
    heading = models.FloatField(null=True, blank=True)  # Direction 0-360
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bus.registration_number} at {self.timestamp}"

    class Meta:
        db_table = 'bus_locations'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['bus', '-timestamp']),
        ]


class Notification(models.Model):
    """Send notifications to guardians"""
    NOTIFICATION_TYPES = (
        ('boarded', 'Student Boarded Bus'),
        ('alighted', 'Student Alighted Bus'),
        ('delayed', 'Bus Delayed'),
        ('arrived', 'Bus Arrived at School'),
        ('system_alert', 'System Alert'),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='notifications')
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True,
                           related_name='notifications')
    
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # For push notifications (FCM)
    fcm_token = models.CharField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.recipient.get_full_name()}"

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']


class Route(models.Model):
    """Define bus routes"""
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='routes')
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='routes')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    estimated_duration = models.IntegerField(help_text="In minutes")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.bus.registration_number}"

    class Meta:
        db_table = 'routes'


class RouteStop(models.Model):
    """Individual stops on a route"""
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    order = models.IntegerField()  # Order of stop in route
    estimated_arrival_time = models.IntegerField(help_text="In minutes from start")

    def __str__(self):
        return f"{self.route.name} - Stop {self.order}: {self.name}"

    class Meta:
        db_table = 'route_stops'
        ordering = ['route', 'order']


class BiometricEnrollment(models.Model):
    """Store fingerprint templates for students"""
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='biometric_enrollment')
    fingerprint_template = models.BinaryField(null=True, blank=True)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)

    def __str__(self):
        return f"Biometric: {self.student.user.get_full_name()}"

    class Meta:
        db_table = 'biometric_enrollment'


class BiometricLog(models.Model):
    """Log all fingerprint scan attempts"""
    STATUS_CHOICES = [
        ('match', 'Match'),
        ('no_match', 'No Match'),
        ('error', 'Error'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='biometric_logs')
    scan_time = models.DateTimeField(auto_now_add=True)
    match_score = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='error')
    location = models.CharField(max_length=100, blank=True)
    scan_type = models.CharField(max_length=20, choices=[('checkin', 'Check In'), ('checkout', 'Check Out')], default='checkin')

    def __str__(self):
        return f"{self.student.user.first_name} - {self.status} at {self.scan_time}"

    class Meta:
        db_table = 'biometric_logs'
        ordering = ['-scan_time']


class Message(models.Model):
    """Direct messaging between guardians and attendants"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    message_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Message from {self.sender.get_full_name()} to {self.recipient.get_full_name()}"

    class Meta:
        db_table = 'messages'
        ordering = ['-timestamp']
