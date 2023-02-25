from flask import Blueprint, render_template, url_for, redirect, request, session 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.dashboard import *
from app.models.studyinterest import *
from wtforms.fields import SelectField, RadioField
from statistics import mean

class subjectSelectionForm(FlaskForm):
    pro_ans1 = RadioField(u'How Knowledgeable are you on a subject?', 
                           choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    pro_ans2 = RadioField(u'What is your Current Grade in this subject?', 
                           choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    pro_ans3 = RadioField(u'How would you Rate Yourself in this subject?', 
                           choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    but = SubmitField("Submit")

def calc_pro_score(form):
    return round(mean([int(form.pro_ans1.data),
                                     int(form.pro_ans2.data), 
                                     int(form.pro_ans3.data)]),2)

bp = Blueprint('subjectselection', __name__, url_prefix='/')
@bp.route('/subjectselection', methods=['GET', 'POST'])
@login_required
def subjectSelection():
    form = subjectSelectionForm()
    course_id  = 1
    course = Course.query.filter_by(id=course_id).first()
    user = User.query.filter_by(username=current_user.username).first()
    si = StudyInterest.query.filter_by(user_id=user.id).filter_by(course_id=course.id).first()
    if request.method == 'GET':
        if si:
            form.pro_ans1.data = si.pro_ans1
            form.pro_ans2.data = si.pro_ans2
            form.pro_ans3.data = si.pro_ans3

    if form.validate_on_submit:
        if user:
            if form.data['but']:
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

    return render_template('subjectselection.html', form=form, course=course)