from flask import Blueprint, render_template, request, url_for, redirect

from model.myDB import model_create, model_read, model_update, model_delete, model_query_all, model_query_emails, \
    model_query_phones

model_bp = Blueprint('model', __name__,
                     url_prefix='/model',
                     template_folder='templates',
                     static_folder='static',
                     static_url_path='assets')


# connects default URL to a function
@model_bp.route('/crud')
def crud():
    """convert Users table into a list of dictionary rows"""
    records = model_query_all()
    return render_template("model/crud.html", table=records)


# create/add a new record to the table
@model_bp.route('/create/', methods=["POST"])
def create():
    if request.form:
        """extract data from form"""
        user_dict = {'name': request.form.get("name"),
                     'email': request.form.get("email"),
                     'password': request.form.get("password"),
                     'phone': request.form.get("phone")}
        # model_create expects: username, password, email, phone
        model_create(user_dict)
    return redirect(url_for('model.crud'))


# CRUD read, which is filtering table based off of ID
@model_bp.route('/read/', methods=["POST"])
def read():
    record = []
    if request.form:
        userid = request.form.get("ID")
        # model_read expects userid
        user_dict = model_read(userid)
        # model_read returns: username, password, email, phone
        record = [user_dict]  # placed in list for compatibility with index.html
    return render_template("model/crud.html", table=record)


# CRUD update
@model_bp.route('/update/', methods=["POST"])
def update():
    if request.form:
        user_dict = {
            'userid': request.form.get("ID"),
            'email': request.form.get("email"),
            'phone': request.form.get("phone")
        }
        # model_update expects userid, email, phone
        model_update(user_dict)
    return redirect(url_for('model.crud'))


# CRUD delete
@model_bp.route('/delete/', methods=["POST"])
def delete():
    if request.form:
        """fetch userid"""
        userid = request.form.get("ID")
        model_delete(userid)
    return redirect(url_for('model.crud'))


# if email url, show the email table only
@model_bp.route('/emails/')
def emails():
    # fill the table with emails only
    records = model_query_emails()
    return render_template("model/crud.html", table=records)


# if phones url, show phones table only
@model_bp.route('/phones/')
def phones():
    # fill the table with phone numbers only
    records = model_query_phones()
    return render_template("model/crud.html", table=records)


