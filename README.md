# Nepal's Care Clinic Management System – Project Overview & Architecture

This high-level documentation summarizes the Django-based Nepal's Care system: its user roles, main features, data models, panel/page structure, and core workflows. This serves as a quick reference for onboarding, handover, or further development.

---

## System Purpose

A comprehensive clinic management platform for appointment booking, video consultations, medical records, and workflow management, with clear role separation and robust data tracking.

---

## How to start

1: Clone the Repository Setps:

- A: Open desired Terminal [Terminal (Linux/Mac) or Command Prompt/PowerShell (Windows)]
- B: Navigate to the directory where you want to keep the project:


  ```bash
  cd path/here/
  ```
- C: Run the clone command:

  ```bash
  git clone https://github.com/0luv69/ClinicMng.git
  ```
- D: Go into the cloned project folder:

  ```bash
  cd ClinicMng
  ```

2: Requirements install:
Make sure you have Python 3 and pip installed. Then run:

```python
pip install -r requirements.txt
```

3: Configure Django Settings:

    3.1:**Navigate to**:

```bash
cd clinic/clinic_base/
```

    &`open setting.py`

    3.2:**Update the following**:

* **Change Domain Name**

```python
DOMAIN_NAME = "http://localhost:8000"
```

*     **Email Configuration**

    At the end of the file, replace:

```python
EMAIL_HOST_USER = "your-email@example.com"
EMAIL_HOST_PASSWORD = "your-app-password"
```

    with your own email credentials (use Google App Password if using Gmail).

*     **Time Zone**:
  	   Set your correct time zone:

```python
TIME_ZONE = "Asia/Kathmandu"
```

---

## User Roles & Permissions

**Admin**

- Full access via Django admin to all models and operations.
- Main function: system setup and Management Team account management.

**Management Team**

- Management dashboard with full CRUD access to Patients, Doctors, Appointments, Prescriptions, Lab Reports, and Medicines.
- Responsible for confirming/canceling appointments, managing manual payment, and formalizing prescriptions/reports from doctor notes.
- Can deactivate/reactivate users (`is_active`), add new medicines (cannot edit/delete medicines).
- Can message any user (except admin).

**Doctor**

- Doctor dashboard with schedule editing (calendar UI, week grid, quick presets, breaks).
- Can toggle all availability statuses except "booked" (booked slots are locked).
- "View Appointment" page: see/filter appointments (timeline, week view, list), reschedule/cancel/confirm (now for both pending and confirmed).
- "View Patient" page: list patients and reschedule appointments.
- Can access any patient’s full medical info (via unique username or "View Medical Records" button).
- Messaging: can request/initiate chat with any patient (patient must accept), see system messages in chat.
- Can join/initiate video calls (WebRTC).
- Cannot edit or delete medical info, prescriptions, or lab reports after entry.

**Patient**

- Patient portal/dashboard for appointment booking, document uploads, lab results, prescriptions, and ID card.
- Two onboarding paths: management-created or self-signup (email verification required).
- Book appointments (doctor, date/time, type, reason, file upload), receive QR code for manual payment.
- Can export appointments to Excel, download documents and lab reports (not prescriptions).
- Can message doctors/management, request chat, and join/request video calls.
- Can view/print/download ID card.
- Can update own info and password.
- Only one appointment per doctor per time slot.
- Receives notifications via email and chat.

---

## Core Features & Workflows

1. **User Onboarding & Profile Management**

   - Admin creates Management Team; Management creates/approves Doctor & Patient accounts.
   - Access controlled by `is_active` and `is_verified`.
2. **Scheduling & Appointments**

   - Doctors set weekly availability; patients book by doctor/date/time/type.
   - Statuses: pending, confirmed, cancelled, completed.
   - Appointments reschedulable by doctor (pending/confirmed, both in View Appointment and View Patient).
   - QR code sent for payment; handled manually by management.
3. **Consultations (Chat & Video Call)**

   - Real-time, role-based chat (WebSocket); system messages integrated.
   - Video/audio calls (WebRTC), linked to appointments or ad hoc.
   - Chat/call rooms use Conversation model.
4. **Medical Records & Reports**

   - Doctors submit quick notes; management formalizes as prescriptions/reports (edit/delete allowed for management).
   - Patients notified on report/prescription upload/edit.
   - Patients can download lab reports/documents.
5. **Document Management**

   - Patients upload/access documents (flat list, no folders).
   - Doctor/management can view all patient documents.
6. **Analytics & Logging**

   - Management dashboard: summary cards, graphs (appointments by type).
   - ActivityLog for key user actions (not universal).
7. **Reviews**

   - Patients rate/review doctors.

---

## Main Data Models & Relationships

```
User (Django)
   |
   └─ Profile (role: admin/management/doctor/patient)
            |
            ├─ MedicalInfo (patient)
            ├─ DoctorProfile (doctor)
            ├─ Documents (patient uploads)
            |
            └─ Appointment (patient, doctor, slot, status)
                     |
                     └─ AppointmentDateSlot (doctor, date)
                             |
                             └─ AppointmentTimeSlot (times, status)
            |
            └─ Prescription (doctor, patient, medicine, status)
                     |
                     └─ PrescriptionSchedule (time, adherence)
            |
            └─ LabReport (doctor, patient, type, status)
                     |
                     └─ LabReportParameter (test, result)
            |
            └─ Conversation (many-to-many: doctor, patient, management)
                     |
                     ├─ Message (text/file/system event)
                     └─ Calls (audio/video, optional appointment link)
            |
            └─ Review (patient → doctor)
            |
            └─ ActivityLog (user actions)
```

---

## UI: Panel & Page Structure

- **Home Page:** Hero/intro, feature boxes, departments, doctors, feedback. Navbar (CAT, profile, ID card).
- **Patient Panel:** Dashboard, appointments (view/book/cancel/export), document mgmt (upload/download), messaging, video call, prescriptions, lab reports, profile/ID card.
- **Doctor Panel:** Dashboard (summary/filter), edit schedule (week grid), "View Appointment" (filter/list/timeline, reschedule/cancel/confirm), "View Patient" (list + reschedule), messaging, video call, profile, view medical info.
- **Management Portal:** Dashboard (cards/graphs), appointments (view/edit), patients/doctors (view/edit/activate/deactivate), prescriptions/lab reports (view/add/edit/delete), medicines (view/add), messaging.
- **Admin Panel:** Standard Django admin (all models).

---

## System Rules & Notes

- Only one patient per doctor per slot; no overlapping bookings.
- All notifications via email and chat; no in-app notification center.
- Manual payment verification using QR code.
- Responsive design for all panels.
- Role-based edit/delete restrictions as described.

---

**This overview reflects all current features, panels, and behaviors of Nepal's Care as described. Ready for further onboarding, handover, or feature expansion.**

# Nepal's Care Clinic Management System – Technical & Operational Overview

This document supplements the project architecture overview with detailed technical information, operational practices, and development environment notes.

---

## 1. Tech Stack & Infrastructure

**Languages & Frameworks**

- Python 3.12.2
- Django 5.2.1

**Dependencies**

- See `requirements.txt` for full list.
- Notable: `channels` (for WebSocket support), `django-multiselectfield`, `django-tailwind`, `daphne` (ASGI server).

**Frontend**

- Django templates with JavaScript and Tailwind CSS.
- Calendar UI leverages [flatpickr](https://flatpickr.js.org/) via CDN.

**Database**

- SQLite (single database, local development).

**Real-time & Communication**

- WebSocket support via Django Channels (using `channels.layers.InMemoryChannelLayer`).
- WebRTC for peer-to-peer video calls.
- Email sending via Django’s built-in email support.

**File Handling**

- Django `MEDIA_ROOT` for file uploads (documents, reports, etc.). Running with `DEBUG = False` for production-like file handling.

---

## 2. Deployment & Environments

- **Current State:** Not deployed; project is a final-year project running locally.
- **Planned Deployment:** Direct server hosting planned (no Docker or cloud CI/CD currently).
- **Static/Media Files:** Intention to use Nginx for media/static file serving in production or fall back to Django’s static file serving for simplicity.

---

## 3. Testing & Quality

- No formal test framework (like pytest or Selenium) in use.
- Relies on Django’s built-in test features and extensive manual testing of all user flows and edge cases.
- No automated CI/CD or linting tools currently set up.

---

## 4. Security & Privacy

- **HTTPS enforced** via Django settings; CORS policies applied.
- **Password storage:** Django’s default (hashed, salted).
- **Sensitive data:** All user-facing models use UUID fields for IDs to avoid exposing sequential IDs.
- **Verification:** New patient registrations require email verification before account activation.
- **Deactivation:** Management/Admin can set `is_active = False` to suspend any account (except admin).
- **Audit:** Sensitive actions are logged and viewable only by admin.

---

## 5. User & Permission Management

- **Role Assignment:**
  - Default role on signup is patient.
  - Management/Admin create doctor and management accounts.
- **Password Reset & Verification:**
  - Email-based verification and password reset (link valid for 1 hour).
- **Role Change/Account Deletion:**
  - Users must email management to request role changes or account deletion.

---

## 6. Integrations & Extensibility

- No public APIs provided.
- No support for plugins or custom modules.
- No third-party integrations (e.g., payment gateways, EHR) at this time.

---

## 7. Known Limitations & Roadmap

- Local-only setup (no deployment scripts or cloud hosting yet).
- No automated testing, CI/CD, or linting.
- No payment integration; payment is handled manually.
- No public API or extensibility mechanisms.
- SQLite database only (not yet tested on PostgreSQL/MySQL).
- No user-facing notification center (notifications via email/chat only).
- Roadmap items and further limitations to be determined as the project is extended.

---

## 8. User Documentation & Support

- No user manual/FAQ yet; documentation is provided here and in project files.
- For support or bug reports, users are expected to contact management/admin via email.

---

## 9. Miscellaneous

- All sensitive workflows (e.g., deactivation, audit logs) are admin/management-only.
- Video calls and real-time chat are core features, implemented with Channels (WS) and WebRTC.

---

This document ensures any new contributor or user has a comprehensive picture of the technical and operational environment for Nepal’s Care.
