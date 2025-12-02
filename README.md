# Nepal's Care Clinic Management System

A comprehensive Django-based clinic management platform designed for seamless healthcare operations, featuring appointment booking, video consultations, medical records management, and real-time communication.

![System Overview](https://img.shields.io/badge/Django-5.2.1-green) ![Python](https://img.shields.io/badge/Python-3.12.2-blue) ![License](https://img.shields. io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

- [Features Overview](#features-overview)
- [System Architecture](#system-architecture)
- [Getting Started](#getting-started)
- [User Roles &amp; Permissions](#user-roles--permissions)
- [Core Workflows](#core-workflows)
- [Technical Stack](#technical-stack)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

---

## 🚀 Features Overview

### 🏥 **Core Healthcare Features**

- **Appointment Management**: Complete booking, scheduling, and management system
- **Video Consultations**: WebRTC-powered real-time video calls
- **Medical Records**: Comprehensive patient medical history and documentation
- **Lab Reports**: Parameter-based reporting with normal/abnormal status tracking
- **Prescription Management**: Medicine scheduling with adherence tracking
- **Real-time Chat**: Socket-based instant messaging between all user types

### 📊 **Administrative Features**

- **Multi-role Dashboard**: Role-specific dashboards with analytics and insights
- **Activity Logging**: Comprehensive audit trail of all system actions
- **User Management**: Complete user lifecycle management with verification
- **Schedule Management**: Advanced calendar-based availability management
- **Document Management**: Secure file upload and management system
- **Payment Integration**: QR code-based payment system

### 🔒 **Security & Compliance**

- **Email Verification**: Required for all new patient registrations
- **Role-based Access Control**: Granular permissions for each user type
- **UUID-based IDs**: Privacy-focused non-sequential identifiers
- **Activity Auditing**: Complete logging of sensitive operations
- **Account Management**: Activation/deactivation controls

---

## 🏗️ System Architecture

### User Roles Hierarchy

```
👑 Admin
├── 🏢 Management Team
├── 👨‍⚕️ Doctors
└── 🏥 Patients
```

### Core Data Models

```
User (Django Authentication)
│
├── Profile (role-based: admin/management/doctor/patient)
│   ├── MedicalInfo (patient-specific)
│   ├── DoctorProfile (professional details)
│   └── Documents (patient uploads)
│
├── Appointment System
│   ├── Appointment (booking records)
│   ├── AppointmentDateSlot (doctor availability)
│   └── AppointmentTimeSlot (specific time slots)
│
├── Medical Records
│   ├── Prescription (medicine management)
│   ├── PrescriptionSchedule (dosage timing)
│   ├── LabReport (test results)
│   └── LabReportParameter (individual test values)
│
├── Communication
│   ├── Conversation (chat rooms)
│   ├── Message (text/file/system notifications)
│   └── Calls (video/audio sessions)
│
└── System Tracking
    ├── Review (patient feedback)
    ├── ActivityLog (audit trail)
    └── Medicine (drug database)
```

---

## 🚦 Getting Started

### Prerequisites

- Python 3.12+
- pip (Python package manager)
- Git

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/0luv69/ClinicMng. git
   cd ClinicMng
   ```
2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Settings**
   Navigate to `clinic/clinic_base/settings.py` and update:

   ```python
   # Domain Configuration
   DOMAIN_NAME = "http://localhost:8000"

   # Email Configuration (Gmail recommended)
   EMAIL_HOST_USER = "your-email@example. com"
   EMAIL_HOST_PASSWORD = "your-app-password"  # Use App Password for Gmail

   # Time Zone
   TIME_ZONE = "Asia/Kathmandu"  # Adjust to your timezone
   ```
4. **Database Setup**

```bash
   python manage.py makemigrations
   python manage. py migrate
   python manage.py createsuperuser
```

5. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```
6. **Access the Application**

   - Main Application: `http://localhost:8000`
   - Admin Panel: `http://localhost:8000/admin`

---

## 👥 User Roles & Permissions

### 👑 **Admin**

- **Full System Access**: Complete Django admin interface access
- **User Management**: Create and manage Management Team accounts
- **System Oversight**: View all activity logs and system analytics
- **Data Control**: Full CRUD operations on all models

### 🏢 **Management Team**

- **Dashboard Access**: Comprehensive management portal with analytics
- **Patient Management**: Complete patient lifecycle (create, edit, activate/deactivate)
- **Doctor Management**: Doctor account creation and profile management
- **Appointment Control**: Confirm, cancel, reschedule appointments
- **Medical Records**: Add, edit, delete prescriptions and lab reports
- **Payment Processing**: Manual payment verification via QR codes
- **Medicine Database**: Add new medicines to system catalog
- **Communication**: Message any user except admin

### 👨‍⚕️ **Doctor**

- **Schedule Management**: Set availability using calendar interface
  - Weekly grid view with drag-and-drop functionality
  - Quick presets (Full Day, Morning Shift, Evening Shift)
  - Break configuration (lunch, evening breaks)
- **Appointment Management**: View, reschedule, cancel, confirm appointments
- **Patient Care**: Access complete medical records for all patients
- **Consultation Tools**:
  - Real-time video calls with patients
  - Chat messaging system
  - Quick notes during consultations
- **Medical Documentation**: Submit prescription and lab report requests
- **Multiple View Options**: Timeline, list, and calendar views for appointments

### 🏥 **Patient**

- **Self-Registration**: Account creation with email verification
- **Appointment Booking**:
  - Select doctor by specialization
  - Choose date, time, and appointment type
  - Upload supporting documents
  - Receive QR code for payment
- **Medical Records Access**: View prescriptions, lab reports, medical history
- **Document Management**: Upload and organize personal medical documents
- **Communication**: Chat with doctors and management team
- **Video Consultations**: Join scheduled video appointments
- **Prescription Management**:
  - View active medications
  - Track daily medicine schedule
  - Access prescription history
- **Export Features**: Download appointments as Excel files

---

## 🔄 Core Workflows

### 1. **Patient Registration & Onboarding**

```mermaid
graph LR
A[Create Account] --> B[Email Verification]
B --> C[Profile Completion]
C --> D[Medical Info Entry]
D --> E[Account Activated]
```

### 2. **Appointment Booking Process**

```mermaid
graph LR
A[Select Doctor] --> B[Choose Date/Time]
B --> C[Provide Reason/Files]
C --> D[Receive QR Code]
D --> E[Payment Confirmation]
E --> F[Appointment Confirmed]
```

### 3. **Medical Consultation Workflow**

```mermaid
graph LR
A[Patient Joins] --> B[Video Consultation]
B --> C[Doctor Notes]
C --> D[Prescription Request]
D --> E[Management Processing]
E --> F[Patient Notification]
```

### 4. **Real-time Communication**

- **WebSocket Integration**: Instant messaging across all user types
- **Video Calls**: WebRTC-powered video consultations
- **System Notifications**: Automated messages for appointments and updates
- **File Sharing**: Document sharing within chat conversations

---

## 🛠️ Technical Stack

### **Backend Technologies**

- **Framework**: Django 5.2.1
- **Language**: Python 3.12.2
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Real-time**: Django Channels with WebSocket support
- **ASGI Server**: Daphne for production deployment

### **Frontend Technologies**

- **Templates**: Django Template Engine
- **Styling**: Tailwind CSS for responsive design
- **JavaScript**: Vanilla JS with modern ES6+ features
- **Calendar**: Flatpickr for date/time selection
- **Video**: WebRTC for peer-to-peer communication

### **Key Dependencies**

```
Django==5.2.1
channels==4.0.0
daphne==4.0.0
django-tailwind==3.6.0
django-multiselectfield==0. 1.12
Pillow==10.0.0
```

### **Security Features**

- **HTTPS Enforcement**: Secure connection requirements
- **CORS Policies**: Cross-origin request protection
- **UUID Fields**: Privacy-focused non-sequential IDs
- **Password Hashing**: Django's secure password storage
- **Email Verification**: Required for account activation

---

## 📱 User Interface Overview

### **Home Page Features**

- Hero section with system introduction
- Department and doctor showcase
- Patient testimonials and feedback
- Quick access navigation

### **Dashboard Layouts**

- **Patient Portal**: Appointment overview, medical summaries, quick actions
- **Doctor Dashboard**: Today's schedule, patient summaries, quick stats
- **Management Portal**: System analytics, appointment management, user oversight
- **Admin Panel**: Complete system administration interface

### **Responsive Design**

- Mobile-first approach
- Tablet and desktop optimized layouts
- Touch-friendly interface elements
- Accessibility compliance

---

## 🔧 Advanced Features

### **Calendar & Scheduling**

- **Interactive Calendar**: Drag-and-drop schedule management
- **Multi-view Support**: Timeline, list, and calendar views
- **Availability Management**: Set breaks, holidays, and working hours
- **Conflict Resolution**: Prevents double-booking automatically

### **Medical Records Management**

- **Lab Reports**: Parameter-based results with reference ranges
- **Prescription Tracking**: Dosage schedules with adherence monitoring
- **Document Storage**: Secure file uploads with format validation
- **Medical History**: Comprehensive patient timeline

### **Communication System**

- **Real-time Messaging**: Instant chat with typing indicators
- **File Sharing**: Document and image sharing within chats
- **Video Consultations**: HD video calls with screen sharing
- **Notification System**: Email and in-app notifications

### **Analytics & Reporting**

- **Dashboard Analytics**: Appointment trends and user statistics
- **Activity Logging**: Comprehensive audit trail
- **Export Features**: Data export in Excel and PDF formats
- **Performance Metrics**: System usage and performance tracking

---

## 🚀 Deployment Guide

### **Production Setup**

1. **Environment Configuration**

   ```bash
   export DEBUG=False
   export ALLOWED_HOSTS="your-domain.com"
   export DATABASE_URL="postgresql://user:pass@localhost/dbname"
   ```
2. **Static Files Collection**

   ```bash
   python manage.py collectstatic
   ```
3. **ASGI Server Configuration**

   ```bash
   daphne -b 0.0.0. 0 -p 8000 clinic.asgi:application
   ```

### **Nginx Configuration Example**

```nginx
server {
    listen 80;
    server_name your-domain.com;
  
    location /static/ {
        alias /path/to/your/staticfiles/;
    }
  
    location /media/ {
        alias /path/to/your/media/;
    }
  
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🔍 API Documentation

### **Authentication Endpoints**

- `POST /accounts/signup/` - Patient registration
- `POST /accounts/login/` - User authentication
- `POST /accounts/verify/` - Email verification
- `POST /accounts/password-reset/` - Password reset

### **Appointment Management**

- `GET /api/appointments/` - List user appointments
- `POST /api/appointments/book/` - Book new appointment
- `PUT /api/appointments/{id}/reschedule/` - Reschedule appointment
- `DELETE /api/appointments/{id}/cancel/` - Cancel appointment

### **Medical Records**

- `GET /api/medical-records/` - Patient medical history
- `GET /api/prescriptions/` - Active prescriptions
- `GET /api/lab-reports/` - Lab test results
- `POST /api/documents/upload/` - Upload medical documents

---

## 🤝 Contributing

We welcome contributions to improve Nepal's Care!  Here's how you can help:

### **Getting Started**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### **Development Guidelines**

- Follow Django coding standards
- Write comprehensive tests for new features
- Update documentation for any API changes
- Ensure responsive design compatibility
- Test across different user roles

### **Areas for Contribution**

- [ ] Mobile application development
- [ ] Payment gateway integration
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Automated testing suite
- [ ] Docker containerization

---

## 📞 Support & Contact

### **Technical Support**

- **Email**: support@nepalscare.com
- **Documentation**: [Wiki Pages](https://github.com/0luv69/ClinicMng/wiki)
- **Issues**: [GitHub Issues](https://github.com/0luv69/ClinicMng/issues)

### **Community**

- **Discussions**: [GitHub Discussions](https://github.com/0luv69/ClinicMng/discussions)
- **Contributors**: [Contributors Page](https://github.com/0luv69/ClinicMng/graphs/contributors)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Django Community** for the excellent framework
- **Tailwind CSS** for the utility-first styling approach
- **WebRTC** community for real-time communication protocols
- **Open Source Contributors** who inspire continuous improvement

---

## 🗺️ Roadmap

### **Version 2.0 (Planned)**

- [ ] Mobile application (React Native/Flutter)
- [ ] Advanced appointment scheduling algorithms
- [ ] Integration with major payment gateways
- [ ] Multi-clinic support
- [ ] Advanced reporting and analytics
- [ ] Telemedicine compliance features

### **Version 1. 5 (In Progress)**

- [ ] Docker containerization
- [ ] Automated testing suite
- [ ] Performance optimizations
- [ ] Enhanced security features
- [ ] Multi-language support

---

**Built with ❤️ for healthcare professionals and patients in Nepal and beyond.**
