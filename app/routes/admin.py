from flask import Flask, Blueprint, render_template, redirect, url_for, flash, get_flashed_messages, request, abort
from app.forms import RegisterForm, LoginForm, CategoryForm, PostForm
from flask_login import login_required
from app.models import Category, Post
from app.functions import queryDate

admin_bp = Blueprint("admin", __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('/admin/dashboard.html')

@admin_bp.route('/dashboard/categories', methods=['GET'])
@login_required
def categories():
    return render_template('/admin/categories.html', form=CategoryForm(), message=get_flashed_messages(), categories=Category().fetch_categories())

@admin_bp.route('/dashboard/add/category', methods=['POST'])
@login_required
def add_category():
    form = CategoryForm()
    if not form.validate_on_submit():
        flash(list(form.errors.values())[0])
        return redirect(url_for('admin.categories'))

    if Category().check_category(request.form.get('category')):
        flash('Category already exists. Please try again')
        return redirect(url_for('admin.categories'))

    Category(cat=request.form.get('category')).add()
    
    return redirect(url_for('admin.categories'))

@admin_bp.route('/dashboard/posts', methods=['GET'])
def posts():
    return render_template('/admin/posts.html', message=get_flashed_messages(), recent=Post().all_posts())

@admin_bp.route('/dashboard/create/post', methods=['GET'])
def create_post():
    return render_template('/admin/create-post.html', form=PostForm(), message=get_flashed_messages())

@admin_bp.route('/dashboard/add/post', methods=['POST'])
def add_post():
    Post(title=request.form.get('title').replace(' ', '-'), category=Category().return_category(request.form.get('category')).cat, status=request.form.get('status'), content=request.form.get('content'), date=queryDate(), last_update=queryDate()).add()

    return redirect(url_for('admin.posts'))

@admin_bp.route('/dashboard/edit/post/<id>', methods=['GET'])
def edit_post(id):
    query = Post().custom_query('id', id)
    if not query:
        return redirect(url_for('admin.dashboard'))

    return render_template('/admin/edit-post.html', form=PostForm(), message=get_flashed_messages(), post=query)

@admin_bp.route('/dashboard/edit/post/<id>/submit', methods=['POST'])
def update_post(id):
    Post().update(id, request.form.get('title'), Category().return_category(request.form.get('category')).cat, request.form.get('status'), request.form.get('content'), queryDate())
    flash('Post succesfully updated')
    return redirect(url_for('admin.edit_post', id=id))
    
@admin_bp.route('/dashboard/preview/post', methods=['GET'])
def preview_post():
    return render_template('/main/post.html', categories=Category().fetch_categories(), new=Post().last_submission())

@admin_bp.route('/dashboard/delete/<id>', methods=['GET'])
def delete_post(id):
    query = Post().custom_query('id', id)
    if not query:
        return redirect(url_for('admin.posts'))
    Post().delete(id)
    
    flash(f'{query.title} has been deleted.')
    return redirect(url_for('admin.posts'))