from flask import Blueprint, render_template, request
from .models import db_helper
import pandas as pd

views = Blueprint('views', __name__)
db = db_helper()

@views.route('/')
def dashboard():
    return render_template("base.html")

@views.route('/accounts', methods=['GET', 'POST'])
def Accounts():
    if request.method == 'POST':
        account_type = request.form.get('account_type')
        account_description = request.form.get('account_description')
    print(account_type)
    print(account_description)
    return render_template("accounts.html")