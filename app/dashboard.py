from flask import Blueprint, render_template, url_for, redirect, request, session 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.inbox import *

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
        #elif form.data['findBuddyBut']:
        #    return

        #elif form.data['subjectSelBut']:
        #    return

        #elif form.data['matUploadBut']:
        #    return

        #elif form.data['matViewBut']:
        #    return

        #elif form.data['rateBut']:
        #    return

        #elif form.data['viewRateBut']:
        #    return

        #elif form.data['profileBut']:
        #    return
        
        elif form.data['logoutBut']:
            return redirect(url_for('auth.login'))

        
    return render_template('dashboard.html', form=form)