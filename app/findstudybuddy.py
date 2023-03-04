from flask import Blueprint, render_template, url_for, redirect, request, session 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.dashboard import *
from app.models.user import *
from app.models.course import *
from app.models.studyinterest import *
from app.models.buddyrelation import *
from wtforms.fields import StringField, SelectField, RadioField, SelectMultipleField
from wtforms import widgets
from sqlalchemy import and_, or_
from sqlalchemy.orm import joinedload

'''
Custom SelectMultipleField with checkboxes
'''
class SelectMultipleFieldsWithChecks(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class FindBuddyForm(FlaskForm):
    subject_code = SelectField('Subject Code', validators=[InputRequired()], choices=[])

    prof_select = SelectMultipleFieldsWithChecks('Proficiency Score', validate_choice=False, choices=[(4, '4.0 - 5.0 score'), (3, '3.0 - 4.0 score'), (2, '2.0 - 3.0 score'), (1, '1.0 - 2.0 score')])

    buddy_but = SubmitField("Search Buddy")
    
    select_buddy = RadioField(u'Select',
                              validators=[InputRequired()]
                              )
        
    select_buddy_but = SubmitField("Select Buddy")


class FindBuddyConfirmation(FlaskForm):
    msg = "Invitation has been sent, you will be notified when buddy responds" 

bp = Blueprint('findstudybuddy', __name__, url_prefix='/')

'''
The findBuddy function 
'''
@bp.route('/findstudybuddy', methods=['GET', 'POST'])
@login_required
def findBuddy():
    form = FindBuddyForm()
    si_all = None
    user = User.query.filter_by(id=current_user.id).first()
    form.subject_code.choices = [("", "")] + [(si.course.id, f'{si.course.subject_code} {si.course.course_number} - {si.course.course_name}') 
                                 for si in StudyInterest.query.filter_by(user_id=user.id).all()]
    
    if form.validate_on_submit:
        ''' For all the selected proficiency score range boxes, create a list of filters'''
        scoreFilter = []
        if isinstance(form.prof_select.data, list) and len(form.prof_select.data) > 0:
            scoreFilter = ['(StudyInterest.pro_score >= {}) & (StudyInterest.pro_score <= {} + 1)'.format(score, score) for score in form.prof_select.data]
            filters = [eval(expr) for expr in scoreFilter]
        if len(scoreFilter) > 0:
            si_query = StudyInterest.query.filter(
                and_(StudyInterest.user_id != user.id,
                    StudyInterest.course_id==form.subject_code.data,
                    or_(*filters))                  
                    ).options(joinedload(StudyInterest.course)).options(joinedload(StudyInterest.user))
        else:
            si_query = StudyInterest.query.filter(
                and_(StudyInterest.user_id != user.id,
                    StudyInterest.course_id==form.subject_code.data)                  
                    ).options(joinedload(StudyInterest.course)).options(joinedload(StudyInterest.user))
        

        si_all = si_query.all()
        #print(si_query.statement)
        buddy_receiver_si = StudyInterest.query.filter(
            and_(StudyInterest.user_id == form.select_buddy.data, 
                  StudyInterest.course_id==form.subject_code.data)).first()
        if form.data['select_buddy_but']:
            #Save data in the model           
            buddy_status = BuddyRelation.query.filter_by(buddy_sender=current_user.id, buddy_receiver=form.select_buddy.data, study_interest_id=buddy_receiver_si.id).first()
            if not buddy_status:
                buddy_status = BuddyRelation(buddy_sender=current_user.id, buddy_receiver=form.select_buddy.data, 
                                        study_interest_id=buddy_receiver_si.id,
                                        invitation_status='S')
            else:
                buddy_status.invitation_status ='S'
                db.session.add(buddy_status)
                db.session.commit()
            #Call send invitation 
            #render template to a new template return 
            print(form.select_buddy.data)
            return redirect(url_for('findstudybuddy.findbuddyconfirmation'))
    return render_template('findstudybuddy.html', form=form, si_all=si_all)

@bp.route('/findbuddyconfirmation', methods=['GET'])
def findbuddyconfirmation():
    form = FindBuddyConfirmation()
    return render_template('findbuddyconfirmation.html', form=form, msg=form.msg)