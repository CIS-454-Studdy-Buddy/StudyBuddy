from flask import Blueprint, render_template, url_for, redirect, request, session 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from app.auth import *
from app.dashboard import *
from app.models.user import User
from app.models.buddyrating import BuddyRating
from sqlalchemy import desc

class viewRatingsForm(FlaskForm):
    view_rating_but = SubmitField("Button")

bp = Blueprint('viewratings', __name__, url_prefix='/')
@bp.route('/viewratings', methods=['GET', 'POST'])
@login_required
def viewRatings():
    form = viewRatingsForm()
    user = User.query.filter_by(username=current_user.username).first()
    buddy_rating = BuddyRating.query.filter_by(rating_receiver=user.id).order_by(desc(BuddyRating.rating_date)).all()
    return render_template('viewratings.html', form=form, buddy_rating=buddy_rating)