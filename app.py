"""
Medical Web Application - Vital Signs
A secure patient records management system with encrypted data storage.
Uses Flask + SQLite (free database) + Cryptography for encryption.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import json
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medical_records.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== MODELS ====================

class Staff(db.Model):
    """Staff members who can access patient records"""
    id = db.Column(db.Integer, primary_key=True)
    staff_number = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Patient(db.Model):
    """Patient basic information (non-encrypted for lookup)"""
    id = db.Column(db.Integer, primary_key=True)
    # These fields are hashed for lookup but stored encrypted elsewhere
    lookup_hash = db.Column(db.String(256), unique=True, nullable=False)  # Hash of first+last+dob
    encrypted_data = db.Column(db.Text, nullable=False)  # Encrypted patient details
    physician_staff_number = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class Visit(db.Model):
    """Patient visit records (encrypted)"""
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    encrypted_data = db.Column(db.Text, nullable=False)  # Encrypted visit details
    visit_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    patient = db.relationship('Patient', backref=db.backref('visits', lazy=True))


# ==================== ENCRYPTION UTILITIES ====================

def generate_encryption_key(first_name, last_name, dob):
    """
    Generate a unique encryption key based on patient credentials.
    This ensures only those with the correct credentials can decrypt the data.
    """
    # Normalize inputs (lowercase, strip whitespace)
    combined = f"{first_name.lower().strip()}{last_name.lower().strip()}{dob}".encode()
    
    # Use a fixed salt (in production, you'd want a secure random salt stored separately)
    salt = b'medical_app_salt_2024'
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    
    key = base64.urlsafe_b64encode(kdf.derive(combined))
    return key

def encrypt_data(data, first_name, last_name, dob):
    """Encrypt data using patient credentials as the key"""
    key = generate_encryption_key(first_name, last_name, dob)
    f = Fernet(key)
    json_data = json.dumps(data)
    encrypted = f.encrypt(json_data.encode())
    return encrypted.decode()

def decrypt_data(encrypted_data, first_name, last_name, dob):
    """Decrypt data using patient credentials"""
    try:
        key = generate_encryption_key(first_name, last_name, dob)
        f = Fernet(key)
        decrypted = f.decrypt(encrypted_data.encode())
        return json.loads(decrypted.decode())
    except Exception:
        return None

def generate_lookup_hash(first_name, last_name, dob):
    """Generate a hash for patient lookup (allows name swap)"""
    # Normalize and sort names to allow first/last name swap
    names = sorted([first_name.lower().strip(), last_name.lower().strip()])
    combined = f"{names[0]}{names[1]}{dob}"
    
    import hashlib
    return hashlib.sha256(combined.encode()).hexdigest()

def find_patient(first_name, last_name, dob):
    """Find patient allowing for first/last name swap"""
    # Try both combinations
    hash1 = generate_lookup_hash(first_name, last_name, dob)
    patient = Patient.query.filter_by(lookup_hash=hash1).first()
    return patient


# ==================== DECORATORS ====================

def staff_required(f):
    """Decorator to require staff authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'staff_number' not in session:
            flash('Please authenticate as staff first.', 'warning')
            return redirect(url_for('patient_auth'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'is_admin' not in session or not session['is_admin']:
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Welcome page with church name, vital signs, and navigation links"""
    return render_template('index.html')

@app.route('/patient-auth', methods=['GET', 'POST'])
def patient_auth():
    """Authentication page for accessing patient records"""
    if request.method == 'POST':
        staff_number = request.form.get('staff_number', '').strip()
        staff_last_name = request.form.get('staff_last_name', '').strip()
        patient_first = request.form.get('patient_first', '').strip()
        patient_last = request.form.get('patient_last', '').strip()
        patient_dob = request.form.get('patient_dob', '').strip()
        
        # Verify staff credentials
        staff = Staff.query.filter_by(staff_number=staff_number).first()
        if not staff or staff.last_name.lower() != staff_last_name.lower():
            flash('Invalid staff credentials. Please try again.', 'danger')
            return render_template('patient_auth.html')
        
        # Store staff info in session
        session['staff_number'] = staff_number
        session['staff_name'] = f"{staff.first_name} {staff.last_name}"
        session['is_admin'] = staff.is_admin
        
        # Find patient (allows name swap)
        patient = find_patient(patient_first, patient_last, patient_dob)
        
        if patient:
            # Store patient credentials for decryption
            session['patient_id'] = patient.id
            session['patient_first'] = patient_first
            session['patient_last'] = patient_last
            session['patient_dob'] = patient_dob
            return redirect(url_for('patient_records'))
        else:
            # Patient not found
            session['temp_patient_first'] = patient_first
            session['temp_patient_last'] = patient_last
            session['temp_patient_dob'] = patient_dob
            return render_template('patient_not_found.html', 
                                   first_name=patient_first, 
                                   last_name=patient_last, 
                                   dob=patient_dob)
    
    return render_template('patient_auth.html')

@app.route('/create-patient', methods=['GET', 'POST'])
@staff_required
def create_patient():
    """Create a new patient record"""
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        dob = request.form.get('dob', '').strip()
        sex = request.form.get('sex', '').strip()
        physician_number = request.form.get('physician_number', '').strip()
        
        # Validate required fields
        if not all([first_name, last_name, dob, sex, physician_number]):
            flash('All fields are required.', 'danger')
            return render_template('create_patient.html')
        
        # Verify physician exists
        physician = Staff.query.filter_by(staff_number=physician_number).first()
        if not physician:
            flash('Invalid physician staff number.', 'danger')
            return render_template('create_patient.html')
        
        # Check if patient already exists
        existing = find_patient(first_name, last_name, dob)
        if existing:
            flash('Patient already exists in the system.', 'warning')
            return render_template('create_patient.html')
        
        # Create encrypted patient data
        patient_data = {
            'first_name': first_name,
            'last_name': last_name,
            'dob': dob,
            'sex': sex
        }
        
        encrypted = encrypt_data(patient_data, first_name, last_name, dob)
        lookup_hash = generate_lookup_hash(first_name, last_name, dob)
        
        new_patient = Patient(
            lookup_hash=lookup_hash,
            encrypted_data=encrypted,
            physician_staff_number=physician_number
        )
        
        db.session.add(new_patient)
        db.session.commit()
        
        flash('Patient record created successfully!', 'success')
        
        # Set session for immediate access
        session['patient_id'] = new_patient.id
        session['patient_first'] = first_name
        session['patient_last'] = last_name
        session['patient_dob'] = dob
        
        return redirect(url_for('patient_records'))
    
    # Pre-fill from temp session data if available
    first_name = session.pop('temp_patient_first', '')
    last_name = session.pop('temp_patient_last', '')
    dob = session.pop('temp_patient_dob', '')
    
    return render_template('create_patient.html', 
                           first_name=first_name, 
                           last_name=last_name, 
                           dob=dob)

@app.route('/patient-records')
@staff_required
def patient_records():
    """Display patient records and visits"""
    patient_id = session.get('patient_id')
    if not patient_id:
        flash('Please select a patient first.', 'warning')
        return redirect(url_for('patient_auth'))
    
    patient = Patient.query.get(patient_id)
    if not patient:
        flash('Patient not found.', 'danger')
        return redirect(url_for('patient_auth'))
    
    # Decrypt patient data
    patient_data = decrypt_data(
        patient.encrypted_data,
        session['patient_first'],
        session['patient_last'],
        session['patient_dob']
    )
    
    if not patient_data:
        flash('Unable to decrypt patient records. Please verify credentials.', 'danger')
        return redirect(url_for('patient_auth'))
    
    # Get physician info
    physician = Staff.query.filter_by(staff_number=patient.physician_staff_number).first()
    
    # Decrypt all visits
    visits = []
    for visit in patient.visits:
        visit_data = decrypt_data(
            visit.encrypted_data,
            session['patient_first'],
            session['patient_last'],
            session['patient_dob']
        )
        if visit_data:
            visit_data['id'] = visit.id
            visit_data['visit_date'] = visit.visit_date.strftime('%Y-%m-%d %H:%M')
            visits.append(visit_data)
    
    # Sort visits by date (most recent first)
    visits.sort(key=lambda x: x['visit_date'], reverse=True)
    
    return render_template('patient_records.html', 
                           patient=patient_data, 
                           physician=physician,
                           visits=visits)

@app.route('/add-visit', methods=['GET', 'POST'])
@staff_required
def add_visit():
    """Add a new visit record for the patient"""
    patient_id = session.get('patient_id')
    if not patient_id:
        flash('Please select a patient first.', 'warning')
        return redirect(url_for('patient_auth'))
    
    if request.method == 'POST':
        visit_data = {
            'date': request.form.get('visit_date', datetime.now().strftime('%Y-%m-%d')),
            'weight': request.form.get('weight', ''),
            'temperature': request.form.get('temperature', ''),
            'blood_pressure': request.form.get('blood_pressure', ''),
            'pulse': request.form.get('pulse', ''),
            'respiration': request.form.get('respiration', ''),
            'pain_level': request.form.get('pain_level', ''),
            'notes': request.form.get('notes', ''),
            'recorded_by': session.get('staff_name', 'Unknown')
        }
        
        encrypted = encrypt_data(
            visit_data,
            session['patient_first'],
            session['patient_last'],
            session['patient_dob']
        )
        
        new_visit = Visit(
            patient_id=patient_id,
            encrypted_data=encrypted
        )
        
        db.session.add(new_visit)
        db.session.commit()
        
        flash('Visit record added successfully!', 'success')
        return redirect(url_for('patient_records'))
    
    return render_template('add_visit.html')

@app.route('/staff-admin', methods=['GET', 'POST'])
def staff_admin():
    """Admin page for managing staff records"""
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'login':
            admin_number = request.form.get('admin_number', '').strip()
            admin_last = request.form.get('admin_last', '').strip()
            
            admin = Staff.query.filter_by(staff_number=admin_number, is_admin=True).first()
            if admin and admin.last_name.lower() == admin_last.lower():
                session['is_admin'] = True
                session['admin_name'] = f"{admin.first_name} {admin.last_name}"
                flash(f'Welcome, {admin.first_name}!', 'success')
            else:
                flash('Invalid admin credentials.', 'danger')
        
        elif action == 'add_staff' and session.get('is_admin'):
            staff_number = request.form.get('staff_number', '').strip()
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            is_admin = request.form.get('is_admin') == 'on'
            
            if not all([staff_number, first_name, last_name]):
                flash('All fields are required.', 'danger')
            elif Staff.query.filter_by(staff_number=staff_number).first():
                flash('Staff number already exists.', 'danger')
            else:
                new_staff = Staff(
                    staff_number=staff_number,
                    first_name=first_name,
                    last_name=last_name,
                    is_admin=is_admin
                )
                db.session.add(new_staff)
                db.session.commit()
                flash(f'Staff member {first_name} {last_name} added successfully!', 'success')
        
        elif action == 'delete_staff' and session.get('is_admin'):
            staff_id = request.form.get('staff_id')
            staff = Staff.query.get(staff_id)
            if staff:
                db.session.delete(staff)
                db.session.commit()
                flash('Staff member removed.', 'success')
    
    staff_list = Staff.query.all() if session.get('is_admin') else []
    return render_template('staff_admin.html', staff_list=staff_list)

@app.route('/logout')
def logout():
    """Clear session and logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/clear-patient')
def clear_patient():
    """Clear patient from session but keep staff logged in"""
    session.pop('patient_id', None)
    session.pop('patient_first', None)
    session.pop('patient_last', None)
    session.pop('patient_dob', None)
    return redirect(url_for('patient_auth'))


# ==================== INITIALIZATION ====================

def init_db():
    """Initialize database and create default admin if none exists"""
    with app.app_context():
        db.create_all()
        
        # Create default admin if no staff exists
        if Staff.query.count() == 0:
            default_admin = Staff(
                staff_number='ADMIN001',
                first_name='System',
                last_name='Administrator',
                is_admin=True
            )
            db.session.add(default_admin)
            db.session.commit()
            print("Default admin created: Staff Number: ADMIN001, Last Name: Administrator")


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
