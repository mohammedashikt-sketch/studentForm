from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from models import db, Student, StuAddress, StudentAcademic
from config import Config
import re

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)

with app.app_context():
    db.create_all()


# ============================================================
# 🔹 ADD COMPLETE STUDENT (Personal + Address + Academic)
# ============================================================
@app.route('/api/students', methods=['POST'])
def add_full_student():
    data = request.get_json()

    # ✅ Step 1: Basic validation
    required_fields = [
        'category', 'title', 'country_code', 'nationality', 'name',
        'email', 'mobile', 'dob', 'community', 'gender',
        'religion', 'mother_tongue', 'aadhar_number',
        'state', 'district', 'city'
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    # ✅ Address validation
    address_data = data.get('address')
    if not address_data:
        return jsonify({"error": "Address details are required"}), 400
    for field in ['fullAddress', 'pincode']:
        if not address_data.get(field):
            return jsonify({"error": f"Address field '{field}' is required"}), 400

    # ✅ Academic data check
    academic_data = data.get('academic')
    if not academic_data:
        return jsonify({"error": "Academic details are required"}), 400

    # ✅ Regex validations
    if not re.fullmatch(r'\d{10}', data['mobile']):
        return jsonify({"error": "Mobile number must be 10 digits"}), 400
    if not re.fullmatch(r'\d{12}', data['aadhar_number']):
        return jsonify({"error": "Aadhar number must be 12 digits"}), 400

    # ✅ Date of birth
    try:
        dob_value = datetime.strptime(data['dob'], "%Y-%m-%d")
        if dob_value > datetime.now():
            return jsonify({"error": "DOB cannot be in the future"}), 400
    except Exception:
        return jsonify({"error": "Invalid date format for DOB"}), 400

    # ======================================================
    # ✅ Create Student + Address + Academic together
    # ======================================================
    try:
        student = Student(
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

        # 🏠 Address
        address = StuAddress(
            fullAddress=address_data['fullAddress'],
            pincode=address_data['pincode']
        )

        # 🎓 Academic
        acad = academic_data
        academic = StudentAcademic(
            tenth_school=acad.get('tenth_school'),
            tenth_board=acad.get('tenth_board'),
            tenth_roll_number=acad.get('tenth_roll_number'),
            tenth_year=acad.get('tenth_year'),
            tenth_percentage=acad.get('tenth_percentage'),
            tenth_math_max=acad.get('tenth_math_max'),
            tenth_math_obt=acad.get('tenth_math_obt'),
            tenth_math_perc=acad.get('tenth_math_perc'),
            tenth_sci_max=acad.get('tenth_sci_max'),
            tenth_sci_obt=acad.get('tenth_sci_obt'),
            tenth_sci_perc=acad.get('tenth_sci_perc'),
            twelfth_school=acad.get('twelfth_school'),
            twelfth_board=acad.get('twelfth_board'),
            twelfth_roll_number=acad.get('twelfth_roll_number'),
            twelfth_year=acad.get('twelfth_year'),
            twelfth_school_code=acad.get('twelfth_school_code'),
            twelfth_centre_code=acad.get('twelfth_centre_code'),
            admit_card=acad.get('admit_card'),
            cutoff=acad.get('cutoff'),
            math_marks=acad.get('math_marks'),
            math_perc=acad.get('math_perc'),
            math_attempts=acad.get('math_attempts'),
            math_month_year=acad.get('math_month_year'),
            physics_marks=acad.get('physics_marks'),
            physics_perc=acad.get('physics_perc'),
            physics_attempts=acad.get('physics_attempts'),
            physics_month_year=acad.get('physics_month_year'),
            chemistry_marks=acad.get('chemistry_marks'),
            chemistry_perc=acad.get('chemistry_perc'),
            chemistry_attempts=acad.get('chemistry_attempts'),
            chemistry_month_year=acad.get('chemistry_month_year'),
            branch_pref_1=acad.get('branch_pref_1'),
            branch_pref_2=acad.get('branch_pref_2'),
            branch_pref_3=acad.get('branch_pref_3'),
            branch_pref_4=acad.get('branch_pref_4'),
            branch_pref_5=acad.get('branch_pref_5'),
            branch_pref_6=acad.get('branch_pref_6'),
            extra_curricular=acad.get('extra_curricular'),
            why_ssn=acad.get('why_ssn')
        )

        # Link all
        student.address = address
        student.academic = academic

        db.session.add(student)
        db.session.commit()

        return jsonify({
            "message": "Student (with academic + address) saved successfully!",
            "student_id": student.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ============================================================
# 🔹 GET ALL STUDENTS (with academic)
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


if __name__ == '__main__':
    app.run(debug=True)
