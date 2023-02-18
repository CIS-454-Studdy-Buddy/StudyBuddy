from flask import Blueprint, render_template, url_for, redirect, request, session 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.dashboard import *

class rateForm(FlaskForm):
    but = SubmitField("Button")

bp = Blueprint('rate', __name__, url_prefix='/')
@bp.route('/rate', methods=['GET', 'POST'])
@login_required
def rate():
    form = rateForm()
    return render_template('rate.html', form=form)