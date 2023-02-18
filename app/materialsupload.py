from flask import Blueprint, render_template, url_for, redirect, request, session 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.dashboard import *

class materialsUploadForm(FlaskForm):
    but = SubmitField("Button")

bp = Blueprint('materialsupload', __name__, url_prefix='/')
@bp.route('/materialsupload', methods=['GET', 'POST'])
@login_required
def materialsUpload():
    form = materialsUploadForm()
    return render_template('materialsupload.html', form=form)