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
    phoneNumber = StringField(render_kw={"placeholder": "Phone Number"})
    aboutMe = StringField(render_kw={"placeholder": "About Me"})


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

        if form.data['saveButton']:
            # phoneNumber and aboutMe are optional fields
            # if phone number and about me are not changed, do not update user's fields
            if ((form.phoneNumber.data == "") and (form.aboutMe.data == "")):
                msg = "Phone number and about me description not changed"
                return redirect(url_for('dashboard.dashboard'))
            # phone number is not changed and aboutMe is changed, update the user's about me description
            elif ((form.phoneNumber.data == "") and (form.aboutMe.data != "")):
                user.about_me = form.aboutMe.data
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('dashboard.dashboard'))
            # about me is not changed and phone number is changed, update the user's phone number
            elif ((form.phoneNumber.data != "") and (form.aboutMe.data == "")):
                user.phone_number = form.phoneNumber.data
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('dashboard.dashboard'))

            # phone number and about me fields are changed, so update both field for the user
            elif (((len(form.phoneNumber.data) <= 15) and form.phoneNumber.data.isnumeric()) and (len(form.aboutMe.data) <= 50)):
                msg = "Valid phone number and about me description"
                user.phone_number = form.phoneNumber.data
                user.about_me = form.aboutMe.data
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('dashboard.dashboard'))

            # if phone number is too long or is invalid, send message to user
            elif ((len(form.phoneNumber.data) > 15) or (not form.phoneNumber.data.isnumeric())):
                msg = "Invalid phone number, please use digits"

            else:
                msg = "Invalid, the maximum character limit for about me description is 50"

        elif form.data['homeButton']:
            return redirect(url_for('dashboard.dashboard'))

        elif form.data['inboxButton']:
            return redirect(url_for('inbox.inbox'))

        elif form.data['logoutButton']:
            return redirect(url_for('auth.login'))

    return render_template('profile.html', form=form, msg = msg)