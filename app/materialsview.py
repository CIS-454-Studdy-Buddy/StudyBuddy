from flask import Blueprint, render_template, url_for, redirect, request, session 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.dashboard import *

class materialsViewForm(FlaskForm):
    but = SubmitField("Button")

bp = Blueprint('materialsview', __name__, url_prefix='/')
@bp.route('/materialsview', methods=['GET', 'POST'])
@login_required
def materialsView():
    form = materialsViewForm()
    return render_template('materialsview.html', form=form)