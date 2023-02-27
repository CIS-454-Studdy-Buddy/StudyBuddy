from flask import Blueprint, render_template, url_for, redirect, request, session 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.inbox import *
from app.models.studyinterest import *
from sqlalchemy.orm import joinedload

class DashboardForm(FlaskForm):
    inboxBut = SubmitField("Inbox")
    findBuddyBut = SubmitField("Find a Study Buddy")
    subjectSelBut = SubmitField("Subject Selection")
    matUploadBut = SubmitField("Materials Upload")
    matViewBut = SubmitField("Materials View")
    rateBut = SubmitField("Rate")
    viewRateBut = SubmitField("View Ratings")
    profileBut = SubmitField("Profile")
    logoutBut = SubmitField("Logout")

bp = Blueprint('dashboard', __name__, url_prefix='/')

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = DashboardForm()
    if form.validate_on_submit():
        if form.data['inboxBut']:
            return redirect(url_for('inbox.inbox'))   
        elif form.data['findBuddyBut']:
            return redirect(url_for('findstudybuddy.findBuddy'))  

        elif form.data['subjectSelBut']:
            return redirect(url_for('subjectselection.subjectSelection')) 

        elif form.data['matUploadBut']:
            return redirect(url_for('materialsupload.materialsUpload'))

        elif form.data['matViewBut']:
            return redirect(url_for('materialsview.materialsView'))

        elif form.data['rateBut']:
            return redirect(url_for('rate.rate'))

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
        print(si_all)
    return render_template('dashboard.html', form=form, si_all=si_all)

    