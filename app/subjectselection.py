from flask import Blueprint, render_template, url_for, redirect, request, session, jsonify 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from wtforms.fields import StringField, SelectField, RadioField
from app.auth import *
from app.dashboard import *
from app.models.course import *
from app.models.studyinterest import *

class SubjectSearchForm(FlaskForm):

    subject_code = SelectField('Subject Code', choices=[])
    course_title = SelectField('Course Title', choices=[])


class SubjectSelectionForm(FlaskForm):
    pro_ans1 = RadioField(u'How Knowledgeable are you on a subject?', 
                           choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    pro_ans2 = RadioField(u'What is your Current Grade in this subject?', 
                           choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    pro_ans3 = RadioField(u'How would you Rate Yourself in this subject?', 
                           choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    but = SubmitField("Submit")
    
bp = Blueprint('subjectselection', __name__, url_prefix='/')

@bp.route('/subjectselection', methods=['GET', 'POST'])
@login_required
def subjectSelection():
    form = SubjectSelectionForm()

    subject_search_form = SubjectSearchForm()
    subject_search_form.subject_code.choices = [(SubjectCode.subject_code, f'({SubjectCode.subject_code}) {SubjectCode.subject_name}') for SubjectCode in SubjectCode.query.all()]

    course_id  = 1
    course = Courses.query.filter_by(id=course_id).first()
    if form.validate_on_submit:
        user = User.query.filter_by(username=current_user.username).first()
        if user:
            if form.data['but']:
                si = StudyInterest(user_id=user.id, course_id=course.id, pro_ans1=form.pro_ans1.data,
                               pro_ans2=form.pro_ans2.data, pro_ans3=form.pro_ans3.data, 
                               pro_score=
                               ((int(form.pro_ans1.data) + int(form.pro_ans2.data) + int(form.pro_ans3.data)) / 3))
                db.session.add(si)
                db.session.commit()

            #form.proScore = (form.proAns1 + form.proAns2 + form.proAns3) / 3
            print(request.form.get("pro_ans1"))
            print(request.form.get("pro_ans2"))
            print(request.form.get("pro_ans3"))
    return render_template('subjectselection.html', form=form, course=course, subject_search_form=subject_search_form)

@bp.route('/subjectselection/<get_code>', methods=['GET', 'POST'])
@login_required
def codesortcourse(get_code):
    course = Courses.query.filter_by(subject_code=get_code).all()
    course_array = []
    for code in course:
        course = {}
        course['code'] = code.subject_code
        course['number'] = code.course_number
        course['name'] = code.course_name
        course_array.append(course)
    return jsonify({'courselist': course_array})
