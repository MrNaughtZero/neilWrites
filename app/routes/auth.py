from flask import Flask, Blueprint, render_template, redirect, url_for, flash, get_flashed_messages, request, abort
from flask_login import login_required, login_user, logout_user, current_user
from app.models import Admin
from app.forms import RegisterForm, LoginForm

auth_bp = Blueprint("auth", __name__)

# @auth_bp.route('/auth/register', methods=['GET'])
# def register():
#     if Admin().check_for_admin():
#         return abort(404)
#     return render_template('/auth/register.html', form=RegisterForm(), message=get_flashed_messages())

# @auth_bp.route('/auth/add/admin', methods=['POST'])
# def add_admin():
#     form = RegisterForm()
#     if not form.validate_on_submit():
#         flash(list(form.errors.values())[0])
#         return redirect(url_for('auth.register'))
    
#     new_admin = Admin(username=request.form.get('username'), password=request.form.get('password')).create_user()
#     if not new_admin:
#         flash('Something went wrong. Please try again.')
#         return redirect(url_for('auth.register'))

#     login_user(new_admin)
#     return redirect(url_for('admin.dashboard'))

# Above is commented out to prevent a new user registering once the first admin is registered.

@auth_bp.route('/auth/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    return render_template('/auth/login.html', form=LoginForm(), message=get_flashed_messages())

@auth_bp.route('/auth/login/attempt', methods=['POST'])
def login_attempt():
    usr = Admin().login_attempt(request.form.get('username'), request.form.get('password'))
    if not usr:
        flash('Incorrect Login Details.')
        return redirect(url_for('auth.login'))
    
    login_user(usr)
    return redirect(url_for('admin.dashboard'))

@auth_bp.route('/auth/logout', methods=['GET'])
def logout():
    if not current_user.is_authenticated:
        return abort(404)
    logout_user()
    return redirect(url_for('auth.login'))

