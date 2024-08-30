from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db_helper
import pandas as pd
import re as re

views = Blueprint('views', __name__)
db = db_helper()
@views.route('/')
def dashboard():
    return render_template("base.html")

@views.route('/add_account', methods=['GET', 'POST'])
def account_create():
    if request.method == 'POST':
        account_type = request.form.get('account_type')
        account_description = request.form.get('account_description')
        sql = f"INSERT INTO `accounts`(`account_type`, `account_description`) VALUES ('{account_type}', '{account_description}')"
        if account_type == 'None':
             flash('Must select Account type', category='error')
        elif len(account_description) < 4:
             flash('Account description must be greater than 4 characters', category='error')
        else:
             db.account_change_query(sql)
             flash('Account added', category='success')
             return redirect(url_for('views.Accounts'))

    return render_template("add_account.html")

@views.route('/account_edit', methods=['GET', 'POST'])
def account_edit():
     if request.method == 'POST':
          results = request.form.get('edit')
          print(results)
     return render_template("edit_account.html", results=results)

@views.route('/account_delete', methods=['GET', 'POST'])
def account_delete():
    if request.method == 'POST':
        id = request.form.get('delete')
        sql = f'DELETE FROM `accounts` WHERE account_id = {id}'
        db.account_change_query(sql)
    return redirect(url_for('views.Accounts'))

@views.route('/accounts', methods=['GET', 'POST'])
def Accounts():
        sql = 'SELECT * FROM `accounts`'
        results = db.accounts_query(sql)
        return render_template("accounts.html", results=results)