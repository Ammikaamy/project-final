from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///classroom.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ===================== MODELS ===================== #

# ตาราง User (ทั้งครูและนักเรียน)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'teacher' or 'student'

# ตาราง Classroom
class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    invite_code = db.Column(db.String(6), unique=True, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    students = db.relationship('StudentClassroom', backref='classroom', lazy=True)

# ตารางนักเรียนที่เข้าร่วมชั้นเรียน
class StudentClassroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)

# ===================== API ROUTES ===================== #

# สร้างรหัสเชิญแบบสุ่ม
def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# 1. ครูสร้างชั้นเรียน
@app.route('/create_classroom', methods=['POST'])
def create_classroom():
    data = request.json
    teacher_id = data.get('teacher_id')
    class_name = data.get('name')

    teacher = User.query.get(teacher_id)
    if not teacher or teacher.role != 'teacher':
        return jsonify({'error': 'Invalid teacher ID'}), 400

    invite_code = generate_invite_code()
    new_class = Classroom(name=class_name, invite_code=invite_code, teacher_id=teacher_id)

    db.session.add(new_class)
    db.session.commit()

    return jsonify({'message': 'Classroom created', 'invite_code': invite_code}), 201

# 2. นักเรียนเข้าร่วมชั้นเรียน
@app.route('/join_classroom', methods=['POST'])
def join_classroom():
    data = request.json
    student_id = data.get('student_id')
    invite_code = data.get('invite_code')

    student = User.query.get(student_id)
    if not student or student.role != 'student':
        return jsonify({'error': 'Invalid student ID'}), 400

    classroom = Classroom.query.filter_by(invite_code=invite_code).first()
    if not classroom:
        return jsonify({'error': 'Invalid invite code'}), 400

    # ตรวจสอบว่านักเรียนเข้าร่วมหรือยัง
    existing_entry = StudentClassroom.query.filter_by(student_id=student_id, classroom_id=classroom.id).first()
    if existing_entry:
        return jsonify({'error': 'Student already in classroom'}), 400

    new_entry = StudentClassroom(student_id=student_id, classroom_id=classroom.id)
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({'message': 'Joined classroom successfully'}), 200

# 3. ดูรายชื่อชั้นเรียนทั้งหมด
@app.route('/classrooms', methods=['GET'])
def get_classrooms():
    classrooms = Classroom.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'invite_code': c.invite_code, 'teacher_id': c.teacher_id} for c in classrooms])

# 4. ดูรายชื่อนักเรียนในชั้นเรียน
@app.route('/classroom/<int:classroom_id>/students', methods=['GET'])
def get_students_in_class(classroom_id):
    students = StudentClassroom.query.filter_by(classroom_id=classroom_id).all()
    student_list = [{'student_id': s.student_id, 'name': User.query.get(s.student_id).name} for s in students]
    return jsonify(student_list)

if __name__ == '__main__':
    app.run(debug=True)
