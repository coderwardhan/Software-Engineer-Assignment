from flask import Blueprint, request
from services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id,
    get_user_by_email,
    search_users,
    get_users_paginated

)

user_bp = Blueprint("users", __name__)

@user_bp.route("/users", methods=["POST"])
def add_user():

    data = request.get_json()

    # Required fields
    if not data.get("name") or not data.get("email") or not data.get("role"):
        return {
            "success": False,
            "error": "Name, email and role are required"
        }, 400

    from utils.validators import is_valid_email

    if not is_valid_email(data["email"]):
        return {
            "success": False,
            "error": "Invalid email format"
        }, 400

    if get_user_by_email(data["email"]):
        return {
            "success": False,
            "error": "Email already exists"
        }, 409

    user = create_user(
        data["name"],
        data["email"],
        data["role"]
    )

    return {
        "success": True,
        "data": user.to_dict()
    }, 201


@user_bp.route("/users", methods=["GET"])
def get_users():

    search = request.args.get("search")

    page = request.args.get("page", type=int)
    limit = request.args.get("limit", type=int)

    if search:
        users = search_users(search)

        return {
            "success": True,
            "data": [user.to_dict() for user in users]
        }, 200

    if page and limit:

        result = get_users_paginated(page, limit)

        return {
            "success": True,
            "page": page,
            "limit": limit,
            "total": result.total,
            "data": [user.to_dict() for user in result.items]
        }, 200

    users = get_all_users()

    return {
        "success": True,
        "data": [user.to_dict() for user in users]
    }, 200