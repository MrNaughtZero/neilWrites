from flask import Flask, Blueprint, render_template, redirect, url_for, abort
from app.models import Category, Post

main_bp = Blueprint("main", __name__)

@main_bp.route('/', methods=['GET'])
def index():
    return render_template('/main/index.html', categories=Category().fetch_categories(), posts=Post().all_posts(), new=Post().last_submission())

@main_bp.route('/<string:title>', methods=['GET'])
def view_post(title):
    query = Post().custom_query('title', title)
    
    if not query:
        return abort(404)
    return render_template('/main/post.html', post=query, categories=Category().fetch_categories(), new=Post().last_submission())

@main_bp.route('/category/<string:category>', methods=['GET'])
def category_page(category):
    query = Post().posts_by_category(category)
    if not query:
        return redirect(url_for('main.index'))
    return render_template('/main/index.html', posts=query, categories=Category().fetch_categories(), new=Post().last_submission())