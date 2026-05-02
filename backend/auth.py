from flask import Blueprint, render_template, request, redirect, url_for, flash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')