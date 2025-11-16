# Safari Salama - Deployment & Configuration Guide

## 🌐 Repository Information

**Repository**: https://github.com/Tania-1111/safari_salama
**Status**: Public (Accessible to all)
**Branch**: main (default)

## ✅ Latest Changes Pushed

### Commit: fede991 (Latest)
- Add comprehensive project documentation and setup guide

### Commit: b78737f
- Merge remote repository with local changes

### Commit: 954e759
- Add .gitignore file for clean repository

### Commit: 5ef6af5
- **Add automatic attendant connection for guardian messaging**
- **Add Message model for direct messaging**
- **Add messaging API endpoints**
- **Add bus attendant API endpoint**

## 🚀 Quick Start Guide

### Local Development Setup

```bash
# 1. Clone the repository
git clone https://github.com/Tania-1111/safari_salama.git
cd safari_salama

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# or
source venv/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage_app.py migrate --run-syncdb

# 5. Create demo data (optional)
python setup_demo_users.py

# 6. Start the server
python manage_app.py runserver 0.0.0.0:8001
```

**Access**: http://localhost:8001

## 📋 Key Implementation Details

### 1. Automatic Attendant Connection System
The guardian messaging feature now automatically connects guardians to their child's bus attendant:

- **File**: `schooltransport/templates/guardian/landing.html`
- **Function**: `loadAttendants()` - Fetches attendant based on student's bus
- **API**: `/api/bus/<bus_id>/attendant/` - Returns attendant information
- **Behavior**: Auto-selects attendant without user intervention

### 2. Messaging Infrastructure
- **Model**: `Message` (schooltransport/models.py)
  - Fields: sender, recipient, bus, message_text, timestamp, is_read, read_at
  - Table: `messages`

- **Endpoints**:
  - `POST /messages/send/` - Send message
  - `GET /messages/get/` - Retrieve conversation
  - `GET /api/bus/<bus_id>/attendant/` - Get bus attendant

- **JavaScript**: Auto-refresh every 3 seconds, auto-read functionality

### 3. Database Schema
```sql
-- Message table structure
CREATE TABLE messages (
  id INTEGER PRIMARY KEY,
  sender_id INTEGER NOT NULL,
  recipient_id INTEGER NOT NULL,
  bus_id INTEGER,
  message_text TEXT NOT NULL,
  timestamp DATETIME AUTO_NOW_ADD,
  is_read BOOLEAN DEFAULT False,
  read_at DATETIME NULL
);
```

## 🔒 Security Configuration

### CSRF Protection
- Enabled by default in Django
- All POST requests require CSRF token
- Token obtained via `getCookie('csrftoken')`

### Authentication
- Role-based access control (RBAC)
- 4 user roles: guardian, attendant, driver, admin
- @login_required decorator on protected views

### API Security
- JSON content type validation
- User ownership validation
- Exception handling with proper error responses

## 📊 Data Models Overview

### Message Model
```python
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True)
    message_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
```

### Bus Model (Relevant Fields)
```python
class Bus(models.Model):
    attendant = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True,
                                      limit_choices_to={'profile__user_type': 'attendant'},
                                      related_name='attended_bus')
```

## 🧪 Testing the Messaging Feature

### 1. Setup Test Data
```bash
python setup_demo_users.py
```

### 2. Login as Guardian
- Username: `guardian1`
- Password: `password123`

### 3. Navigate to Guardian Dashboard
- URL: `http://localhost:8001/guardian/`

### 4. Check Automatic Attendant Connection
- The system should automatically load the attendant for the guardian's child's bus
- Display: "Connected to: [Attendant Name]"

### 5. Send a Test Message
- Type in the message input field
- Click "Send" button
- Message should appear in the conversation

### 6. Switch to Attendant Account
- Login as `attendant1`
- Navigate to attendant landing
- Should see incoming message from guardian

## 🐛 Troubleshooting

### Issue: "No attendant available to message"
**Cause**: Bus has no attendant assigned
**Solution**: 
1. Login as admin
2. Go to `/admin/buses/`
3. Assign an attendant to the bus
4. Refresh guardian page

### Issue: Messages not loading
**Cause**: API endpoint not found or authentication issue
**Solution**:
1. Verify `/api/bus/<bus_id>/attendant/` is in urls.py
2. Check server logs for errors
3. Ensure user is authenticated
4. Clear browser cache

### Issue: Date format error in student status
**Cause**: Using time format on DateField
**Solution**: Already fixed - use `{{ today|date:"M d, Y" }}` format only

## 📦 Requirements Overview

Key dependencies installed:
- Django==4.2.7
- djangorestframework==3.14.0
- Daphne==4.0.0
- psycopg2-binary (PostgreSQL support)
- python-decouple (Environment variables)

Full list in: `requirements.txt`

## 🌍 Deployment Checklist

### Pre-Deployment
- [ ] All migrations applied (`python manage_app.py migrate`)
- [ ] Static files collected (`python manage_app.py collectstatic`)
- [ ] Environment variables configured
- [ ] Database backups taken
- [ ] Tests passing (`python manage_app.py test`)

### Production Settings
- [ ] `DEBUG = False` in settings
- [ ] `ALLOWED_HOSTS` configured
- [ ] `SECRET_KEY` changed to secure value
- [ ] HTTPS enabled
- [ ] Database switched to PostgreSQL
- [ ] Static files served via CDN or whitenoise
- [ ] Error logging configured

### Post-Deployment
- [ ] Health check endpoint verified
- [ ] API endpoints tested
- [ ] Messaging functionality tested
- [ ] Biometric enrollment tested
- [ ] Location tracking verified

## 📚 API Documentation

### Get Bus Attendant
```
GET /api/bus/{bus_id}/attendant/

Response (Success):
{
  "success": true,
  "attendant": {
    "id": 3,
    "name": "John Attendant",
    "phone": "+1234567890"
  }
}

Response (No Attendant):
{
  "success": false,
  "error": "No attendant assigned to this bus"
}
```

### Send Message
```
POST /messages/send/

Body:
{
  "recipient_id": 3,
  "message_text": "Hello attendant",
  "bus_id": 1
}

Response:
{
  "success": true,
  "message": "Message sent successfully",
  "message_id": 42
}
```

### Get Messages
```
GET /messages/get/?recipient_id=3

Response:
{
  "success": true,
  "messages": [
    {
      "id": 42,
      "sender_id": 2,
      "sender_name": "Jane Guardian",
      "recipient_id": 3,
      "message_text": "Hello",
      "timestamp": "2025-11-16T17:45:00Z",
      "is_read": true
    }
  ]
}
```

## 🔄 Git Workflow

### Recent Commits
```
fede991 - Add comprehensive project documentation and setup guide
b78737f - Merge remote repository
954e759 - Add .gitignore file
5ef6af5 - Add automatic attendant connection for guardian messaging
```

### Pushing Changes
```bash
# View status
git status

# Stage changes
git add .

# Commit
git commit -m "Your commit message"

# Push to GitHub
git push origin main
```

## 📞 Support & Issues

- **GitHub Issues**: https://github.com/Tania-1111/safari_salama/issues
- **Repository**: https://github.com/Tania-1111/safari_salama
- **Branch**: main (default)
- **Visibility**: Public

## ✨ Features Implemented

### ✅ Completed
1. Role-based user authentication (Guardian, Attendant, Driver, Admin)
2. Real-time bus location tracking with Google Maps
3. Biometric fingerprint enrollment and verification
4. Student attendance tracking (boarding/alighting)
5. Guardian-Attendant direct messaging with auto-selection
6. Student real-time status GUI with boarding indicators
7. Trip history and reports
8. Notification system
9. Route management
10. Admin dashboard

### 🚀 Future Enhancements
- Mobile app development
- Advanced analytics and reporting
- SMS/Push notifications
- WhatsApp integration
- Multi-language support
- Payment gateway integration
- Parental control features

---

**Last Updated**: November 16, 2025
**Repository Status**: Public and Ready to Use
**Deployment Status**: Ready for Local Development & Production
