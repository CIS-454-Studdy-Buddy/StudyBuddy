from flask import Blueprint, render_template, url_for, redirect, request, session 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.dashboard import *

class subjectSelectionForm(FlaskForm):
    but = SubmitField("Button")

bp = Blueprint('subjectselection', __name__, url_prefix='/')
@bp.route('/subjectselection', methods=['GET', 'POST'])
@login_required
def subjectSelection():
    form = subjectSelectionForm()
    return render_template('subjectselection.html', form=form)