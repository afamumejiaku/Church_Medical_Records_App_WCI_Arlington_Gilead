# 🏥 Gilead Vital Signs - Medical Records Web Application

A secure medical web application for Winners Chapel International Arlington - Gilead Health Ministry, featuring encrypted patient records and comprehensive visit documentation.

---

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [User Guide](#-user-guide)
- [Security & Encryption](#-security--encryption)
- [Database Schema](#-database-schema)
- [File Structure](#-file-structure)
- [Troubleshooting](#-troubleshooting)
- [Production Deployment](#-production-deployment)

---

## ✨ Features

### Welcome Page
- Church name and Vital Signs branding
- Quick access links to Patient Records and Staff Administration

### Patient Records Management
- **Secure Access**: Requires both staff authentication AND patient identification
- **Name Swap Tolerance**: System finds patients even if first/last names are entered in reverse order
- **New Patient Registration**: Create records with required fields (first name, last name, DOB, sex, physician)
- **Patient Not Found Handling**: Options to create new record or retry search

### Visit Documentation
For each patient visit, record:

| Vital Sign | Description |
|------------|-------------|
| Date | Visit date |
| Weight | Patient weight (lbs/kg) |
| Temperature | Body temperature (°F/°C) |
| Blood Pressure | Systolic/Diastolic (e.g., 120/80) |
| Pulse | Heart rate (bpm) |
| Respiration | Breathing rate (breaths/min) |
| Pain Level | Scale of 0-10 |
| Notes | Additional observations |

### Staff Administration
- Admin portal for managing staff accounts
- Unique staff numbers for each team member
- Admin privilege assignment
- Staff deletion capability

### Data Encryption
- Patient records encrypted using patient credentials
- Credentials-based key derivation (PBKDF2)
- Data only accessible with correct first name, last name, and DOB

---

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Web browser (Chrome, Firefox, Safari, Edge)

### Step-by-Step Installation

1. **Extract the application files:**
   ```bash
   unzip medical_app.zip
   cd medical_app
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the application:**
   Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

---

## 🚀 Quick Start

### Default Admin Credentials

| Field | Value |
|-------|-------|
| Staff Number | `ADMIN001` |
| Last Name | `Administrator` |

### First-Time Setup

1. **Login to Staff Administration**
   - Click "Staff Admin" on the welcome page
   - Enter default admin credentials above
   - Click "Login as Admin"

2. **Create Staff Accounts**
   - Fill in Staff Number (e.g., `DR001`, `NURSE001`)
   - Enter First Name and Last Name
   - Check "Admin Privileges" if needed
   - Click "Add Staff"

3. **Create Your First Patient**
   - Go to "Patient Records"
   - Enter staff credentials
   - Enter patient details (system will prompt to create new record)
   - Fill in required patient information

4. **Record a Visit**
   - Access patient records
   - Click "Add Visit"
   - Enter vital signs and notes
   - Save the record

---

## 📖 User Guide

### Accessing Patient Records

1. Navigate to **Patient Records** from the main menu
2. Enter your **Staff Credentials**:
   - Staff Number (assigned by admin)
   - Your Last Name
3. Enter **Patient Information**:
   - Patient First Name
   - Patient Last Name
   - Date of Birth

> 💡 **Tip**: Names can be entered in either order. "John Smith" and "Smith John" will both find the same patient.

### If Patient Not Found

The system will display options:
- **Create New Patient Record**: Register the patient in the system
- **Try Again**: Re-enter information if there was a typo

### Creating a New Patient

Required fields:

| Field | Description | Example |
|-------|-------------|---------|
| First Name | Patient's first name | John |
| Last Name | Patient's last name | Smith |
| Date of Birth | Patient's DOB | 1985-03-15 |
| Sex | Male/Female/Other | Male |
| Physician Staff Number | Assigned doctor's ID | DR001 |

### Recording Visit Vitals

| Field | Format | Example |
|-------|--------|---------|
| Weight | Include units | 165 lbs |
| Temperature | Include units | 98.6°F |
| Blood Pressure | Systolic/Diastolic | 120/80 |
| Pulse | Beats per minute | 72 bpm |
| Respiration | Breaths per minute | 16/min |
| Pain Level | 0-10 scale | 3 |
| Notes | Free text | Patient reports mild headache |

---

## 🔐 Security & Encryption

### How Encryption Works

```
Patient Credentials (First Name + Last Name + DOB)
                    ↓
            PBKDF2 Key Derivation
                    ↓
            256-bit Encryption Key
                    ↓
        Fernet Symmetric Encryption
                    ↓
            Encrypted Patient Data
```

### Security Features

1. **Credential-Based Encryption**
   - Patient data encrypted using patient's own information
   - Without correct credentials, data cannot be decrypted
   - Even database administrators cannot read raw patient data

2. **Staff Authentication**
   - Staff must authenticate before accessing any records
   - Session management with secure logout

3. **Access Logging**
   - Each visit record tracks who recorded the information
   - Timestamp on all records

### Important Security Notes

⚠️ **Credential Recovery**: If a patient's credentials (name/DOB) are entered incorrectly during creation, the record cannot be recovered. Always verify information carefully.

⚠️ **Data Backup**: Regularly backup the `medical_records.db` file. Encrypted data is only accessible with original credentials.

---

## 🗄️ Database Schema

### Staff Table
```sql
CREATE TABLE staff (
    id INTEGER PRIMARY KEY,
    staff_number VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Patient Table
```sql
CREATE TABLE patient (
    id INTEGER PRIMARY KEY,
    lookup_hash VARCHAR(256) UNIQUE NOT NULL,  -- For finding patients
    encrypted_data TEXT NOT NULL,               -- Encrypted patient info
    physician_staff_number VARCHAR(20) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Visit Table
```sql
CREATE TABLE visit (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER REFERENCES patient(id),
    encrypted_data TEXT NOT NULL,  -- Encrypted visit details
    visit_date DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 📁 File Structure

```
medical_app/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This documentation
│
├── instance/
│   └── medical_records.db      # SQLite database (created on first run)
│
├── static/
│   ├── style.css              # Application styling
│   └── logo.png               # Church logo for welcome page
│
└── templates/
    ├── base.html              # Base template with header/footer
    ├── index.html             # Welcome/home page
    ├── patient_auth.html      # Patient access authentication
    ├── patient_not_found.html # Patient not found options
    ├── create_patient.html    # New patient registration
    ├── patient_records.html   # Patient details & visit history
    ├── add_visit.html         # Record new visit
    └── staff_admin.html       # Staff management portal
```

---

## 🔧 Troubleshooting

### Common Issues

**Problem**: Application won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Problem**: "Module not found" error
```bash
# Ensure you're in the correct directory
cd medical_app

# Install missing module
pip install <module_name>
```

**Problem**: Database locked error
```bash
# Close any other applications accessing the database
# Restart the Flask application
```

**Problem**: Cannot decrypt patient data
- Verify the exact spelling of first name, last name
- Verify the exact date of birth format
- Names are case-insensitive but must match exactly otherwise

**Problem**: Forgot admin password
```bash
# Delete the database to reset (WARNING: loses all data)
rm instance/medical_records.db

# Restart the application - default admin will be recreated
python app.py
```

---

## 💻 Desktop Application (Offline Use)

You can create a standalone desktop application that runs without internet or Python installed.

### Option 1: Quick Run (Requires Python)

If the computer has Python installed:

**Windows:**
```bash
# Double-click run_app.bat
# OR run from command prompt:
run_app.bat
```

**Mac/Linux:**
```bash
chmod +x run_app.sh
./run_app.sh
```

### Option 2: Build Standalone Executable (No Python Required)

Create a single executable file that works on any computer:

**Windows:**
1. Open Command Prompt in the medical_app folder
2. Run: `build_windows.bat`
3. Find executable at: `dist\VitalSigns.exe`
4. Copy `VitalSigns.exe` to any Windows computer - it will run!

**Mac/Linux:**
```bash
chmod +x build_mac_linux.sh
./build_mac_linux.sh
# Executable at: dist/VitalSigns
```

### Where is Data Stored?

The database is stored locally on each computer:

| OS | Location |
|----|----------|
| Windows | `C:\Users\<user>\AppData\Local\GileadVitalSigns\` |
| Mac | `~/Library/Application Support/GileadVitalSigns/` |
| Linux | `~/.gileadvitalsigns/` |

### Sharing Data Between Computers

To share patient data between computers:
1. Copy the `medical_records.db` file from the data location above
2. Place it in the same location on the other computer
3. Both computers will have the same records

> ⚠️ **Important**: Patient data is encrypted. You need the correct patient credentials (name + DOB) to access records.

---

## 🚀 Production Deployment

### Recommended Changes for Production

1. **Use a Production WSGI Server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

2. **Enable HTTPS**
   - Use a reverse proxy (Nginx, Apache)
   - Obtain SSL certificate (Let's Encrypt)

3. **Use a Production Database**
   ```python
   # Change in app.py for PostgreSQL:
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/medical_db'
   ```

4. **Set Secure Secret Key**
   ```python
   # Use environment variable
   app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
   ```

5. **Disable Debug Mode**
   ```python
   app.run(debug=False)
   ```

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| SECRET_KEY | Flask session key | `your-secret-key-here` |
| DATABASE_URL | Database connection | `sqlite:///medical_records.db` |
| FLASK_ENV | Environment mode | `production` |

---

## 📞 Support & Contact

For technical issues or questions:
- Review this documentation
- Check the Troubleshooting section
- Contact your system administrator
- Email AfamUmejiaku@gmail.com

---

## 📄 License

This application is provided for use by Winners Chapel International Arlington - Gilead Health Ministry.
Designed and Maintained by Afamefuna Umejiaku

---

## 🙏 Acknowledgments

- Built with Flask (Python web framework)
- SQLite database (free, no setup required)
- Cryptography library for secure encryption
- Designed for healthcare privacy and security

---

*Gilead Vital Signs Medical Records System v1.0*  
*Winners Chapel International Arlington*  
*Keeping your health data secure* 🔐
