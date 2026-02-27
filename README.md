# 🏥 Gilead Vital Signs  
### Secure Medical Records Application

A secure, privacy-focused medical records web application built for **Winners Chapel International Arlington – Gilead Health Ministry**.  
The system enables encrypted patient record management, visit documentation, and controlled staff access — designed for real-world church health department workflows.

---

## 📸 Application Preview

<p align="center">
  <img src="images/welcome.png" alt="Gilead Vital Signs Welcome Page" width="85%">
</p>

---

## 📋 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [User Guide](#-user-guide)
- [Security & Encryption](#-security--encryption)
- [Database Schema](#-database-schema)
- [File Structure](#-file-structure)
- [Desktop / Offline Use](#-desktop--offline-use)
- [Production Deployment](#-production-deployment)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## ✨ Features

### 🏠 Welcome Page
- Church branding and Gilead Vital Signs identity
- Secure navigation to Patient Records and Staff Administration
- Clean, user-friendly interface for non-technical users

### 🧑‍⚕️ Patient Records Management
- Dual authentication: **Staff credentials + Patient identity**
- First/Last name swap tolerance
- Secure new patient registration
- Graceful “Patient Not Found” handling with guided actions

### 🩺 Visit Documentation
Each visit securely records:

| Vital Sign | Description |
|-----------|------------|
| Weight | Patient weight |
| Temperature | Body temperature |
| Blood Pressure | Systolic / Diastolic |
| Pulse | Heart rate |
| Respiration | Breathing rate |
| Pain Level | 0–10 scale |
| Notes | Clinical observations |

### 👥 Staff Administration
- Admin-only staff management portal
- Unique staff numbers (e.g., `ADMIN001`, `NURSE001`)
- Role-based access control
- Secure staff deletion and privilege assignment

### 🔐 Data Security
- Patient records encrypted using patient credentials
- PBKDF2 key derivation
- Encrypted database storage
- Full audit trail of record access

---

## 🖼️ Screenshots

### Welcome Page
![Welcome Page](images/welcome.png)

### Patient Records & Visit History
![Patient Records](images/patient_records.png)

### Patient Not Found Handling
![Patient Not Found](images/patient_not_found.png)

### Staff Administration
![Staff Administration](images/staff_admin.png)

---

## 📦 Packages & Libraries Used

### 🔧 Core Application
- **Flask** – Lightweight Python web framework for routing, sessions, and request handling
- **Jinja2** – HTML templating engine (bundled with Flask)
- **Werkzeug** – WSGI utilities and security helpers (bundled with Flask)

### 🔐 Security & Encryption
- **cryptography**  
  - Fernet symmetric encryption  
  - PBKDF2 key derivation for credential-based encryption
- **hashlib** *(Python standard library)* – Secure hashing functions
- **secrets** *(Python standard library)* – Cryptographically secure random values
- **os** *(Python standard library)* – Environment variables and filesystem access

### 🗄️ Database
- **sqlite3** *(Python standard library)* – Embedded relational database for offline-first storage

### 🕒 Utilities
- **datetime** *(Python standard library)* – Timestamping and date handling
- **uuid** *(Python standard library)* – Unique identifier generation
- **json** *(Python standard library)* – Structured data serialization

### 🌐 Frontend
- **HTML5 / CSS3** – User interface structure and styling
- **Bootstrap (CSS)** *(via CDN)* – Responsive layout and UI components
- **Font Awesome / Icon Fonts** *(via CDN)* – UI icons and visual indicators

### 🚀 Deployment & Distribution
- **gunicorn** – Production WSGI server for deployment
- **PyInstaller** – Builds standalone desktop executables for offline use

---

## 📄License and Acknowledgments
This application is provided for use by Winners Chapel International Arlington - Gilead Health Ministry.
- Built with Flask (Python web framework)
- SQLite database (free, no setup required)
- Cryptography library for secure encryption
- Designed for healthcare privacy and security
- Can also be Installed as Desktop App using the Guide.md Instructions
- Gilead Vital Signs Medical Records System v1.0
- Designed and maintained by Afamefuna Umejiaku
