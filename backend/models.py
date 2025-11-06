from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ============================================================
# 🧩 Student Personal / Admission Details
# ============================================================
class Student(db.Model):
    __tablename__ = 'student'  # Table name

    id = db.Column(db.Integer, primary_key=True)

    # 🔹 Admission details
    category = db.Column(db.String(50), nullable=False)
    ciwgc = db.Column(db.String(50))
    nri = db.Column(db.String(50))

    # 🔹 Personal details
    title = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    alt_mobile = db.Column(db.String(15))
    country_code = db.Column(db.String(50), nullable=False)
    country_code_alt = db.Column(db.String(50))
    dob = db.Column(db.Date, nullable=False)
    differently_abled = db.Column(db.String(50))
    community = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    religion = db.Column(db.String(50), nullable=False)
    mother_tongue = db.Column(db.String(50), nullable=False)
    blood_group = db.Column(db.String(20))
    nationality = db.Column(db.String(50), nullable=False)
    first_graduate = db.Column(db.String(50))
    aadhar_number = db.Column(db.String(20), nullable=False)

    # 🔹 Additional info
    college_info_source = db.Column(db.String(100))
    country_of_residency = db.Column(db.String(100))
    state = db.Column(db.String(100))
    district = db.Column(db.String(100))
    city = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 🔹 One-to-One relationships
    address = db.relationship(
        'StuAddress',
        back_populates='student',
        uselist=False,
        cascade="all, delete-orphan"
    )

    academic = db.relationship(
        'StudentAcademic',
        back_populates='student',
        uselist=False,
        cascade="all, delete-orphan"
    )

# ============================================================
# 📦 Student Address Details
# ============================================================
class StuAddress(db.Model):
    __tablename__ = 'student_address'

    id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    fullAddress = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)

    student = db.relationship('Student', back_populates='address')

# ============================================================
# 🎓 Academic Details (10th, 12th & Preferences)
# ============================================================
class StudentAcademic(db.Model):
    __tablename__ = 'student_academic'

    id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)

    # 🔸 10th Details
    tenth_school = db.Column(db.String(150))
    tenth_board = db.Column(db.String(100))
    tenth_roll_number = db.Column(db.String(50))
    tenth_year = db.Column(db.String(10))
    tenth_percentage = db.Column(db.String(10))

    # 🔸 10th Subject Marks
    tenth_math_max = db.Column(db.Integer)
    tenth_math_obt = db.Column(db.Integer)
    tenth_math_perc = db.Column(db.String(10))
    tenth_sci_max = db.Column(db.Integer)
    tenth_sci_obt = db.Column(db.Integer)
    tenth_sci_perc = db.Column(db.String(10))

    # 🔸 12th Details
    twelfth_school = db.Column(db.String(150))
    twelfth_board = db.Column(db.String(100))
    twelfth_roll_number = db.Column(db.String(50))
    twelfth_year = db.Column(db.String(10))
    twelfth_school_code = db.Column(db.String(50))
    twelfth_centre_code = db.Column(db.String(50))
    admit_card = db.Column(db.String(50))
    cutoff = db.Column(db.String(10))

    # 🔸 Qualified Exam Marks
    math_marks = db.Column(db.String(20))
    math_perc = db.Column(db.String(10))
    math_attempts = db.Column(db.String(10))
    math_month_year = db.Column(db.String(20))

    physics_marks = db.Column(db.String(20))
    physics_perc = db.Column(db.String(10))
    physics_attempts = db.Column(db.String(10))
    physics_month_year = db.Column(db.String(20))

    chemistry_marks = db.Column(db.String(20))
    chemistry_perc = db.Column(db.String(10))
    chemistry_attempts = db.Column(db.String(10))
    chemistry_month_year = db.Column(db.String(20))

    # 🔸 Branch Preferences
    branch_pref_1 = db.Column(db.String(100))
    branch_pref_2 = db.Column(db.String(100))
    branch_pref_3 = db.Column(db.String(100))
    branch_pref_4 = db.Column(db.String(100))
    branch_pref_5 = db.Column(db.String(100))
    branch_pref_6 = db.Column(db.String(100))

    # 🔸 Additional Particulars
    extra_curricular = db.Column(db.Text)
    why_ssn = db.Column(db.Text)

    # 🔸 Audit field
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Back reference to student
    student = db.relationship('Student', back_populates='academic')

# ============================================================
# ✅ Helper: Initialize database (optional)
# ============================================================
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
