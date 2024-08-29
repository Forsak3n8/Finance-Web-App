from flask import Blueprint, render_template, request, redirect, url_for
from .models import db_helper
import pandas as pd

views = Blueprint('views', __name__)
db = db_helper()

@views.route('/')
def dashboard():
    return render_template("base.html")

@views.route('/account_delete', methods=['GET', 'POST'])
def account_delete():
     if request.method == 'POST':
          id = request.form.get('delete')
          sql = f'DELETE FROM `accounts` WHERE account_id = {id}'
          db.account_delete_query(sql)
     return redirect(url_for('views.Accounts'))

@views.route('/accounts', methods=['GET', 'POST'])
def Accounts():
        sql = 'SELECT * FROM `accounts`'
        results = db.accounts_query(sql)
        if request.method == 'POST':
            account_type = request.form.get('account_type')
            account_description = request.form.get('account_description')
            print(account_type)
            print(account_description)
        return render_template("accounts.html", results=results)