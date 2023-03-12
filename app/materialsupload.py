from flask import Blueprint, render_template, url_for, redirect, request, session, current_app, Flask
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
    if form.data['material_but']:
        try:
            print(request.files)
            file = request.files['file']
            
            if file:
                blob_data = None
                file.save(os.path.join('uploads/', secure_filename(file.filename)))
                with open(os.path.join('uploads/', secure_filename(file.filename)), "rb") as f:
                    blob_data = bytearray(f.read())
                d = Document(buddy_sender=user.id, buddy_receiver=buddy.id,
                            course_id=br.study_interest.course.id, content=blob_data)
                db.session.add(d)
                db.session.commit()
                '''
                d = Document.query.filter_by(id=4).first()
                with open(os.path.join('uploads/', 'temp.png'), "wb") as f:
                    f.write(d.content)
                '''
                
        except RequestEntityTooLarge:
            return 'File is larger than the 5MB limit.'
    
    return render_template('materialsupload.html', form=form, br=br, buddy=buddy)

@bp.route('/upload', methods=['POST'])
def upload():
    
    br_id = int(request.args.get("id"))
    br = BuddyRelation.query.filter_by(id=br_id).first()
    user = User.query.filter_by(username=current_user.username).first()
    buddy = br.get_buddy(current_user.username)

    try:
        file = request.files['file']

        if file:
            d = Document(buddy_sender=user.id, buddy_receiver=buddy.id,
                          course_id=br.study_interest.course.id)
            db.session.add(d)
            db.session.commit()
            file.save(os.path.join('uploads/', secure_filename(file.filename)))

    except RequestEntityTooLarge:
        return 'File is larger than the 5MB limit.'
    
    return redirect(url_for('materialsupload.materialsUpload'))

