from flask import Blueprint, render_template, url_for, redirect, request, session, jsonify 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from wtforms.fields import StringField, SelectField, RadioField
from app.auth import *
from app.dashboard import *
from app.models.course import *
from app.models.studyinterest import *
from statistics import mean
from sqlalchemy.orm import joinedload


class SubjectSelectionForm(FlaskForm):
    subject_code = SelectField('Subject Code', choices=[])
    course_title = SelectField('Course Title', choices=[], 
                               render_kw={"onchange": "course_title.onchange()"})

    pro_ans1 = RadioField(u'How Knowledgeable are you on a subject?',
                          validators=[InputRequired()],
                           choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    pro_ans2 = RadioField(u'What is your Current Grade in this subject?',
                          validators=[InputRequired()], 
                           choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    pro_ans3 = RadioField(u'How would you Rate Yourself in this subject?',
                          validators=[InputRequired()], 
                           choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])   
    but = SubmitField("Submit")

def calc_pro_score(form):
    return round(mean([int(form.pro_ans1.data),
                                     int(form.pro_ans2.data), 
                                     int(form.pro_ans3.data)]),2)

bp = Blueprint('subjectselection', __name__, url_prefix='/')

'''
1. The initial GET
2. Submit  
'''
@bp.route('/subjectselection', methods=['GET', 'POST'])
@login_required
def subjectSelection():
    form = SubjectSelectionForm()
    form.subject_code.choices = [(Subject.subject_code, f'({Subject.subject_code}) {Subject.subject_name}') for Subject in Subject.query.all()]
    user = User.query.filter_by(username=current_user.username).first()
    course = None
    
        
    '''
    if request.method == 'GET':
        if si:
            form.pro_ans1.data = si.pro_ans1
            form.pro_ans2.data = si.pro_ans2
            form.pro_ans3.data = si.pro_ans3
    '''
    if form.validate_on_submit:
        if user:
            if form.data['but']:
                #Count si study_interest
                course_id  = form.course_title.data # Option value contains id 
                course = Course.query.filter_by(id=course_id).first()
                total_si = StudyInterest.query.filter_by(user_id=user.id).count()
                
                if total_si >= 5:
                    msg = "Maximum number of subjects selected"
                    return render_template('subjectselection.html', form=form, course=course, msg=msg)
                
                si = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()
                if si:
                    si.pro_ans1 = form.pro_ans1.data
                    si.pro_ans2 = form.pro_ans2.data
                    si.pro_ans3 = form.pro_ans3.data
                    si.pro_score = calc_pro_score(form)
                                                   
                else:
                    si = StudyInterest(user_id=user.id, course_id=course.id, pro_ans1=form.pro_ans1.data,
                               pro_ans2=form.pro_ans2.data, pro_ans3=form.pro_ans3.data, 
                               pro_score= calc_pro_score(form))
                                    
                db.session.add(si)
                db.session.commit()
                form.subject_code.data = None
                form.course_title.data = None
                form.pro_ans1.data = None
                form.pro_ans2.data = None
                form.pro_ans3.data = None
            #form.proScore = (form.proAns1 + form.proAns2 + form.proAns3) / 3
            print(request.form.get("pro_ans1"))
            print(request.form.get("pro_ans2"))
            print(request.form.get("pro_ans3"))
    return render_template('subjectselection.html', form=form, course=course)

@bp.route('/subjectselection/<get_code>', methods=['GET', 'POST'])
@login_required
def codesortcourse(get_code):
    course = Course.query.filter_by(subject_code=get_code).all()
    course_array = []
    for code in course:
        course = {}
        course['id'] = code.id
        course['code'] = code.subject_code
        course['number'] = code.course_number
        course['name'] = code.course_name
        course_array.append(course)
    return jsonify({'courselist': course_array})

'''
1. Create a route called subjectselections
2. StudyInterest model filter by user code and return render with a template
3. Create template and loop study interest objects and display
'''
@bp.route('/subjectselections', methods=['GET', 'POST'])
@login_required
def list_of_subjects_selected():
    form = SubjectSelectionForm()
    si = None
    user = User.query.filter_by(username=current_user.username).first()
    if user:
        si = StudyInterest.query.filter_by(user_id=user.id).options(joinedload(StudyInterest.course)).all()  
    return render_template('subjectselections.html',form=form, si=si)
