from . import db


class WebUserForm(db.Model):
    __tablename__ = 'web_user_form'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), index=True)
    email = db.Column(db.String(150), nullable=True)
    type_appeal = db.Column(db.String(150), nullable=True)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='new')

