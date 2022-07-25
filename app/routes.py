from flask import current_app as app
from flask import request, render_template, redirect, url_for, send_from_directory
from .models import db, WebUserForm


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        appeal = request.form.get('type_appeal')
        message = request.form.get('message')
        user = WebUserForm(username=name, email=email, type_appeal=appeal, message=message)
        db.session.add(user)
        db.session.commit()
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



