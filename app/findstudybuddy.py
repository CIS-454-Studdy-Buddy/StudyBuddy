from flask import Blueprint, render_template, url_for, redirect, request, session 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.dashboard import *

class FindBuddyForm(FlaskForm):
    but = SubmitField("Button")

bp = Blueprint('findstudybuddy', __name__, url_prefix='/')
@bp.route('/findstudybuddy', methods=['GET', 'POST'])
@login_required
def findBuddy():
    form = FindBuddyForm()
    return render_template('findstudybuddy.html', form=form)