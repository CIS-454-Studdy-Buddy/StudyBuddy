from flask import Blueprint, render_template, url_for, redirect, request, session , send_file
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.dashboard import *
from app.models.document import *
from io import BytesIO

class materialsViewForm(FlaskForm):
    material_view_but = SubmitField("Button")

bp = Blueprint('materialsview', __name__, url_prefix='/')
@bp.route('/materialsview', methods=['GET', 'POST'])
@login_required
def materialsView():
    form = materialsViewForm()
    user = User.query.filter_by(username=current_user.username).first()
    list_of_doc = Document.query.filter_by(buddy_receiver=user.id).all()
    return render_template('materialsview.html', form=form, list_of_doc=list_of_doc)

@bp.route('/docView', methods=['GET'])
@login_required
def docView():
    doc_id = request.args.get("id")
    user = User.query.filter_by(username=current_user.username).first()
    doc = Document.query.filter_by(id=doc_id).first()
    return send_file(BytesIO(doc.content), as_attachment=True, download_name=doc.name)