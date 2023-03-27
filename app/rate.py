from flask import Blueprint, render_template, url_for, redirect, request, session 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.dashboard import *
from app.models.user import User
from app.models.buddyrating import BuddyRating
from wtforms.fields import StringField, SelectField, RadioField, SelectMultipleField
from wtforms.validators import DataRequired, NumberRange
from sqlalchemy.sql import func

def my_bool(str_value):
    if str_value == "No":
        return False
    else:
        return True

def reward_points_calc(form):
    rewards_points = 0
                
    if form.is_score_improved.data == 1:
        rewards_points += 5
                
    if form.is_gained_knowledge.data == 1:
        rewards_points += 5
    '''
    if form.is_score_improved.data == 1 and form.is_gained_knowledge.data == 1:
        rewards_points += 10
    
                
    elif form.is_score_improved.data == 1:
        rewards_points += 5
                
    elif form.is_gained_knowledge.data == 1:
        rewards_points += 5
    '''
    
    return rewards_points

class RateConfirmation(FlaskForm):
    msg = "make sure to check your view ratings page to check on any updates" 

class rateForm(FlaskForm):
    month = SelectField('Duration', validators=[InputRequired()], 
                        choices=[("", ""), (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), 
                                 (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'),
                                 (10, 'October'), (11, 'November'), (12, 'December')])

    year = SelectField('Duration', validators=[InputRequired()], choices=[("", ""), (2023, '2023')])

    is_score_improved = RadioField(u'Did your score improve?',
                          validators=[InputRequired()],
                           choices=[("Yes", "Yes"), ("No", "No")], coerce=my_bool)
    
    is_gained_knowledge = RadioField(u'Did your gain knowledge?',
                          validators=[InputRequired()],
                           choices=[("Yes", "Yes"), ("No", "No")], coerce=my_bool)
    
    buddy_rate = RadioField(u'On a 1-5 scale how would you rate your buddy?',
                          validators=[InputRequired()],
                           choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")])
    
    comment = StringField(validators=[Length(
        min=0, max=50)], render_kw={"placeholder": "Comment"})

    rate_but = SubmitField("Rate")

bp = Blueprint('rate', __name__, url_prefix='/')
@bp.route('/rate', methods=['GET', 'POST'])
@login_required
def rate():
    form = rateForm()
    # read id from query string
    br_id = int(request.args.get("id"))
    # buddy relation model query with id and get the buddy relation object
    # get buddy function of the object model and pass the current user.username
    # pass the buddy relation object to the template
    br = BuddyRelation.query.filter_by(id=br_id).first()
    course_id = br.study_interest.course.id
    user = User.query.filter_by(username=current_user.username).first()
    buddy = br.get_buddy(current_user.username)
    buddy_id = buddy.id
    if form.validate_on_submit:
        if form.data['rate_but']:
            print(form.month.data)
            print(form.year.data)
            print(form.is_score_improved.data)
            print(form.is_gained_knowledge.data)
            
            br_rate = BuddyRating.query.filter_by(buddy_relation_id=br_id, rating_sender=user.id,
                                                  rating_receiver=buddy.id, month=form.month.data, year=form.year.data).first()
            if br_rate:
                br_rate.is_score_improved = form.is_score_improved.data
                br_rate.is_gained_knowledge = form.is_gained_knowledge.data
                br_rate.buddy_rate = form.buddy_rate.data
                br_rate.comment = form.comment.data
                br_rate.is_survey_completed=True
                br_rate.reward_points = reward_points_calc(form)
                              
            else:
                br_rate = BuddyRating(buddy_relation_id=br_id, rating_sender=user.id,
                                    rating_receiver=buddy.id, month=form.month.data, year=form.year.data,
                                    is_score_improved=form.is_score_improved.data, is_gained_knowledge=form.is_gained_knowledge.data,
                                    buddy_rate=form.buddy_rate.data, comment=form.comment.data, 
                                    is_survey_completed=True, reward_points=reward_points_calc(form),
                                    sender_survey_points=5)
            db.session.add(br_rate)
            db.session.commit()
            #br.study_interest.course.course_name
            '''
            BuddyRating.query.filter_by(buddy_relation_id=br_id, rating_sender=current_user.username,
                                        rating_receiver=buddy.username)
            '''
            avg_rating = db.session.query(func.avg(BuddyRating.buddy_rate).label('average')).filter(
                BuddyRating.buddy_relation_id==br_id, 
                BuddyRating.rating_sender==user.id,
                BuddyRating.rating_receiver==buddy.id).scalar()
            
            total_rewards = db.session.query(func.sum(BuddyRating.reward_points).label('sum')).filter(
                BuddyRating.rating_receiver==buddy.id).scalar()
            receiving_user = User.query.filter_by(id=buddy_id).first()
            receiving_user.reward_points = total_rewards

            total_survey_points = db.session.query(func.sum(BuddyRating.sender_survey_points).label('sum')).filter(
                BuddyRating.rating_sender==user.id).scalar()
            #user = User.query.filter_by(id=buddy_id).first()
            user.survey_points = total_survey_points
            
            print(avg_rating)
            si = StudyInterest.query.filter_by(user_id=buddy_id, course_id=course_id).first()
            si.buddy_star_rating = avg_rating
            db.session.add(si)
            db.session.add(user)
            db.session.add(receiving_user)
            db.session.commit()
            return redirect(url_for('rate.rateconfirmation'))
    return render_template('rate.html', form=form, buddy=buddy, br=br)

@bp.route('/rateconfirmation', methods=['GET'])
def rateconfirmation():
    form = RateConfirmation()
    return render_template('rateconfirmation.html', form=form, msg=form.msg)