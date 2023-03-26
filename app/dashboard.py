from flask import Blueprint, render_template, url_for, redirect, request, session 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.models.studyinterest import *
from app.models.buddyrelation import *
from sqlalchemy.orm import joinedload
from sqlalchemy import and_ , or_

class DashboardForm(FlaskForm):
    findBuddyBut = SubmitField("Buddy Search")
    subjectSelBut = SubmitField("Subject Select")
    matViewBut = SubmitField("View Materials")
    viewRateBut = SubmitField("View Ratings")
    profileBut = SubmitField("Profile")
    logoutBut = SubmitField("Logout")

bp = Blueprint('dashboard', __name__, url_prefix='/')

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = DashboardForm()
    if form.validate_on_submit(): 
        if form.data['findBuddyBut']:
            return redirect(url_for('findstudybuddy.findBuddy'))  

        elif form.data['subjectSelBut']:
            return redirect(url_for('subjectselection.subjectSelection')) 

        elif form.data['matViewBut']:
            return redirect(url_for('materialsview.materialsView'))

        elif form.data['viewRateBut']:
            return redirect(url_for('viewratings.viewRatings'))

        elif form.data['profileBut']:
            return redirect(url_for('profile.profile'))
        
        elif form.data['logoutBut']:
            return redirect(url_for('auth.login'))

    si_all = None
    user = User.query.filter_by(username=current_user.username).first()
    if user:
        si_all = StudyInterest.query.filter_by(user_id=user.id).options(joinedload(StudyInterest.course)).all()
        br = BuddyRelation.query.filter_by(buddy_receiver=user.id, invitation_status='S')
        br_connections = BuddyRelation.query.filter(or_(BuddyRelation.buddy_receiver==user.id, BuddyRelation.buddy_sender==user.id), BuddyRelation.invitation_status=='A').all()
    else:
        print("********")
        print(current_user.username)
    return render_template('dashboard.html', form=form, si_all=si_all, br=br, br_connections=br_connections, user=user)


   



    