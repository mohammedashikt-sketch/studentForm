import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from config import Config
from models import db, Student, StudentParent, StuAddress, StudentAcademic, StudentUpload
from utils import allowed_file, generate_unique_number, validate_student_data

# ============================================================
# App Configuration
# ============================================================
app = Flask(__name__, static_folder="../frontend", template_folder="../frontend")
app.config.from_object(Config)
CORS(app)
db.init_app(app)

with app.app_context():
    db.create_all()

# ============================================================
# Logging Configuration
# ============================================================
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ============================================================
# Serve Frontend
# ============================================================
@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory('../frontend', path)

# ============================================================
# Upload + Save Student Data
# ============================================================
@app.route('/api/students/upload', methods=['POST'])
def upload_and_save_student():
    try:
        logging.info("📥 Received student upload request")

        student_data = request.form.get('student_data')
        if not student_data:
            logging.warning("Student data missing in request")
            return jsonify({'error': "Student data missing"}), 400

        data = json.loads(student_data)
        error = validate_student_data(data)
        if error:
            logging.warning(f"Validation failed: {error}")
            return jsonify({"error": error}), 400

        # Parse DOB safely
        dob_str = data.get('dob')
        try:
            dob_value = datetime.strptime(dob_str, "%Y-%m-%d")
        except ValueError:
            dob_value = datetime.fromisoformat(dob_str.replace("Z", ""))

        logging.info("✅ Basic student data parsed")

        # Prepare related tables
        address_data = data.get('address', {})
        academic_data = data.get('academic', {})

        student = Student(
            unique_number=int(generate_unique_number()),
            category=data['category'],
            ciwgc=data.get('ciwgc'),
            nri=data.get('nri'),
            title=data['title'],
            name=data['name'],
            email=data['email'],
            mobile=data['mobile'],
            alt_mobile=data.get('alt_mobile'),
            country_code=data['country_code'],
            country_code_alt=data.get('country_code_alt'),
            dob=dob_value,
            differently_abled=data.get('differently_abled'),
            community=data['community'],
            gender=data['gender'],
            religion=data['religion'],
            mother_tongue=data['mother_tongue'],
            blood_group=data.get('blood_group'),
            nationality=data['nationality'],
            first_graduate=data.get('first_graduate'),
            aadhar_number=data['aadhar_number'],
            college_info_source=data.get('college_info_source'),
            country_of_residency=data.get('country_of_residency'),
            state=data['state'],
            district=data['district'],
            city=data['city']
        )

        address = StuAddress(
            fullAddress=address_data.get('fullAddress'),
            pincode=address_data.get('pincode')
        )

        academic = StudentAcademic(
            tenth_school=academic_data.get('tenth_school'),
            tenth_board=academic_data.get('tenth_board'),
            tenth_roll_number=academic_data.get('tenth_roll_number'),
            tenth_year=academic_data.get('tenth_year'),
            tenth_percentage=academic_data.get('tenth_percentage'),
            tenth_math_max=academic_data.get('tenth_math_max'),
            tenth_math_obt=academic_data.get('tenth_math_obt'),
            tenth_math_perc=academic_data.get('tenth_math_perc'),
            tenth_sci_max=academic_data.get('tenth_sci_max'),
            tenth_sci_obt=academic_data.get('tenth_sci_obt'),
            tenth_sci_perc=academic_data.get('tenth_sci_perc'),
            twelfth_school=academic_data.get('twelfth_school'),
            twelfth_board=academic_data.get('twelfth_board'),
            twelfth_roll_number=academic_data.get('twelfth_roll_number'),
            twelfth_year=academic_data.get('twelfth_year'),
            twelfth_school_code=academic_data.get('twelfth_school_code'),
            twelfth_centre_code=academic_data.get('twelfth_centre_code'),
            admit_card=academic_data.get('admit_card'),
            cutoff=academic_data.get('cutoff'),
            math_marks=academic_data.get('math_marks'),
            math_perc=academic_data.get('math_perc'),
            math_attempts=academic_data.get('math_attempts'),
            math_month_year=academic_data.get('math_month_year'),
            physics_marks=academic_data.get('physics_marks'),
            physics_perc=academic_data.get('physics_perc'),
            physics_attempts=academic_data.get('physics_attempts'),
            physics_month_year=academic_data.get('physics_month_year'),
            chemistry_marks=academic_data.get('chemistry_marks'),
            chemistry_perc=academic_data.get('chemistry_perc'),
            chemistry_attempts=academic_data.get('chemistry_attempts'),
            chemistry_month_year=academic_data.get('chemistry_month_year'),
            branch_pref_1=academic_data.get('branch_pref_1'),
            branch_pref_2=academic_data.get('branch_pref_2'),
            branch_pref_3=academic_data.get('branch_pref_3'),
            branch_pref_4=academic_data.get('branch_pref_4'),
            branch_pref_5=academic_data.get('branch_pref_5'),
            branch_pref_6=academic_data.get('branch_pref_6'),
            extra_curricular=academic_data.get('extra_curricular'),
            why_ssn=academic_data.get('why_ssn')
        )

        db.session.add(student)
        db.session.flush()
        
        parent = StudentParent(
            id=student.id,
            father_title=data.get('father_title'),
            father_name=data.get('father_name'),
            father_mobile=data.get('father_mobile'),
            father_landline=data.get('father_landline'),
            father_email=data.get('father_email'),
            father_occupation=data.get('father_occupation'),
            father_designation=data.get('father_designation'),
            father_annual_income=data.get('father_annual_income'),
            mother_title=data.get('mother_title'),
            mother_name=data.get('mother_name'),
            mother_mobile=data.get('mother_mobile'),
            mother_landline=data.get('mother_landline'),
            mother_email=data.get('mother_email'),
            mother_occupation=data.get('mother_occupation'),
            mother_designation=data.get('mother_designation'),
            mother_annual_income=data.get('mother_annual_income'),
            has_guardian=data.get('has_guardian'),
            guardian_title=data.get('guardian_title'),
            guardian_name=data.get('guardian_name'),
            guardian_mobile=data.get('guardian_mobile'),
            guardian_landline=data.get('guardian_landline'),
            guardian_email=data.get('guardian_email'),
            guardian_occupation=data.get('guardian_occupation'),
            guardian_designation=data.get('guardian_designation')
        )
        # -------------------------------
        # File Uploads (before commit)
        # -------------------------------
        files = request.files
        file_fields = [
            'photo', 'signature', 'marksheet_10th', 'marksheet_12th',
            'marksheet_diploma', 'marksheet_graduation',
            'community', 'passport', 'admitcard'
        ]

        upload_folder = app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)

        paths = {}
        for key in file_fields:
            file = files.get(key)
            if file and allowed_file(file.filename, key):
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"{student.id}_{key}.{ext}"
                file_path = os.path.join(upload_folder, secure_filename(filename))
                file.save(file_path)
                paths[key] = os.path.join('uploads', filename)
                logging.info(f"✅ Saved file {filename}")
            else:
                paths[key] = None
                logging.warning(f"⚠️ No valid file uploaded for {key}")

        

        # -------------------------------
        # Save Upload Info
        # -------------------------------
        upload = StudentUpload(
            id=student.id,
            applicant_name=data['name'],
            parent_name=data['parent_name'],
            community_path=paths['community'],
            photo_path=paths['photo'],
            signature_path=paths['signature'],
            marksheet_10th_path=paths['marksheet_10th'],
            marksheet_12th_path=paths['marksheet_12th'],
            marksheet_graduation_path=paths['marksheet_graduation'],
            marksheet_diploma_path=paths['marksheet_diploma'],
            passport_path=paths['passport'],
            admitcard_path=paths['admitcard']
        )

        student.address = address
        student.academic = academic
        student.parent = parent

        # Link all under one commit
        db.session.add_all([student, parent, address, academic, upload])
        db.session.commit()

        logging.info("🎉 Student and related data committed successfully")
        return jsonify({"message": "Student data + files uploaded successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"❌ Error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

# ============================================================
# Fetch All Students
# ============================================================
@app.route('/api/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    result = []
    for s in students:
        result.append({
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "mobile": s.mobile,
            "dob": s.dob.strftime("%Y-%m-%d") if s.dob else None,
            "category": s.category,
            "gender": s.gender,
            "city": s.city,
            "address": {
                "fullAddress": s.address.fullAddress if s.address else None,
                "pincode": s.address.pincode if s.address else None
            },
            "academic": {
                "tenth_school": s.academic.tenth_school if s.academic else None,
                "twelfth_school": s.academic.twelfth_school if s.academic else None,
                "cutoff": s.academic.cutoff if s.academic else None,
                "branch_pref_1": s.academic.branch_pref_1 if s.academic else None
            } if s.academic else {}
        })
    return jsonify(result), 200

# ============================================================
# Run App
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)
