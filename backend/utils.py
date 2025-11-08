from datetime import datetime
from models import db, Student, StudentUpload
from sqlalchemy import func
import re
from config import Config

ALLOWED_PHOTOS = Config.ALLOWED_PHOTOS
ALLOWED_DOCS = Config.ALLOWED_DOCS


def allowed_file(filename, doc_type):
    allowed = ALLOWED_PHOTOS if doc_type in ['photo', 'signature'] else ALLOWED_DOCS
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed

def generate_unique_number():
    last_number = db.session.query(func.max(Student.unique_number)).scalar()
    if last_number:
        try:
            new_number = int(last_number) + 1  # convert string to int and increment
        except ValueError:
            # fallback if last_number is not numeric
            new_number = int(datetime.now().timestamp())
    else:
        new_number = 1001  # starting number if table is empty
    return str(new_number)  # always return as string

def insert_student(**data):
    student = Student(**data)
    db.session.add(student)
    db.session.commit()

def validate_student_data(data):
    """Validate required fields and formats"""
    required_fields = [
        'category', 'title', 'country_code', 'nationality', 'name',
        'email', 'mobile', 'dob', 'community', 'gender',
        'religion', 'mother_tongue', 'aadhar_number',
        'state', 'district', 'city'
    ]

    category = data.get('category')
    if category == 'NRI':
        required_fields.append('nri')
    elif category == 'CIWGC':
        required_fields.append('ciwgc')

    for field in required_fields:
        if not data.get(field):
            return f"'{field}' is required"

    if not re.fullmatch(r'\d{10}', data['mobile']):
        return "Mobile number must be 10 digits"

    if data.get('alt_mobile') and not re.fullmatch(r'\d{10}', data['alt_mobile']):
        return "Alternate mobile number must be 10 digits"

    if not re.fullmatch(r'\d{12}', data['aadhar_number']):
        return "Aadhar number must be 12 digits"

    '''try:
        dob_value = datetime.strptime(data['dob'], "%Y-%m-%d")
        if dob_value > datetime.now():
            return "Date of birth cannot be in the future"
    except Exception:
        return "Invalid date of birth format"'''
    dob_str=data.get("dob")
    try:
        # Try to parse YYYY-MM-DD first
        dob_value = datetime.strptime(dob_str, "%Y-%m-%d")
    except ValueError:
        try:
            # Try ISO format (e.g. 2025-10-28T00:00:00Z)
            dob_value = datetime.fromisoformat(dob_str.replace("Z", ""))
        except Exception:
            return "Invalid date of birth format"

    if dob_value > datetime.now():
        return "Date of birth cannot be in the future"

    return None  # ✅ No errors