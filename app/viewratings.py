from flask import Blueprint, render_template, url_for, redirect, request, session 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.dashboard import *

class viewRatingsForm(FlaskForm):
    but = SubmitField("Button")

bp = Blueprint('viewratings', __name__, url_prefix='/')
@bp.route('/viewratings', methods=['GET', 'POST'])
@login_required
def viewRatings():
    form = viewRatingsForm()
    return render_template('viewratings.html', form=form)