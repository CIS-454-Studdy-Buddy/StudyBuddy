from flask import Blueprint, render_template, url_for, redirect, request, session, jsonify 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from wtforms import StringField, SelectField
from app.auth import *
from app.dashboard import *
from app.models.course import *

class SubjectSelectionForm(FlaskForm):
    save_button = SubmitField("Selection Save")

class SubjectSearchForm(FlaskForm):

    subject_code = SelectField('Subject Code', choices=[])
    course_title = SelectField('Course Title', choices=[])

bp = Blueprint('subjectselection', __name__, url_prefix='/')

@bp.route('/subjectselection', methods=['GET', 'POST'])
@login_required
def subjectSelection():
    form = SubjectSelectionForm()
    subject_search_form = SubjectSearchForm()
    subject_search_form.subject_code.choices = [(SubjectCode.subject_code, f'({SubjectCode.subject_code}) {SubjectCode.subject_name}') for SubjectCode in SubjectCode.query.all()]

    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=current_user.username).first()
    #     if user:
    #         # TODO
    #         print("TODO")

    #      if form.data['save_button']:
    #          selected_code = subject_search_form.subject_code.data
    #          selected_course = subject_search_form.course_title.data
    #          return f'The current selected value is: {selected_code} {selected_course}'

    return render_template('subjectselection.html', form=form, subject_search_form=subject_search_form)

@bp.route('/subjectselection/<get_code>', methods=['GET', 'POST'])
@login_required
def codesortcourse(get_code):
    course = Courses.query.filter_by(subject_code=get_code).all()
    course_array = []
    for code in course:
        course = {}
        course['code'] = code.subject_code
        course['number'] = code.course_number
        course['name'] = code.course_name
        course_array.append(course)
    return jsonify({'courselist': course_array})
