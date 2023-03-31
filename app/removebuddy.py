from flask import Blueprint, render_template, url_for, redirect, request, session 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.dashboard import *
import flask_login
from app.models.studyinterest import *


class RemoveBuddyForm(FlaskForm):
    remove_but = SubmitField("Yes")
    dont_remove_but = SubmitField("No")


bp = Blueprint('removebuddy', __name__, url_prefix='/')

@bp.route('/removebuddy', methods=['GET', 'POST'])
@login_required
def removeBuddy():
    form = RemoveBuddyForm()
    # read id from query string
    br_id = int(request.args.get("id"))
    br = BuddyRelation.query.filter_by(id=br_id).first()
    user = User.query.filter_by(username=current_user.username).first()
    if br is None:
        return redirect(url_for('dashboard.dashboard'))
    if user:
        if user.id != br.buddy_sender and user.id != br.buddy_receiver:
            return redirect(url_for('dashboard.dashboard'))
        else:
            if form.validate_on_submit():
                if form.data['remove_but']:
                    # remove buddy
                    #print(br)
                    #print(BuddyRelation.id)
                    #print(BuddyRelation.id == br_id)
                    si = StudyInterest.query.filter_by(id=br.study_interest_id).first()
                    course_id = si.course.id
                    if user.id == br.buddy_sender:
                        si.buddy_status = 'N'
                        si = StudyInterest.query.filter_by(user_id = br.buddy_receiver).filter_by(course_id = course_id).first()
                        si.buddy_status = 'N'
                    elif user.id == br.buddy_receiver:
                        si.buddy_status = 'N'
                        si = StudyInterest.query.filter_by(user_id = br.buddy_sender).filter_by(course_id = course_id).first()
                        si.buddy_status = 'N'
                
                    db.session.query(BuddyRelation).filter(BuddyRelation.id == br_id).delete()
                    db.session.commit()

                    return redirect(url_for('dashboard.dashboard'))

                elif form.data['dont_remove_but']:
                    # dont remove buddy, redirect to dashboard
                    return redirect(url_for('dashboard.dashboard'))
    else:
        print("********")
        print(current_user.username)


    

    return render_template('removebuddy.html', br=br, form=form)