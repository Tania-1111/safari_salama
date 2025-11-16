from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, School, Bus, Student, StudentAttendance,
    BusLocation, Notification, Route, RouteStop
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'user_type', 'phone_number', 'profile_image', 'address', 'verified']


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


class BusLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusLocation
        fields = ['id', 'latitude', 'longitude', 'accuracy', 'speed', 'heading', 'timestamp']


class BusSerializer(serializers.ModelSerializer):
    current_location = serializers.SerializerMethodField()
    driver_name = serializers.CharField(source='driver.get_full_name', read_only=True)
    attendant_name = serializers.CharField(source='attendant.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = Bus
        fields = [
            'id', 'registration_number', 'capacity', 'current_latitude',
            'current_longitude', 'status', 'driver_name', 'attendant_name',
            'is_active', 'created_at', 'updated_at', 'current_location'
        ]

    def get_current_location(self, obj):
        latest = obj.location_history.latest('timestamp')
        if latest:
            return BusLocationSerializer(latest).data
        return None


class StudentAttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    bus_registration = serializers.CharField(source='bus.registration_number', read_only=True)

    class Meta:
        model = StudentAttendance
        fields = [
            'id', 'student', 'student_name', 'bus', 'bus_registration',
            'status', 'latitude', 'longitude', 'location_name',
            'biometric_verified', 'biometric_confidence', 'timestamp', 'date'
        ]


class StudentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    guardian_name = serializers.CharField(source='guardian.get_full_name', read_only=True, allow_null=True)
    bus_registration = serializers.CharField(source='bus.registration_number', read_only=True, allow_null=True)
    recent_attendance = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id', 'user', 'user_name', 'registration_number', 'date_of_birth',
            'class_name', 'guardian', 'guardian_name', 'bus', 'bus_registration',
            'biometric_enrolled', 'biometric_type', 'parent_phone',
            'created_at', 'updated_at', 'recent_attendance'
        ]

    def get_recent_attendance(self, obj):
        attendance = obj.attendance_logs.all()[:5]
        return StudentAttendanceSerializer(attendance, many=True).data


class RouteStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteStop
        fields = ['id', 'name', 'latitude', 'longitude', 'order', 'estimated_arrival_time']


class RouteSerializer(serializers.ModelSerializer):
    stops = RouteStopSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = ['id', 'name', 'description', 'start_location', 'end_location',
                  'estimated_duration', 'is_active', 'created_at', 'stops']


class NotificationSerializer(serializers.ModelSerializer):
    recipient_name = serializers.CharField(source='recipient.get_full_name', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'recipient_name', 'notification_type', 'title',
            'message', 'student', 'student_name', 'bus', 'is_read', 'read_at',
            'created_at', 'updated_at'
        ]
