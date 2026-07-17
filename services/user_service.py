from database import db
from models.user_model import User
from utils.validators import is_valid_email
from sqlalchemy import or_

def create_user(name, email, role):
    user = User(
        name=name,
        email=email,
        role=role
    )

    db.session.add(user)
    db.session.commit()

    return user
def get_all_users():
    return User.query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def search_users(search):
    return User.query.filter(
        or_(
            User.name.ilike(f"%{search}%"),
            User.email.ilike(f"%{search}%")
        )
    ).all()

def get_users_paginated(page, limit):
    return User.query.paginate(
        page=page,
        per_page=limit,
        error_out=False
    )