'''
Author: Talal Hakki
'''
from flask import Blueprint, render_template, url_for, redirect, request, session 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *

'''
This is a form class for the contactForm 
'''
class contactForm(FlaskForm):
    firstName = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "First Name"})
    lastName = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Last Name"})
    email = StringField(validators=[InputRequired(), Email(granular_message="invalid email address"), Length(
        min=4, max=20)], render_kw={"placeholder": "Email"})
    comments = StringField(validators=[InputRequired(), Length(
        min=4, max=100)], render_kw={"placeholder": "Comments (<=100 characters)"})
    sendButton = SubmitField("Send")

bp = Blueprint('contactus', __name__, url_prefix='/')

@bp.route('/contactus', methods=['GET', 'POST'])
def contactUs():
    form = contactForm()
    if form.validate_on_submit():
        if form.data['sendButton']:
            return redirect(url_for('auth.home'))
        
    return render_template('contactus.html', form=form)


