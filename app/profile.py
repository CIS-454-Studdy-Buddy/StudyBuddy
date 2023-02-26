from flask import Blueprint, render_template, url_for, redirect, request, session 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.dashboard import *
from app.inbox import *
import flask_login


class profileForm(FlaskForm):
    homeButton = SubmitField("Home")
    inboxButton = SubmitField("Inbox")
    logoutButton = SubmitField("Logout")
    saveButton = SubmitField("Save")
    phoneNumber = StringField(validators=[Length(
        min=0, max=15)],render_kw={"placeholder": "Phone Number"})
    aboutMe = StringField(validators=[Length(
        min=0, max=50)], render_kw={"placeholder": "About Me"})

bp = Blueprint('profile', __name__, url_prefix='/')
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = profileForm()
    msg = ""
    user = User.query.filter_by(username=current_user.username).first()
    if user:
        
        if request.method == 'GET':
            form.phoneNumber.data = user.phone_number
            form.aboutMe.data = user.about_me
        print((len(form.phoneNumber.data) > 15) or (not form.phoneNumber.data.isnumeric()))
        if form.data['saveButton']:
            # phoneNumber and aboutMe are optional fields
           
            # if phone number is too long or is invalid, send message to user
            if len(form.phoneNumber.data) > 15:
                msg = "Invalid phone number must be less than 15 characters"
                return render_template('profile.html', form=form, msg=msg)
            
            if form.phoneNumber.data and not form.phoneNumber.data.isnumeric():
                msg = "Invalid phone number, please use digits"
                return render_template('profile.html', form=form, msg=msg)
            
            
            if len(form.aboutMe.data) >= 50:
                msg = "Invalid, the maximum character limit for about me description is 50"
                return render_template('profile.html', form=form, msg=msg)
                        
            
            user.phone_number = form.phoneNumber.data
            user.about_me = form.aboutMe.data
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('profile.profile'))
                     

        elif form.data['homeButton']:
            return redirect(url_for('dashboard.dashboard'))

        elif form.data['inboxButton']:
            return redirect(url_for('inbox.inbox'))

        elif form.data['logoutButton']:
            return redirect(url_for('auth.login'))

    return render_template('profile.html', form=form, msg=msg)
