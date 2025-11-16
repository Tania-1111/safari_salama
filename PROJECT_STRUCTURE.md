# Safari Salama - Complete Project Structure

```
safariSalama_FD/
│
├── manage.py                          # Django command-line utility
├── requirements.txt                   # Python dependencies
├── README.md                          # Project documentation
├── BEGINNER_GUIDE.md                 # Step-by-step beginner guide
├── setup_demo.py                     # Create demo data
│
├── schooltransport/                  # Main Django app
│   │
│   ├── __init__.py
│   ├── asgi.py                       # ASGI configuration (WebSocket)
│   ├── wsgi.py                       # WSGI configuration (HTTP)
│   ├── setting.py                    # Django settings
│   ├── urls.py                       # URL routing
│   ├── routing.py                    # WebSocket routing
│   │
│   ├── models.py                     # Database models
│   │   ├── UserProfile               # User types (guardian, driver, etc)
│   │   ├── School                    # School information
│   │   ├── Bus                       # Bus details
│   │   ├── Student                   # Student records
│   │   ├── BusLocation              # GPS history
│   │   ├── StudentAttendance        # Attendance tracking
│   │   ├── Notification             # Notification records
│   │   ├── Route                    # Bus routes
│   │   └── RouteStop                # Route waypoints
│   │
│   ├── views.py                      # View logic
│   │   ├── register()                # User registration
│   │   ├── login_view()              # User login
│   │   ├── guardian_dashboard()      # Guardian UI
│   │   ├── driver_dashboard()        # Driver UI
│   │   ├── update_bus_location()     # Receive GPS updates
│   │   ├── verify_and_checkin()      # Student boarding
│   │   ├── verify_and_checkout()     # Student alighting
│   │   ├── admin_dashboard()         # Admin UI
│   │   └── ... (20+ more views)
│   │
│   ├── serializers.py                # REST API serializers
│   │   ├── UserSerializer
│   │   ├── BusSerializer
│   │   ├── StudentSerializer
│   │   ├── NotificationSerializer
│   │   └── ...
│   │
│   ├── consumers.py                  # WebSocket consumers
│   │   ├── NotificationConsumer      # Real-time notifications
│   │   ├── BusTrackingConsumer       # Live GPS updates
│   │   └── StudentCheckinConsumer    # Attendance events
│   │
│   ├── biometric.py                  # Biometric processing
│   │   ├── BiometricSystem           # Main biometric handler
│   │   ├── FingerprintProcessor      # Fingerprint recognition
│   │   ├── FacialRecognition         # Facial recognition
│   │   └── BiometricDevice           # Device interfaces
│   │
│   ├── admin.py                      # Django admin configuration
│   ├── apps.py                       # App configuration
│   ├── tests.py                      # Unit tests
│   │
│   ├── static/                       # Static files
│   │   ├── css/
│   │   │   ├── style.css            # Main stylesheet
│   │   │   ├── dashboard.css        # Dashboard styles
│   │   │   └── responsive.css       # Mobile styles
│   │   ├── js/
│   │   │   ├── map.js               # Google Maps integration
│   │   │   ├── gps.js               # GPS handling
│   │   │   ├── biometric.js         # Biometric UI
│   │   │   ├── notifications.js     # Notification handling
│   │   │   └── websocket.js         # WebSocket client
│   │   └── images/
│   │       ├── logo.png
│   │       ├── icons.svg
│   │       └── ...
│   │
│   └── templates/                    # HTML templates
│       ├── base.html                # Base template
│       ├── login.html               # Login page
│       ├── register.html            # Registration page
│       │
│       ├── guardian/
│       │   ├── dashboard.html       # Guardian dashboard
│       │   ├── student_list.html    # View students
│       │   ├── map.html             # Bus tracking map
│       │   └── notifications.html   # View notifications
│       │
│       ├── driver/
│       │   ├── dashboard.html       # Driver dashboard
│       │   ├── gps_map.html         # GPS tracking
│       │   ├── route_info.html      # Route details
│       │   └── students_on_bus.html # Student list
│       │
│       ├── attendant/
│       │   ├── checkin.html         # Student boarding
│       │   ├── checkout.html        # Student alighting
│       │   └── biometric_input.html # Biometric capture
│       │
│       └── admin/
│           ├── dashboard.html       # Admin dashboard
│           ├── students.html        # Manage students
│           ├── buses.html           # Manage buses
│           ├── drivers.html         # Manage drivers
│           ├── routes.html          # Manage routes
│           └── reports.html         # Attendance reports
│
├── media/                            # User-uploaded files
│   ├── profiles/                    # Profile pictures
│   └── documents/                   # Documents
│
├── logs/                            # Application logs
│   └── safari_salama.log
│
├── venv/                            # Virtual environment
│   ├── Lib/
│   ├── Scripts/
│   └── ...
│
└── db.sqlite3                       # SQLite database (development only)
```

---

## File Descriptions

### Core Django Files

| File | Purpose |
|------|---------|
| `manage.py` | Django management commands (migrate, runserver, etc) |
| `settings.py` | Configuration (database, apps, security, API keys) |
| `urls.py` | URL routing for HTTP requests |
| `routing.py` | URL routing for WebSocket requests |
| `wsgi.py` | Production web server interface |
| `asgi.py` | WebSocket server interface |

### Application Logic

| File | Purpose |
|------|---------|
| `models.py` | Database schema (9 models) |
| `views.py` | Business logic and API endpoints (20+ views) |
| `serializers.py` | REST API response formatting |
| `consumers.py` | WebSocket handlers |
| `biometric.py` | Fingerprint & facial recognition |

### Frontend Files

| Directory | Files | Purpose |
|-----------|-------|---------|
| `templates/` | 15+ HTML files | User interfaces |
| `static/css/` | 3+ stylesheets | Design & layout |
| `static/js/` | 5+ scripts | Interactivity & API calls |
| `static/images/` | Icons & assets | Visual elements |

### Configuration Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python package dependencies |
| `README.md` | Project documentation |
| `BEGINNER_GUIDE.md` | Step-by-step setup guide |

---

## Technology Stack Mapping

```
Frontend Layer
    │
    ├── HTML5 Templates
    │   └── guardian/dashboard.html
    │   └── driver/dashboard.html
    │   └── login.html
    │
    ├── CSS3 Styling
    │   └── Responsive design
    │   └── Material design
    │
    └── JavaScript (Vanilla + Libraries)
        ├── Google Maps API
        ├── WebSocket client
        ├── Fetch API (HTTP)
        └── Geolocation API
        
API Layer
    │
    ├── REST API (Django REST Framework)
    │   ├── Authentication endpoints
    │   ├── Student management
    │   ├── Bus tracking
    │   └── Biometric endpoints
    │
    └── WebSocket (Django Channels)
        ├── Real-time notifications
        ├── Live GPS updates
        └── Attendance events

Business Logic Layer
    │
    ├── Authentication & Authorization
    │   └── User roles (5 types)
    │
    ├── GPS Tracking Engine
    │   ├── Location capture
    │   ├── History storage
    │   └── Distance calculation
    │
    ├── Biometric Processing
    │   ├── Fingerprint recognition
    │   └── Facial recognition
    │
    └── Notification Service
        ├── Email (Django Mail)
        ├── SMS (Twilio)
        ├── Push (Firebase)
        └── WebSocket (real-time)

Data Layer
    │
    └── Database (SQLite/PostgreSQL)
        ├── Users (9 models)
        ├── GPS locations
        ├── Attendance records
        └── Notifications
```

---

## Data Flow Diagrams

### 1. Guardian Tracking Bus (Read-Only)

```
Guardian Opens Dashboard
    │
    ▼
fetch('/guardian/dashboard/') [REST API]
    │
    ▼
Django View: guardian_dashboard()
    │
    ▼
Query Database:
  - Get students
  - Get buses
    │
    ▼
Return JSON with coordinates
    │
    ▼
Display on Google Maps
    │
    ▼
Auto-refresh every 10 seconds
```

### 2. Driver Updates GPS Location

```
Driver Clicks "Start GPS Tracking"
    │
    ▼
Browser Permission: Allow Location
    │
    ▼
navigator.geolocation.watchPosition()
    │
    ▼
Capture: Latitude, Longitude, Speed, Heading
    │
    ▼
POST /driver/location/update/ [REST API]
    │
    ▼
Django View: update_bus_location()
    │
    ▼
Create BusLocation Record
Update Bus.current_latitude/longitude
    │
    ▼
Database Saved ✓
    │
    ▼
Guardian's Map Auto-Updates
  (via auto-refresh or WebSocket)
```

### 3. Student Boarding Process

```
Student Arrives at Bus
    │
    ▼
Attendant Initiates Check-In
    │
    ▼
Biometric Device Captures Fingerprint/Face
    │
    ▼
Send Image to Server: POST /attendance/checkin/
    │
    ▼
Django View: verify_and_checkin()
    │
    ├─► BiometricSystem.verify_biometric()
    │   │
    │   ├─► FingerprintProcessor.match()
    │   │   └─► Compare feature descriptors
    │   │
    │   └─► Calculate confidence score
    │
    ▼
Confidence > 75%?
    │
    ├─► YES: Create StudentAttendance Record
    │   ├─► status = 'boarded'
    │   ├─► biometric_verified = True
    │   └─► latitude, longitude = bus location
    │
    ├─► NO: Return error "Not recognized"
    │
    ▼
Send Notification to Guardian
    │
    ├─► Email
    ├─► SMS (if phone available)
    ├─► Push notification (if Firebase)
    └─► WebSocket (real-time in-app)
    │
    ▼
Guardian Receives Alert ✓
  "David has boarded bus KCA-123A"
```

### 4. Notification Delivery

```
Event Triggers:
├─► Student Boarded
├─► Student Alighted
├─► Bus Delayed
└─► System Alert

        │
        ▼
Call: send_notification_to_guardian()
        │
        ├────────────────────┬─────────────┬──────────────┐
        │                    │             │              │
        ▼                    ▼             ▼              ▼
    Database          Email Server    Twilio API    Firebase API
    (In-App)          (Gmail)          (SMS)         (Push)
        │                    │             │              │
        └────────────────────┴─────────────┴──────────────┘
                            │
                            ▼
                    Guardian Receives:
                    - In-app notification
                    - Email
                    - SMS
                    - Push notification
```

---

## Key Endpoints Summary

### Authentication (Public)
- `POST /register/` - New user registration
- `POST /login/` - User login
- `GET /logout/` - User logout

### Guardian (Protected)
- `GET /guardian/dashboard/` - Main dashboard
- `GET /guardian/student/<id>/status/` - Student bus status
- `GET /notifications/` - Get notifications
- `POST /notifications/<id>/read/` - Mark read

### Driver (Protected)
- `GET /driver/dashboard/` - Driver dashboard
- `POST /driver/location/update/` - Update GPS (frequent)
- `GET /driver/bus/<id>/route/` - Get route info

### Biometric & Attendance (Protected)
- `POST /biometric/enroll/` - Enroll fingerprint
- `POST /attendance/checkin/` - Board student
- `POST /attendance/checkout/` - Alight student

### Admin (Protected)
- `GET /admin/dashboard/` - Admin panel
- `GET /admin/students/` - List students
- `GET /admin/buses/` - List buses
- `GET /admin/attendance/` - Attendance reports

### WebSocket (Protected)
- `ws://server/ws/notifications/` - Get alerts
- `ws://server/ws/bus/<id>/tracking/` - Track bus live
- `ws://server/ws/bus/<id>/checkin/` - Attendance events

---

## Database Tables (9 Models)

| Table | Rows | Purpose |
|-------|------|---------|
| `auth_user` | 5 | Django user accounts |
| `user_profiles` | 5 | User types & metadata |
| `schools` | 1 | School information |
| `buses` | 2 | Bus fleet |
| `students` | 10 | Student records |
| `bus_locations` | 1000+ | GPS history |
| `student_attendance` | 500+ | Boarding/alighting logs |
| `notifications` | 100+ | Alert history |
| `routes` | 5 | Bus routes |

---

## Deployment Checklist

- [ ] Set `DEBUG = False`
- [ ] Configure SECRET_KEY
- [ ] Setup PostgreSQL database
- [ ] Install Redis for caching
- [ ] Configure SSL/HTTPS
- [ ] Setup Gunicorn or Daphne
- [ ] Configure Nginx reverse proxy
- [ ] Setup domain name
- [ ] Configure API keys (Google, Twilio, Firebase)
- [ ] Setup backup system
- [ ] Setup monitoring/logging
- [ ] Test all endpoints
- [ ] Load testing

---

This structure provides a scalable, maintainable foundation for your student transportation system!
