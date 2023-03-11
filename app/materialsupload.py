from flask import Blueprint, render_template, url_for, redirect, request, session, current_app, Flask
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.dashboard import *
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os



class materialsUploadForm(FlaskForm):
    but = SubmitField("Button")

bp = Blueprint('materialsupload', __name__, url_prefix='/')
@bp.route('/materialsupload', methods=['GET','POST'])
@login_required
def materialsUpload():
    form = materialsUploadForm()

    return render_template('materialsupload.html', form=form)

@bp.route('/upload', methods=['POST'])
def upload():

    try:
        file = request.files['file']

        if file:
            file.save(os.path.join('uploads/', secure_filename(file.filename)))

    except RequestEntityTooLarge:
        return 'File is larger than the 5MB limit.'


    return redirect(url_for('materialsupload.materialsUpload'))

