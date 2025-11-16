# Safari Salama - School Transport Management System

## 🚀 Project Overview

Safari Salama is a comprehensive school transport management system that combines real-time GPS tracking, biometric attendance verification, and guardian-attendant communication.

### Features

#### 👨‍👩‍👧 Guardian Features
- Real-time student bus location tracking on interactive maps
- Student boarding/alighting status from biometric devices
- Direct messaging with bus attendants
- Trip history and attendance reports
- Automatic attendant connection based on student's bus assignment

#### 🚌 Attendant Features
- Real-time bus tracking
- Student attendance verification via fingerprint biometrics
- Messaging with guardians
- Trip management and history

#### 🚗 Driver Features
- Route navigation
- Real-time location updates
- Trip history
- Route information display

#### 👨‍💼 Admin Features
- Student management
- Bus fleet management
- User account management
- Attendance report generation
- System-wide analytics

## 🛠️ Tech Stack

- **Backend**: Django 4.2.7 with Django REST Framework
- **Server**: Daphne 4.0.0 (ASGI)
- **Database**: SQLite3 (development) / PostgreSQL (production ready)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript with AJAX
- **Biometric**: Fingerprint enrollment and verification system
- **Real-time Tracking**: WebSocket support via Daphne

## 📦 Installation

### Prerequisites
- Python 3.8+
- Virtual Environment (venv)
- pip package manager

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Tania-1111/safari_salama.git
   cd safari_salama
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\Activate.ps1
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage_app.py migrate --run-syncdb
   ```

5. **Setup demo data (optional)**
   ```bash
   python setup_demo_users.py
   python enroll_demo_fingerprints.py
   ```

6. **Start the development server**
   ```bash
   python manage_app.py runserver 0.0.0.0:8001
   ```

   Access the application at: `http://localhost:8001`

## 🔐 Authentication

### Default Demo Users

After running `setup_demo_users.py`, use these credentials:

- **Guardian**: 
  - Username: `guardian1`
  - Password: `password123`

- **Attendant**:
  - Username: `attendant1`
  - Password: `password123`

- **Driver**:
  - Username: `driver1`
  - Password: `password123`

- **Admin**:
  - Username: `admin1`
  - Password: `password123`

## 📁 Project Structure

```
safari_salama/
├── schooltransport/          # Main Django app
│   ├── models.py             # Database models
│   ├── views.py              # View logic and API endpoints
│   ├── urls.py               # URL routing
│   ├── serializers.py        # DRF serializers
│   ├── biometric.py          # Fingerprint processing
│   ├── migrations/           # Database migrations
│   ├── templates/            # HTML templates by role
│   │   ├── guardian/         # Guardian role templates
│   │   ├── attendant/        # Attendant role templates
│   │   ├── driver/           # Driver role templates
│   │   └── admin/            # Admin role templates
│   └── static/               # CSS and JavaScript
├── frontend/                 # React frontend (optional)
├── manage_app.py            # Django management script
├── requirements.txt         # Python dependencies
└── db.sqlite3              # SQLite database
```

## 🔄 Key API Endpoints

### Authentication
- `POST /register/` - User registration
- `POST /login/` - User login
- `GET /logout/` - User logout

### Guardian APIs
- `GET /guardian/` - Guardian dashboard
- `GET /guardian/student/<id>/status/` - Student real-time status
- `GET /guardian/trips/` - Trip history

### Messaging APIs
- `POST /messages/send/` - Send message to attendant
- `GET /messages/get/` - Get conversation with attendant
- `GET /api/bus/<bus_id>/attendant/` - Get attendant for a bus

### Biometric APIs
- `POST /biometric/enroll/` - Enroll student fingerprint
- `POST /biometric/verify/` - Verify fingerprint
- `GET /biometric/scanner/` - Fingerprint scanner interface

### Attendance APIs
- `POST /attendance/checkin/` - Student check-in (biometric)
- `POST /attendance/checkout/` - Student check-out (biometric)

### Bus Location APIs
- `POST /driver/location/update/` - Update bus GPS location
- `GET /driver/bus/<bus_id>/route/` - Get bus route information

## 📊 Database Models

### Core Models
- **User** - Django built-in user model
- **UserProfile** - Extended user information (role, phone, address)
- **School** - School information
- **Bus** - Bus fleet information
- **Student** - Student information linked to bus and guardian
- **StudentAttendance** - Daily boarding/alighting records
- **BusLocation** - Real-time GPS coordinates
- **Message** - Guardian-Attendant direct messaging

### Biometric Models
- **BiometricEnrollment** - Student fingerprint templates
- **BiometricLog** - Fingerprint scan attempts and results

### Administrative Models
- **Route** - Bus routes
- **RouteStop** - Individual route stops
- **Notification** - System notifications to users

## 🔐 Security Features

- Role-based access control (RBAC)
- CSRF protection
- Session-based authentication
- Secure password hashing
- Input validation and sanitization
- API endpoint protection with `@login_required`

## 🌐 Making Repository Public

The repository is already configured as public. You can verify this by:

1. Visit: https://github.com/Tania-1111/safari_salama
2. Check the repository settings for visibility status
3. The code is accessible to all users

## 📝 Recent Features Added

### Automatic Attendant Connection (Latest)
- Guardians are now automatically connected to their child's bus attendant
- No manual attendant selection required
- Seamless messaging experience
- Auto-loads previous conversation history

### Real-time Student Status
- Beautiful GUI displaying student boarding status
- Live data from fingerprint biometric device
- Biometric confidence score display
- Last updated timestamp

### Messaging System
- Direct communication between guardians and attendants
- Auto-read message marking
- 3-second message refresh for real-time updates
- Message persistence in database

## 🧪 Testing

Run the test suite:
```bash
python manage_app.py test
```

Run specific test file:
```bash
python test_checkin_flow.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 📧 Support

For issues and questions, please use the GitHub Issues page:
https://github.com/Tania-1111/safari_salama/issues

## 🙏 Acknowledgments

- Django community
- DRF (Django REST Framework)
- Daphne ASGI server
- All contributors

---

**Last Updated**: November 16, 2025
**Version**: 1.0.0
