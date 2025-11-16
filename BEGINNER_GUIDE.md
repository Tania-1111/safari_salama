# 🚌 SAFARI SALAMA - STEP-BY-STEP BEGINNER GUIDE

## Complete Instructions for Building Your Student Transportation System

---

## PART 1: Understanding the Project

### What is Safari Salama?

Safari Salama is a student transportation management system for Kenyan schools that:
- Tracks buses in real-time using GPS
- Authenticates students using biometrics (fingerprint or facial recognition)
- Sends instant notifications to parents when students board/alight
- Allows parents to track where their child's bus is located
- Provides school admins with comprehensive reports

### Key Users:

1. **Guardian (Parent)** - Sees bus location and student status
2. **Driver** - Updates GPS location and manages route
3. **Attendant** - Records student boarding/alighting via biometric
4. **School Admin** - Manages students, buses, and reports
5. **Student** - Enrolls biometric data

---

## PART 2: Project Setup (First Time)

### Step 1: Install Python and Dependencies

```bash
# Check Python version (should be 3.9+)
python --version

# Navigate to project
cd c:\Users\USER\Desktop\safariSalama_FD

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 2: Configure Google Maps API

1. Go to https://console.cloud.google.com
2. Create a new project
3. Search for "Maps JavaScript API" and enable it
4. Create an API key
5. Add the key to `schooltransport/setting.py`:

```python
GOOGLE_MAPS_API_KEY = 'YOUR_KEY_HERE'
```

### Step 3: Configure Email (Gmail)

1. Enable "Less secure app access" on your Gmail account
2. Add your email to `setting.py`:

```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Step 4: Setup Database

```bash
# Create database tables
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin account
python manage.py createsuperuser
# Enter username, email, password
```

### Step 5: Create Demo Data

```bash
# Run setup script to create test users
python setup_demo.py

# You should see:
# ✓ Created admin user
# ✓ Created driver user
# ✓ Created school
# ✓ Created bus
# etc...
```

---

## PART 3: Running the Application

### Option A: Using Daphne (With WebSocket Support) ✅ RECOMMENDED

```bash
# Install Daphne if not already installed
pip install daphne

# Run the server
daphne -b 0.0.0.0 -p 8000 schooltransport.asgi:application

# Open browser at http://localhost:8000
```

### Option B: Using Django Development Server (No WebSocket)

```bash
python manage.py runserver

# Open browser at http://localhost:8000
```

---

## PART 4: Testing the Application

### Login Credentials (From Demo Data):

**Administrator:**
```
URL: http://localhost:8000/login/
Username: admin
Password: admin123
```

**Driver:**
```
URL: http://localhost:8000/driver/dashboard/
Username: driver1
Password: driver123
```

**Guardian:**
```
URL: http://localhost:8000/guardian/dashboard/
Username: guardian1
Password: guardian123
```

### Test Workflows:

#### Workflow 1: Guardian Tracking Bus

1. Login as guardian1
2. You should see:
   - List of students on the left
   - Live map showing bus location
   - Bus status information
3. Click on a student to see their bus
4. Map should update automatically every 10 seconds

#### Workflow 2: Driver Updating GPS

1. Login as driver1
2. Click "Start GPS Tracking" button
3. Allow browser to access location
4. GPS coordinates should appear and update
5. Check database: `BusLocation` table should have new entries

#### Workflow 3: Student Biometric Enrollment

1. Go to http://localhost:8000/biometric/enroll/
2. Allow camera access
3. Take a selfie
4. System enrolls your biometric

#### Workflow 4: Student Check-in/out

1. At bus boarding point (attendant):
2. POST to http://localhost:8000/attendance/checkin/
3. Biometric captured and verified
4. If match > 75%, creates attendance record
5. Guardian receives notification

---

## PART 5: Key Code Explanations

### 1. Models (Database Structure)

Located in: `schooltransport/models.py`

```python
# User authentication
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20)  # guardian|driver|admin|etc
    phone_number = models.CharField(max_length=15)

# School information
class School(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    latitude = models.FloatField()  # GPS location
    longitude = models.FloatField()

# Bus tracking
class Bus(models.Model):
    driver = models.OneToOneField(User)
    registration_number = models.CharField(max_length=50)
    current_latitude = models.FloatField()  # Current position
    current_longitude = models.FloatField()
    status = models.CharField(max_length=20)  # active|on_route|at_school

# Bus GPS history
class BusLocation(models.Model):
    bus = models.ForeignKey(Bus)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

# Student attendance
class StudentAttendance(models.Model):
    student = models.ForeignKey(Student)
    status = models.CharField(max_length=20)  # boarded|alighted
    latitude = models.FloatField()  # Where they boarded/alighted
    longitude = models.FloatField()
    biometric_verified = models.BooleanField()  # Confirmed via biometric
    timestamp = models.DateTimeField(auto_now_add=True)

# Notifications
class Notification(models.Model):
    recipient = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
```

### 2. Views (Business Logic)

Located in: `schooltransport/views.py`

```python
# Driver updates GPS location
@csrf_exempt
def update_bus_location(request):
    """
    Receives GPS coordinates from driver's phone
    Saves to database and updates bus current location
    """
    data = json.loads(request.body)
    bus = Bus.objects.get(id=data['bus_id'])
    
    # Save location history
    BusLocation.objects.create(
        bus=bus,
        latitude=data['latitude'],
        longitude=data['longitude'],
        speed=data['speed']
    )
    
    # Update current position
    bus.current_latitude = data['latitude']
    bus.current_longitude = data['longitude']
    bus.save()

# Guardian checks student status
def student_status(request, student_id):
    """
    Returns current status of student's bus
    """
    student = Student.objects.get(id=student_id)
    bus = student.bus
    
    # Get last location
    location = bus.location_history.latest('timestamp')
    
    # Get last attendance
    attendance = student.attendance_logs.latest('timestamp')
    
    return JsonResponse({
        'bus': {
            'registration': bus.registration_number,
            'status': bus.status,
            'location': {
                'latitude': location.latitude,
                'longitude': location.longitude
            }
        },
        'student_status': attendance.status  # boarded|alighted
    })

# Verify biometric and record attendance
@csrf_exempt
def verify_and_checkin(request):
    """
    1. Receives captured biometric
    2. Matches with student's stored template
    3. Creates attendance record if match > 75%
    4. Sends notification to guardian
    """
    data = json.loads(request.body)
    bus = Bus.objects.get(id=data['bus_id'])
    
    # Find matching student (simplified)
    biometric_system = BiometricSystem('fingerprint')
    is_match, confidence = biometric_system.verify_biometric(
        data['biometric_data'],
        student.biometric_template
    )
    
    if is_match and confidence > 75:
        # Record attendance
        StudentAttendance.objects.create(
            student=student,
            bus=bus,
            status='boarded',
            biometric_verified=True,
            biometric_confidence=confidence
        )
        
        # Send notification
        send_notification_to_guardian(
            student,
            f'{student.name} boarded bus {bus.registration}'
        )
```

### 3. Biometric Processing

Located in: `schooltransport/biometric.py`

```python
from schooltransport.biometric import BiometricSystem

# Initialize system
biometric = BiometricSystem(biometric_type='fingerprint')

# 1. ENROLLMENT - Store fingerprint template
def enroll_student():
    # Capture image
    image_from_camera = get_camera_input()  # Base64
    
    # Create template
    template = biometric.enroll_biometric(
        image_data=image_from_camera,
        student_name='John Doe'
    )
    
    # Store in database
    student.biometric_template = template['template']
    student.biometric_enrolled = True
    student.save()

# 2. VERIFICATION - Compare captured with stored
def verify_student():
    # Capture at bus
    captured_image = biometric_scanner.capture()
    
    # Compare with stored
    is_match, confidence = biometric.verify_biometric(
        captured_data=captured_image,
        stored_template=student.biometric_template
    )
    
    # Confidence is 0-100
    # If > 75%, consider it a match
    if is_match and confidence > 75:
        print(f"Match! Confidence: {confidence}%")
    else:
        print("Not recognized")
```

### 4. Notification System

```python
# When student boards, this happens:

def verify_and_checkin(request):
    # ... verification happens ...
    
    # Send notification to guardian
    send_notification_to_guardian(
        student=student,
        message=f'{student_name} has boarded {bus_registration}',
        notification_type='boarded'
    )

def send_notification_to_guardian(student, message, notification_type):
    """
    Sends notification via multiple channels
    """
    guardian = student.guardian
    
    # 1. Save in database
    Notification.objects.create(
        recipient=guardian,
        student=student,
        title='Student Transportation Alert',
        message=message,
        notification_type=notification_type
    )
    
    # 2. Send email
    send_mail(
        subject='Safari Salama Alert',
        message=message,
        from_email='noreply@safarisalama.com',
        recipient_list=[guardian.email]
    )
    
    # 3. Send SMS (if Twilio configured)
    if guardian.profile.phone_number:
        from twilio.rest import Client
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_=TWILIO_NUMBER,
            to=guardian.profile.phone_number
        )
    
    # 4. Send via WebSocket (real-time)
    async_to_sync(channel_layer.group_send)(
        f'user_{guardian.id}',
        {
            'type': 'send_notification',
            'message': message,
            'title': 'Student Alert'
        }
    )
```

### 5. GPS Tracking (Frontend)

Located in: `schooltransport/templates/driver/dashboard.html`

```javascript
// 1. START GPS TRACKING
function startGPSTracking() {
    // Browser's built-in geolocation
    navigator.geolocation.watchPosition(
        (position) => {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            const speed = position.coords.speed * 3.6;  // Convert to km/h
            const heading = position.coords.heading;
            
            // Send to server
            fetch('/driver/location/update/', {
                method: 'POST',
                body: JSON.stringify({
                    bus_id: 1,
                    latitude: lat,
                    longitude: lng,
                    speed: speed,
                    heading: heading
                })
            });
            
            // Update map
            updateMapMarker(lat, lng);
        },
        (error) => console.error(error),
        {
            enableHighAccuracy: true,
            maximumAge: 10000,  // Update every 10 sec
            timeout: 30000
        }
    );
}

// 2. DISPLAY ON MAP
function updateMapMarker(latitude, longitude) {
    // Create/update marker on Google Map
    const busLocation = { lat: latitude, lng: longitude };
    
    if (busMarker) {
        busMarker.setPosition(busLocation);
    } else {
        busMarker = new google.maps.Marker({
            position: busLocation,
            map: map,
            title: 'Bus Location'
        });
    }
    
    // Center map on bus
    map.setCenter(busLocation);
}
```

### 6. Guardian Tracking (Frontend)

Located in: `schooltransport/templates/guardian/dashboard.html`

```javascript
// GUARDIAN SEES LIVE BUS LOCATION

function loadStudents() {
    fetch('/guardian/dashboard/')
        .then(r => r.json())
        .then(data => {
            // Display students
            data.students.forEach(student => {
                addStudentToList(student);
            });
        });
}

function selectStudent(studentId) {
    // Get student's bus info
    fetch(`/guardian/student/${studentId}/status/`)
        .then(r => r.json())
        .then(data => {
            // Show bus info
            document.getElementById('bus-info').innerHTML = `
                Bus: ${data.bus.registration}
                Status: ${data.bus.status}
                Last Update: ${data.bus.current_location.timestamp}
            `;
            
            // Show on map
            const pos = {
                lat: data.bus.current_location.latitude,
                lng: data.bus.current_location.longitude
            };
            map.setCenter(pos);
            updateBusMarker(pos);
        });
}

// Auto-update every 10 seconds
setInterval(() => {
    if (selectedStudentId) {
        selectStudent(selectedStudentId);
    }
}, 10000);
```

---

## PART 6: Database Schema Visualization

```
┌──────────────────────┐
│    Django User       │
│  (Built-in Auth)     │
│ - username           │
│ - email              │
│ - password           │
└──────────┬───────────┘
           │ 1:1
           ▼
┌──────────────────────┐
│   UserProfile        │
│ - user_type          │  ◄─── guardian, driver, admin, etc
│ - phone_number       │
│ - verified           │
└──────────┬───────────┘
           │
  ┌────────┼────────┬──────────────┐
  │        │        │              │
  ▼        ▼        ▼              ▼
 School   Bus    Student       Guardian
  │       │        │              │
  │    ┌──┴──┐     │              │
  │    │     │     │              │
  ▼    ▼     ▼     ▼              ▼
       BusLocation StudentAttendance Notification
```

---

## PART 7: Common Tasks

### Task 1: Add a New Student

```python
from schooltransport.models import Student, School, User
from datetime import date

# 1. Create user
student_user = User.objects.create_user(
    username='newstudent',
    email='student@school.com',
    password='password123'
)

# 2. Create student record
student = Student.objects.create(
    user=student_user,
    school=School.objects.first(),
    guardian=User.objects.get(username='guardian1'),
    bus=Bus.objects.first(),
    registration_number='STU/2024/002',
    date_of_birth=date(2010, 6, 15),
    class_name='Form 1B',
    parent_phone='+254712345678'
)

print(f"Student {student.user.get_full_name()} created")
```

### Task 2: Enroll Student Biometric

```python
from schooltransport.models import Student
from schooltransport.biometric import BiometricSystem

# Get student
student = Student.objects.get(registration_number='STU/2024/001')

# Initialize biometric system
biometric = BiometricSystem('fingerprint')

# Capture image (from webcam or scanner)
image_data = capture_from_device()  # Base64 encoded

# Enroll
result = biometric.enroll_biometric(image_data, student.user.get_full_name())

if result['success']:
    student.biometric_template = result['template']
    student.biometric_enrolled = True
    student.save()
    print("✓ Biometric enrolled")
```

### Task 3: Create Attendance Record

```python
from schooltransport.models import StudentAttendance, Student, Bus

student = Student.objects.get(id=1)
bus = Bus.objects.get(id=1)

# Record student boarding
attendance = StudentAttendance.objects.create(
    student=student,
    bus=bus,
    status='boarded',
    latitude=-1.2865,
    longitude=36.8172,
    biometric_verified=True,
    biometric_confidence=92.5
)

print(f"✓ {student.user.get_full_name()} boarded at {attendance.timestamp}")
```

### Task 4: Get Student's Bus Location

```python
from schooltransport.models import Student

student = Student.objects.get(id=1)
bus = student.bus

# Get latest location
latest_location = bus.location_history.latest('timestamp')

print(f"Bus {bus.registration_number} is at:")
print(f"  Latitude: {latest_location.latitude}")
print(f"  Longitude: {latest_location.longitude}")
print(f"  Speed: {latest_location.speed} km/h")
print(f"  Last updated: {latest_location.timestamp}")
```

---

## PART 8: Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'django'"

**Solution:**
```bash
# Activate virtual environment first
venv\Scripts\activate

# Then install
pip install -r requirements.txt
```

### Problem: "Database locked" error

**Solution:**
```bash
# Delete old database and recreate
del db.sqlite3
python manage.py migrate
```

### Problem: GPS not updating on map

**Solution:**
1. Check browser location permissions
2. Check network connectivity
3. Verify API endpoint is receiving data: Check server logs
4. Ensure Daphne is running (not just runserver)

### Problem: Biometric recognition fails

**Solution:**
1. Ensure good lighting
2. Clean camera lens
3. Adjust confidence threshold (default 75%)
4. Try enrollment again

### Problem: Email notifications not sending

**Solution:**
```python
# Test email configuration
from django.core.mail import send_mail

send_mail(
    'Test',
    'This is a test email',
    'noreply@safarisalama.com',
    ['your_email@example.com'],
    fail_silently=False  # Show errors
)
```

---

## PART 9: Next Steps (Advanced Features)

1. **Optimize GPS Accuracy:**
   - Use Kalman filters
   - Combine with map matching

2. **Machine Learning:**
   - Predict bus delays
   - Optimize routes using ML

3. **Mobile App:**
   - React Native or Flutter app
   - Better biometric hardware integration

4. **Scale to Production:**
   - Use PostgreSQL
   - Deploy on AWS/Google Cloud
   - Setup CI/CD pipeline

5. **Additional Features:**
   - Parent chat with driver
   - Bus maintenance tracking
   - Student behavior logs
   - Emergency alert system

---

## PART 10: Resources

### Official Documentation:
- Django: https://docs.djangoproject.com
- Google Maps API: https://developers.google.com/maps
- Django Channels: https://channels.readthedocs.io
- OpenCV: https://docs.opencv.org

### Communities:
- Django Forum: https://forum.djangoproject.com
- Stack Overflow: Tag "django"
- Python Discord: https://discord.gg/python

### Tools:
- Postman (API Testing): https://postman.com
- DBeaver (Database Management): https://dbeaver.io
- VS Code Extensions: Django, Python, REST Client

---

## Final Checklist

- [ ] Python installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] Google Maps API key configured
- [ ] Email configured
- [ ] Database migrations completed
- [ ] Demo data created
- [ ] Server running (Daphne or runserver)
- [ ] Can login with test credentials
- [ ] Guardian dashboard shows map
- [ ] Driver GPS tracking working
- [ ] Notifications sending

---

**Good luck building your Transportation Management System! 🚌✨**

For support or questions, refer to the README.md file or Django documentation.

