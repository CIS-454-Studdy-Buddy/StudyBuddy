from flask import Blueprint, render_template, url_for, redirect, request, session 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, validators
from wtforms.validators import InputRequired, Length, ValidationError, Email
from flask_bcrypt import Bcrypt
from app.models.user import User
from app.extensions import db, bcrypt, login_manager, email
from flask_mail import Message
import random  


bp = Blueprint('auth', __name__, url_prefix='/')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class RegisterForm(FlaskForm):
    first_name = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "First Name"})
    
    last_name = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Last Name"})
                             
    username = StringField(validators=[InputRequired(), Email(granular_message="invalid email address"), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
            min=4, max=20)], render_kw={"placeholder": "Password"})
    
    re_enter_password = PasswordField('Re-enter Password',[validators.DataRequired(),validators.Length(
        min=4, max=20)], render_kw={"placeholder": "Re-enter New Password"})

    submit = SubmitField("SignUp")

    def validate_username(self, username):
        if not username.data.endswith("@syr.edu"):
            raise ValidationError("email address must syracuse university email address")
        existing_user_username = User.query.filter_by(
            username=username.data).first()

        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one.")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login") 


class ForgotForm(FlaskForm):
     username = StringField(validators=[InputRequired(), Email(granular_message="invalid email address"), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
     submit = SubmitField("Submit")

class PasswordResetForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Email(granular_message="invalid email address"), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField('New Password',[validators.DataRequired(),validators.Length(
        min=4, max=20)], render_kw={"placeholder": "New Password"})
    re_enter_password = PasswordField('Re-enter Password',[validators.DataRequired(),validators.Length(
        min=4, max=20)], render_kw={"placeholder": "Re-enter New Password"})
    submit = SubmitField("Submit")

class EmailConfimation(FlaskForm):
    msg = "Please check your email to confirm validity"  

class ForgotConfimation(FlaskForm):
    msg = "Please check your email for a link to reset password"

@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    msg = ""
    form = PasswordResetForm()
    if form.validate_on_submit():
        if form.password.data == form.re_enter_password.data:
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                ## TODO replace old password with new password in database
                hash_pass = bcrypt.generate_password_hash(form.password.data)
                User.query.filter_by(username=form.username.data).update(dict (password=hash_pass))
                db.session.commit()
                msg = "Success, passwords match."
                return redirect(url_for('auth.login'))
            else:
                msg = "Invalid username, try again."
                
        else:
            msg = "Passwords do not match, try again."
    return render_template('reset_password.html', form = form, msg = msg)
            


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    msg = ""
    if form.validate_on_submit():
        if form.password.data == form.re_enter_password.data:
            html_msg = email_content_email_confirmation(username=form.username.data, 
                                                email_confirmation=url_for('auth.login', _external=True))
            send_email(email_address=form.username.data, msg_html=html_msg)
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(first_name=form.first_name.data, last_name=form.last_name.data,  
                            username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.emailconfirmation'))
        else:
            msg = "Passwords do not match, try again."
    return render_template('register.html', form=form, msg=msg)

@bp.route('/emailconfirmation', methods=['GET'])
def emailconfirmation():
    form = EmailConfimation()
    return render_template('emailconfimation.html', form=form, msg=form.msg)


@bp.route('/login', methods=['GET','POST'])
def login():
    msg = ""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard.dashboard'))
            else:
                msg = "Invalid Login"
        else:
            msg = "Invalid Login" 
    return render_template('login.html', form=form, msg=msg)


@bp.route('/')
def home():
    return render_template('home.html')


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('auth.login'))

@bp.route('/forgot', methods=['GET', 'POST'])
def forgot():
    form = ForgotForm() 
    if form.validate_on_submit():
        html_msg = email_content_password_reset(username=form.username.data, 
                                                reset_password_url=url_for('auth.reset_password', _external=True))
        
        send_email(email_address=form.username.data, msg_html=html_msg)
        
        return redirect(url_for('auth.forgotconfirmation'))
        
    return render_template('forgot.html', form=form)

@bp.route('/forgotconfirmation', methods=['GET'])
def forgotconfirmation():
    form = ForgotConfimation()
    return render_template('forgotconfimation.html', form=form, msg=form.msg)

def send_email(email_address, msg_html):
    msg = Message(
                'Hello',
                sender ='su.study.buddy@gmail.com',
                recipients = [email_address]
               )
    msg.body = 'Hello Flask message sent from Flask-Mail'
    msg.html = msg_html 
    email.send(msg)
    return 'Sent'

def email_content_password_reset(username, reset_password_url):
    msg_non_html = ""
    #reset_password_url = url_for('auth.reset_password')
    token =  random.randint(10**9,10**10)
    url = f"{reset_password_url}?t={token}"
    html_msg = f'<b>Hey {username}</b>, sending you this email from my <a href="{url}">Study Buddy App</a>'
    return html_msg

def email_content_email_confirmation(username, email_confirmation):
    token =  random.randint(10**9,10**10)
    url = f"{email_confirmation}?t={token}"
    html_msg = f'<b>Hey {username}</b>, sending you this email from my <a href="{url}">Study Buddy App</a>'
    return html_msg
