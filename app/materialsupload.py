from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, session, current_app, Flask, send_file
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.dashboard import *
from app.models.document import *
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os


class materialsUploadForm(FlaskForm):
    material_but = SubmitField("Upload")

bp = Blueprint('materialsupload', __name__, url_prefix='/')
@bp.route('/materialsupload', methods=['GET','POST'])
@login_required
def materialsUpload():
    form = materialsUploadForm()
    br_id = int(request.args.get("id"))
    br = BuddyRelation.query.filter_by(id=br_id).first()
    user = User.query.filter_by(username=current_user.username).first()
    buddy = br.get_buddy(current_user.username)
    file_name = ""
    if form.data['material_but']:
        try:
            print("request.files1", request.files)
            file = request.files['file']
            
            if not os.path.exists('app/uploads'):
                os.makedirs('app/uploads')

            if file:
                blob_data = None
                file.save(os.path.join('app/uploads/', secure_filename(file.filename)))
                with open(os.path.join('app/uploads/', secure_filename(file.filename)), "rb") as f:
                    blob_data = bytearray(f.read())
                d = Document(buddy_sender=user.id, buddy_receiver=buddy.id,
                            course_id=br.study_interest.course.id, name=file.filename, content=blob_data)
                db.session.add(d)
                db.session.commit()
                file_name = file.filename
                print("This is the file.filename: ", file.filename)
                '''
                d = Document.query.filter_by(id=4).first()
                with open(os.path.join('uploads/', 'temp.png'), "wb") as f:
                    f.write(d.content)
                '''
                
        except RequestEntityTooLarge:
            return 'File is larger than the 5MB limit.'
        

    return render_template('materialsupload.html', form=form, br=br, buddy=buddy, file_name=file_name)
