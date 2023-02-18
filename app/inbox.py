from flask import Blueprint, render_template, url_for, redirect, request, session 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.dashboard import *

class InboxForm(FlaskForm):
    but = SubmitField("Button")

bp = Blueprint('inbox', __name__, url_prefix='/')

@bp.route('/inbox', methods=['GET', 'POST'])
@login_required
def inbox():
    form = InboxForm()
    return render_template('inbox.html', form=form)