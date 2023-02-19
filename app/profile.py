from flask import Blueprint, render_template, url_for, redirect, request, session 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.dashboard import *
from app.inbox import *

class profileForm(FlaskForm):
    homeButton = SubmitField("Home")
    inboxButton = SubmitField("Inbox")
    logoutButton = SubmitField("Logout")
    saveButton = SubmitField("Save")
    firstName = "James"
    lastName = "Smith"
    username = "jsmith@syr.edu"
    phoneNumber = StringField(validators=[InputRequired(), Email(granular_message="invalid phone number"), Length(
        min=0, max=15)], render_kw={"placeholder": "Phone Number"})
    aboutMe = StringField(validators=[InputRequired(), Email(granular_message="invalid about me input"), Length(
        min=0, max=50)], render_kw={"placeholder": "About Me"})

    

bp = Blueprint('profile', __name__, url_prefix='/')
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = profileForm()
    if form.validate_on_submit():
        if form.data['homeButton']:
            return redirect(url_for('dashboard.dashboard'))
        elif form.data['inboxButton']:
            return redirect(url_for('inbox.inbox'))
        elif form.data['logoutButton']:
            return redirect(url_for('auth.login'))

    return render_template('profile.html', form=form)