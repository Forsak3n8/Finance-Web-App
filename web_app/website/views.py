from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db_helper
import pandas as pd
import re as re

# define upload path and allowed extensions for data upload
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@views.route('/transaction_types_edit', methods=['GET', 'POST'])
def transaction_types_edit():
    if request.method == 'POST':
        transaction_type_id = request.form.get('transaction_type_id')
        transaction_type_description = request.form.get('transaction_type_description')
        transaction_is_purchase = request.form.get('transaction_is_purchase')
        sql = f"UPDATE `transaction_type` SET transaction_type_description = '{transaction_type_description}', transaction_is_purchase = '{transaction_is_purchase}' WHERE transaction_type_id = '{transaction_type_id}'"
        db.account_change_query(sql)
        flash('Transaction type edited', category='success')
        return redirect(url_for('views.transaction_types'))
         
    return redirect(url_for('views.transaction_types'))

@views.route('/transaction_types_delete', methods=['GET', 'POST'])
def transaction_types_delete():
    if request.method == 'POST':
        transaction_type_id = request.form.get('delete')
        sql = f'DELETE FROM `transaction_type` WHERE transaction_type_id = {transaction_type_id}'
        db.account_change_query(sql)
        flash('Transaction type deleted', category='success')
    return redirect(url_for('views.transaction_types'))

@views.route('/transaction_types_add', methods=['GET', 'POST'])
def transaction_types_add():
    if request.method == 'POST':
        transaction_type_description = request.form.get('transaction_type_description')
        transaction_is_purchase = request.form.get('transaction_is_purchase')
        sql = f"INSERT INTO `transaction_type`(`transaction_type_description`, `transaction_is_purchase`) VALUES ('{transaction_type_description}', '{transaction_is_purchase}')"
        db.account_change_query(sql)
        flash('Transaction type added', category='success')
        return redirect(url_for('views.transaction_types'))

    return redirect(url_for('views.transaction_types'))

@views.route('/categories', methods=['GET'])
def categories():   
    if request.method == 'GET':
        sql = 'SELECT * FROM `category`'
        results = db.database_query(sql)
    return render_template("categories.html", results=results)

@views.route('/categories_edit', methods=['GET', 'POST'])
def categories_edit():
    if request.method == 'POST':
        category_id = request.form.get('category_id')
        category_description = request.form.get('category_description')
        category_essential = request.form.get('category_essential')
        sql = f"UPDATE `category` SET category_description = '{category_description}', category_essential = '{category_essential}' WHERE category_id = '{category_id}'"
        db.account_change_query(sql)
        flash('Category updated', category='success')
        return redirect(url_for('views.categories'))
    return redirect(url_for('views.categories'))
    
@views.route('/categories_delete', methods=['GET', 'POST'])
def categories_delete():
    if request.method == 'POST':
        category_id = request.form.get('delete')
        sql = f'DELETE FROM `category` WHERE category_id = {category_id}'
        db.account_change_query(sql)
        flash('Category deleted', category='success')
        return redirect(url_for('views.categories'))
    return redirect(url_for('views.categories'))

@views.route('/categories_add', methods=['GET', 'POST'])
def categories_add():
    if request.method == 'POST':
        category_description = request.form.get('category_description')
        category_essential = request.form.get('category_essential')
        sql = f"INSERT INTO `category`(`category_description`, `category_essential`) VALUES ('{category_description}', '{category_essential}')"
        db.account_change_query(sql)
        flash('Category added', category='success')
        return redirect(url_for('views.categories'))
    return redirect(url_for('views.categories'))
    
@views.route('/import_data', methods=['GET'])
def import_data():
    if request.method == 'GET':
        sql = 'SELECT * FROM `accounts`'
        results = db.database_query(sql)
    return render_template("import_data.html", results=results)

@views.route('/import_data_staging', methods=['GET', 'POST'])
def import_data_staging():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
                try:
                    df = pd.read_csv(file)
                    return render_template("import_data_staging.html", df=df)
                except pd.errors.EmptyDataError:
                    flash('File cannot be parsed.', category='error')
                    return redirect(url_for('views.import_data'))
    return redirect(url_for('views.import_data'))