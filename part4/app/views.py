from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/index.html')
def index_alias():
    return render_template('index.html')

@main_bp.route('/login.html')
def login():
    return render_template('login.html')
