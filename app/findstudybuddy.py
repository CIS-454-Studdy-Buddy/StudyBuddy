from flask import Blueprint, render_template, url_for, redirect, request, session 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.models.user import *
from app.models.course import *
from app.models.studyinterest import *
from app.models.buddyrelation import *
from wtforms.fields import StringField, SelectField
from sqlalchemy import and_
from sqlalchemy.orm import joinedload


class FindBuddyForm(FlaskForm):
    subject_code = SelectField('Subject Code', validators=[InputRequired()], choices=[])

    buddy_but = SubmitField("Search Buddy")

bp = Blueprint('findstudybuddy', __name__, url_prefix='/')
@bp.route('/findstudybuddy', methods=['GET', 'POST'])
@login_required
def findBuddy():
    form = FindBuddyForm()
    si_all = None
    user = User.query.filter_by(id=current_user.id).first()
    form.subject_code.choices = [("", "")] + [(si.course.id, f'{si.course.subject_code} {si.course.course_number} - {si.course.course_name}') 
                                 for si in StudyInterest.query.filter_by(user_id=user.id).all()]
    
    if form.validate_on_submit:
        si_query = StudyInterest.query.filter(
            and_(StudyInterest.user_id != user.id,
                  StudyInterest.course_id==form.subject_code.data
                  # put additonal filter here 
                  )                  
                  ).options(joinedload(StudyInterest.course)).options(joinedload(StudyInterest.user))
        si_all = si_query.all()
        #print(si_query.statement)
    return render_template('findstudybuddy.html', form=form, si_all=si_all)