from flask import Blueprint, render_template, request, redirect, url_for, flash
import json
from .models import db_helper
import pandas as pd
import re as re

# initialize views
views = Blueprint('views', __name__)

# define db with db_helper class
db = db_helper()

# define main root
@views.route('/')
def dashboard():
    return render_template("base.html")

@views.route('/accounts', methods=['GET'])
def accounts():   
    if request.method == 'GET':
        sql = 'SELECT * FROM `accounts`'
        results = db.database_query(sql)
    return render_template("accounts.html", results=results)

@views.route('/accounts_add', methods=['GET', 'POST'])
def accounts_add():
    if request.method == 'POST':
        account_type = request.form.get('account_type')
        account_description = request.form.get('account_description')
        sql = f"INSERT INTO `accounts`(`account_type`, `account_description`) VALUES ('{account_type}', '{account_description}')"
        db.account_change_query(sql)
        flash('Account added', category='success')
        return redirect(url_for('views.accounts'))

    return redirect(url_for('views.accounts'))

@views.route('/accounts_edit', methods=['GET', 'POST'])
def accounts_edit():
    if request.method == 'POST':
        account_id = request.form.get('account_id')
        account_type = request.form.get('account_type')
        account_description = request.form.get('account_description')
        sql = f"UPDATE `accounts` SET account_type = '{account_type}', account_description = '{account_description}' WHERE account_id = '{account_id}'"
        db.account_change_query(sql)
        flash('Account edited', category='success')
        return redirect(url_for('views.accounts'))
         
    return redirect(url_for('views.accounts'))

@views.route('/accounts_delete', methods=['GET', 'POST'])
def accounts_delete():
    if request.method == 'POST':
        account_id = request.form.get('delete')
        sql = f'DELETE FROM `accounts` WHERE account_id = {account_id}'
        db.account_change_query(sql)
        flash('Account deleted', category='success')
    return redirect(url_for('views.accounts'))


@views.route('/transaction_types', methods=['GET'])
def transaction_types():   
    if request.method == 'GET':
        sql = 'SELECT * FROM `transaction_type`'
        results = db.database_query(sql)
    return render_template("transaction_types.html", results=results)