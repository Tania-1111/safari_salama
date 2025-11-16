# 🚌 Safari Salama - Student Transportation Management System

## Complete Implementation Guide

A comprehensive Django web application for managing student transportation in Kenyan schools, featuring real-time GPS tracking, biometric authentication, and instant notifications.

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Installation & Setup](#installation--setup)
5. [Database Schema](#database-schema)
6. [User Roles & Features](#user-roles--features)
7. [API Endpoints](#api-endpoints)
8. [GPS Tracking Implementation](#gps-tracking-implementation)
9. [Biometric System](#biometric-system)
10. [Notification System](#notification-system)
11. [Frontend Components](#frontend-components)
12. [Deployment Guide](#deployment-guide)

---

## 🎯 Project Overview

**Safari Salama** is a student transportation management system designed for Kenyan schools. It helps schools, guardians, drivers, and attendants manage bus transportation efficiently.

### Key Features:
- ✅ Multi-user authentication (Guardian, Driver, Attendant, School Admin, Student)
- ✅ Real-time GPS tracking of buses
- ✅ Biometric authentication (fingerprint/facial recognition)
- ✅ Real-time notifications via email, SMS, and push notifications
- ✅ Student attendance tracking (boarding/alighting)
- ✅ Route management and optimization
- ✅ Admin dashboard with analytics
- ✅ WebSocket support for live updates

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend Layer                         │
├──────────────┬──────────────┬──────────────┬─────────────┤
│  Guardian    │    Driver    │  Attendant   │    Admin    │
│  Dashboard   │  Dashboard   │  Interface   │  Dashboard  │
└──────────────┴──────────────┴──────────────┴─────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              API & WebSocket Layer                        │
├─────────────────────────────────────────────────────────┤
│  REST API (Django REST Framework)                        │
│  WebSocket (Django Channels)                             │
│  Authentication (JWT/Session)                            │
└─────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│          Application Logic Layer (Views)                 │
├─────────────────────────────────────────────────────────┤
│  Authentication & Authorization                          │
│  GPS Tracking Engine                                     │
│  Biometric Processing                                    │
│  Notification Service                                    │
│  Attendance Management                                   │
└─────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│          Data Access Layer (Models)                      │
├─────────────────────────────────────────────────────────┤
│  User Management                                         │
│  Bus Information                                         │
│  Student Records                                         │
│  GPS Locations                                           │
│  Notifications & Logs                                    │
└─────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│            Database Layer                                │
├─────────────────────────────────────────────────────────┤
│  PostgreSQL / SQLite3                                    │
│  Redis (Caching & Session)                              │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 4.2.7
- **API**: Django REST Framework
- **Real-time**: Django Channels (WebSocket)
- **ASGI Server**: Daphne

### Frontend
- **HTML5**, **CSS3**, **JavaScript (Vanilla)**
- **Google Maps API** (for bus tracking)
- **WebSocket Client** (for real-time updates)

### Database
- **Primary**: PostgreSQL (production) / SQLite3 (development)
- **Cache**: Redis

### Biometric Processing
- **OpenCV**: Image processing
- **face_recognition**: Facial recognition
- **py-fingerprint**: Fingerprint recognition

### Notifications
- **Twilio**: SMS notifications
- **Firebase Cloud Messaging**: Push notifications
- **Django Mail**: Email notifications

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 12+ (optional, SQLite for development)
- Redis (for caching)
- Node.js 16+ (optional, for frontend build tools)

### Step 1: Clone & Setup Project

```bash
# Navigate to project directory
cd c:\Users\USER\Desktop\safariSalama_FD

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Django Settings

Edit `schooltransport/setting.py`:

```python
# Change SECRET_KEY
SECRET_KEY = 'your-secret-key-here'

# Set Google Maps API Key
GOOGLE_MAPS_API_KEY = 'your-google-maps-api-key'

# Configure Database (optional, default is SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'safiri_salama',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Configure Email
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'

# Twilio Configuration
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = '+1234567890'

# Firebase Configuration
FIREBASE_API_KEY = 'your_firebase_key'
FIREBASE_PROJECT_ID = 'your_project_id'
```

### Step 3: Initialize Database

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser
```

### Step 4: Create Directories

```bash
# Create media and logs directories
mkdir media logs static
```

### Step 5: Run Development Server

```bash
# Using Daphne (for WebSocket support)
daphne -b 0.0.0.0 -p 8000 schooltransport.asgi:application

# Or use runserver (without WebSocket)
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

---

## 📊 Database Schema

### Core Models

```
┌─────────────────┐
│   User          │
│  (Django Auth)  │
└────────┬────────┘
         │
         ▼
┌──────────────────┐       ┌──────────────┐
│  UserProfile     │       │   School     │
│ - user_type      │       │ - name       │
│ - phone_number   │◄──────┤ - location   │
│ - address        │       │ - latitude   │
│ - verified       │       │ - longitude  │
└──────────────────┘       └────────┬─────┘
         ▲                          │
         │                          ▼
         │                  ┌────────────────┐
         │                  │      Bus       │
         │                  │ - registration │
         │                  │ - capacity     │
         │                  │ - driver_id    │
         │                  │ - attendant_id │
         │                  └────────┬───────┘
         │                           │
         │           ┌───────────────┼───────────────┐
         │           │               │               │
         │           ▼               ▼               ▼
         │      ┌─────────┐  ┌──────────────┐  ┌──────────────┐
         │      │ Student │  │ BusLocation  │  │ StudentAttend│
         │      │ - class │  │ - latitude   │  │ - status     │
         │      │ - bio   │  │ - longitude  │  │ - verified   │
         │      │ - data  │  │ - timestamp  │  │ - location   │
         │      │         │  │              │  │              │
         │      └────┬────┘  └──────────────┘  └──────────────┘
         │           │
         │           ▼
         │     ┌─────────────┐
         └────►│ Notification│
               │ - recipient │
               │ - message   │
               │ - type      │
               └─────────────┘
```

### Key Models Details:

**UserProfile**
```
- user (FK: User)
- user_type (guardian|driver|attendant|admin|student)
- phone_number
- profile_image
- address
- verified
```

**School**
```
- admin (FK: User)
- name
- location
- latitude, longitude
- registration_number
```

**Bus**
```
- school (FK)
- driver (FK: User)
- attendant (FK: User)
- registration_number
- capacity
- current_latitude, longitude
- status (active|on_route|at_school)
```

**Student**
```
- school (FK)
- user (FK)
- guardian (FK: User)
- bus (FK)
- registration_number
- biometric_template (JSON)
- biometric_type
- biometric_enrolled
```

**StudentAttendance**
```
- student (FK)
- bus (FK)
- status (boarded|alighted)
- latitude, longitude
- biometric_verified
- biometric_confidence
- timestamp
```

**BusLocation**
```
- bus (FK)
- latitude, longitude
- accuracy
- speed
- heading
- timestamp
```

**Notification**
```
- recipient (FK: User)
- notification_type
- title, message
- student (FK)
- bus (FK)
- is_read
```

---

## 👥 User Roles & Features

### 1. Guardian (Parent/Parent)

**Features:**
- ✅ View students under their care
- ✅ Track bus location in real-time
- ✅ Receive notifications when student boards/alights
- ✅ View student attendance history
- ✅ Contact driver/attendant

**Dashboard Components:**
- Student list with status
- Live map with bus location
- Notifications panel
- Attendance reports

### 2. Driver

**Features:**
- ✅ Start/end routes
- ✅ GPS tracking (automatic updates every 10 seconds)
- ✅ View assigned bus details
- ✅ View route stops
- ✅ View students on bus
- ✅ Receive notifications

**Dashboard Components:**
- Live GPS tracking map
- Route information
- Students list
- GPS status indicator

### 3. Attendant

**Features:**
- ✅ Record student boarding (via biometric)
- ✅ Record student alighting (via biometric)
- ✅ View student list
- ✅ Confirm attendance

### 4. School Admin

**Features:**
- ✅ Manage students
- ✅ Manage buses
- ✅ Manage drivers/attendants
- ✅ View attendance reports
- ✅ Configure routes
- ✅ View analytics

**Dashboard:**
- Overview statistics
- Student management
- Bus management
- Attendance reports

### 5. Student

**Features:**
- ✅ Enroll biometric
- ✅ Board/alight via biometric
- ✅ No manual login needed

---

## 🔌 API Endpoints

### Authentication

```
POST   /register/                  - Register new user
POST   /login/                     - Login user
GET    /logout/                    - Logout user
```

### Guardian APIs

```
GET    /guardian/dashboard/        - Get guardian dashboard
GET    /guardian/student/<id>/status/ - Get student bus status
GET    /notifications/             - Get user notifications
POST   /notifications/<id>/read/   - Mark notification as read
```

### Driver APIs

```
GET    /driver/dashboard/          - Get driver dashboard
POST   /driver/location/update/    - Update bus location (GPS)
GET    /driver/bus/<id>/route/     - Get assigned route
```

### Biometric & Attendance APIs

```
POST   /biometric/enroll/          - Enroll student biometric
POST   /attendance/checkin/        - Student boards (biometric verify)
POST   /attendance/checkout/       - Student alights (biometric verify)
```

### Admin APIs

```
GET    /admin/dashboard/           - Admin dashboard
GET    /admin/students/            - List students
GET    /admin/buses/               - List buses
GET    /admin/attendance/          - Attendance reports
```

### WebSocket Endpoints

```
ws://localhost:8000/ws/notifications/              - Get notifications
ws://localhost:8000/ws/bus/<bus_id>/tracking/      - Track bus live
ws://localhost:8000/ws/bus/<bus_id>/checkin/       - Receive checkin events
```

---

## 🗺️ GPS Tracking Implementation

### How It Works:

#### 1. **Driver-Side GPS Capture**

The driver's app uses the browser's Geolocation API:

```javascript
// Start continuous GPS tracking
navigator.geolocation.watchPosition(
    (position) => {
        const { latitude, longitude, accuracy, speed, heading } = position.coords;
        
        // Send to server
        fetch('/driver/location/update/', {
            method: 'POST',
            body: JSON.stringify({
                bus_id: 1,
                latitude: latitude,
                longitude: longitude,
                accuracy: accuracy,
                speed: speed * 3.6,  // Convert m/s to km/h
                heading: heading
            })
        });
    },
    (error) => console.error(error),
    {
        enableHighAccuracy: true,
        maximumAge: 10000,  // 10 seconds
        timeout: 30000      // 30 seconds
    }
);
```

#### 2. **Server-Side Location Storage**

Location data is saved in the database:

```python
# views.py
@csrf_exempt
def update_bus_location(request):
    data = json.loads(request.body)
    bus = Bus.objects.get(id=data['bus_id'])
    
    # Save location history
    location = BusLocation.objects.create(
        bus=bus,
        latitude=data['latitude'],
        longitude=data['longitude'],
        accuracy=data['accuracy'],
        speed=data['speed'],
        heading=data['heading']
    )
    
    # Update current location
    bus.current_latitude = data['latitude']
    bus.current_longitude = data['longitude']
    bus.save()
```

#### 3. **Guardian-Side Map Display**

Guardians see real-time bus location on Google Maps:

```javascript
// Initialize map
let map = new google.maps.Map(document.getElementById('map'), {
    zoom: 15,
    center: { lat: -1.2865, lng: 36.8172 }
});

// Update bus marker periodically
function updateBusLocation() {
    fetch(`/guardian/student/${studentId}/status/`)
        .then(res => res.json())
        .then(data => {
            const location = data.bus.current_location;
            const buMarker = new google.maps.Marker({
                position: { lat: location.latitude, lng: location.longitude },
                map: map,
                title: 'Bus Location'
            });
            map.setCenter(buMarker.getPosition());
        });
}

// Refresh every 10 seconds
setInterval(updateBusLocation, 10000);
```

#### 4. **Google Maps Integration**

**Setup Steps:**

1. **Get Google Maps API Key:**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project
   - Enable "Maps JavaScript API"
   - Create an API key
   - Restrict to your domain

2. **Include API in Templates:**
   ```html
   <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY"></script>
   ```

3. **Display Features:**
   - Bus current location (yellow marker)
   - School location (blue marker)
   - Route stops (green markers)
   - Polyline showing the route
   - Route optimization

---

## 🔐 Biometric System

### Architecture:

```
┌─────────────────────────────────────────────┐
│         Biometric Device Input              │
│  (Webcam, Fingerprint Scanner, etc.)       │
└────────────────┬────────────────────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  Image Capture  │
        │  (Base64)       │
        └────────┬────────┘
                 │
                 ▼
    ┌────────────────────────────┐
    │  Biometric Processing      │
    │  - Image Preprocessing     │
    │  - Feature Extraction      │
    │  - Template Creation       │
    └────────────────┬───────────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
    ┌─────────────┐         ┌──────────────┐
    │ Fingerprint │         │   Facial     │
    │ Recognition │         │ Recognition  │
    └─────────────┘         └──────────────┘
         │                        │
         └───────────┬────────────┘
                     ▼
         ┌──────────────────────┐
         │  Matching Engine     │
         │  - Compare captured  │
         │  - Calculate score   │
         │  - Return confidence │
         └──────────┬───────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
    ┌────────┐           ┌──────────┐
    │ Match  │           │  No Match│
    │ >75%   │           │  <75%    │
    └────────┘           └──────────┘
```

### Fingerprint Recognition Implementation:

```python
from schooltransport.biometric import BiometricSystem, FingerprintProcessor

# Initialize system
biometric = BiometricSystem(biometric_type='fingerprint')

# 1. Enrollment - Store fingerprint
enrollment_result = biometric.enroll_biometric(
    image_data=base64_encoded_image,
    student_name='John Doe'
)
# Result: {'success': True, 'template': {...}, 'confidence': 95.0}

# 2. Verification - Compare captured with stored
is_match, confidence = biometric.verify_biometric(
    captured_data=captured_image,
    stored_template=student.biometric_template
)
# Returns: (True, 92.5) or (False, 35.2)

# 3. Create attendance record if match
if is_match and confidence > 75:
    StudentAttendance.objects.create(
        student=student,
        bus=bus,
        status='boarded',
        biometric_verified=True,
        biometric_confidence=confidence
    )
```

### Facial Recognition Implementation:

```python
from schooltransport.biometric import BiometricSystem

# Initialize facial recognition
biometric = BiometricSystem(biometric_type='facial')

# Enrollment
enrollment = biometric.enroll_biometric(
    image_data=selfie_image,
    student_name='Jane Doe'
)

# Verification
is_match, confidence = biometric.verify_biometric(
    captured_data=captured_selfie,
    stored_template=student.biometric_template
)
```

### Biometric Device Capture:

```python
from schooltransport.biometric import BiometricDevice

# Capture from webcam
image_data = BiometricDevice.capture_from_webcam(device_index=0)

# Or show preview and wait for capture
image_data = BiometricDevice.display_capture_preview(timeout=5000)

# Send to server for enrollment
response = requests.post(
    'http://localhost:8000/biometric/enroll/',
    json={
        'student_id': 123,
        'biometric_data': image_data,
        'biometric_type': 'fingerprint'
    }
)
```

---

## 📢 Notification System

### Notification Flow:

```
Student Boards/Alights
         │
         ▼
┌─────────────────────────┐
│  StudentAttendance      │
│  Record Created         │
└────────────┬────────────┘
             │
             ▼
┌──────────────────────────────┐
│ send_notification_to_guardian │
└────────────┬─────────────────┘
             │
    ┌────────┼────────┬────────────┐
    ▼        ▼        ▼            ▼
┌─────┐┌────────┐┌──────┐┌───────────┐
│Email││  SMS   ││Push  ││ In-App    │
│     ││(Twilio)││(FCM) ││Notification
└─────┘└────────┘└──────┘└───────────┘
    │        │        │            │
    └────────┴────────┴────────────┘
             │
             ▼
Guardian receives alert
```

### Implementation:

**1. Email Notifications:**
```python
from django.core.mail import send_mail

send_mail(
    subject='Student Transportation Alert',
    message=f'{student_name} has boarded bus {bus_registration}',
    from_email='noreply@safarisalama.com',
    recipient_list=[guardian.email],
    fail_silently=True,
)
```

**2. SMS Notifications (Twilio):**
```python
from twilio.rest import Client

client = Client(account_sid, auth_token)
message = client.messages.create(
    body=f'{student_name} boarded bus {bus_reg}',
    from_=twilio_phone,
    to=guardian_phone
)
```

**3. Push Notifications (Firebase):**
```python
import firebase_admin
from firebase_admin import messaging

message = messaging.Message(
    notification=messaging.Notification(
        title='Student Transportation',
        body=f'{student_name} has boarded',
    ),
    token=fcm_token,
)
response = messaging.send(message)
```

**4. In-App Notifications (WebSocket):**
```javascript
// Connect to WebSocket
const socket = new WebSocket('ws://localhost:8000/ws/notifications/');

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    showNotification(data.title, data.message);
};
```

---

## 🎨 Frontend Components

### 1. Guardian Dashboard

**Features:**
- Student list on the left
- Live map showing bus location
- Bus status information
- Attendance log
- Notification bell

### 2. Driver Dashboard

**Features:**
- GPS map showing current location
- Route information panel
- Students on bus list
- Start/Stop route buttons
- GPS status indicator

### 3. Admin Dashboard

**Features:**
- Summary statistics
- Student management
- Bus management
- Attendance reports
- Analytics charts

### 4. Biometric Interface (Attendant)

**Features:**
- Webcam/biometric scanner input
- Real-time capture preview
- Student identification
- Confirmation message
- Manual override option

---

## 🚀 Deployment Guide

### Production Checklist:

1. **Security:**
   ```python
   # settings.py
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

2. **Database:**
   ```bash
   # Use PostgreSQL
   pip install psycopg2-binary
   
   # Configure in settings.py
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'safiri_salama',
           'USER': 'postgres',
           'PASSWORD': 'strong_password',
           'HOST': 'your_host',
           'PORT': '5432',
       }
   }
   ```

3. **Static Files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Run with Gunicorn + Nginx:**
   ```bash
   pip install gunicorn
   gunicorn schooltransport.wsgi:application --workers 4 --bind 0.0.0.0:8000
   ```

5. **Use Daphne for WebSocket:**
   ```bash
   daphne -b 0.0.0.0 -p 8000 schooltransport.asgi:application
   ```

6. **Environment Variables:**
   ```
   DJANGO_SECRET_KEY=your_secret_key
   GOOGLE_MAPS_API_KEY=your_key
   TWILIO_ACCOUNT_SID=your_sid
   TWILIO_AUTH_TOKEN=your_token
   FIREBASE_API_KEY=your_key
   EMAIL_HOST_USER=your_email
   EMAIL_HOST_PASSWORD=your_password
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   ```

---

## 📞 Support & Troubleshooting

### Common Issues:

1. **GPS not updating:**
   - Check browser location permissions
   - Ensure HTTPS for production
   - Check network connectivity

2. **Biometric not recognizing:**
   - Ensure good lighting
   - Clean camera lens
   - Adjust threshold values

3. **WebSocket connection fails:**
   - Use Daphne instead of runserver
   - Check firewall settings
   - Verify channel layer configuration

---

## 📝 Notes for Beginners

1. Start with SQLite for development
2. Use Django admin to test models
3. Test APIs with Postman before frontend integration
4. Read Django documentation: https://docs.djangoproject.com/
5. Google Maps API requires billing setup
6. Twilio requires account credits for SMS

---

**Created:** November 2025
**Version:** 1.0.0
**License:** MIT
