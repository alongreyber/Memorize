import traceback
import bson
from app import app, models, import_scripts
from flask import Flask, request, redirect, jsonify, Response, url_for, flash, Blueprint

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, set_access_cookies, unset_jwt_cookies
)

bp = Blueprint('api', __name__, template_folder='templates')

@bp.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"error": "Missing username parameter"}), 400
    if not password:
        return jsonify({"error": "Missing password parameter"}), 400

    user = models.User.objects(username=username).first()
    if not user:
        return jsonify({"error": "Bad username or password"}), 200
    if not user.check_password(password):
        return jsonify({"error": "Bad username or password"}), 200

    # Identity can be any data that is json serializable
    # Create the tokens we will be sending back to the user
    access_token = create_access_token(identity=str(user.id))

    # Set the JWTs and the CSRF double submit protection cookies
    # in this response
    user_serialized = user.to_mongo()
    del user_serialized['password_hash']
    resp = jsonify({ 'status': 'ok', 'user' : user_serialized })
    set_access_cookies(resp, access_token)
    app.logger.info(
            dict(action='login', user=user.to_mongo()))
    return resp, 200


# Because the JWTs are stored in an httponly cookie now, we cannot
# log the user out by simply deleting the cookie in the frontend.
# We need the backend to send us a response to delete the cookies
# in order to logout. unset_jwt_cookies is a helper function to
# do just that.
@bp.route('/logout')
def logout():
    resp = jsonify({'status': 'ok'})
    unset_jwt_cookies(resp)
    return resp, 200

@bp.route('/users')
@jwt_required
def get_all_users():
    user_id = get_jwt_identity() 
    user = models.User.objects(id=user_id).first()
    if not user.is_admin:
        return jsonify({'error' : 'You do not have permission to view this page'}), 403
    users = models.User.objects()
    return users.to_json()

@bp.route('/user/new', methods=['POST'])
@jwt_required
def new_user():
    user_id = get_jwt_identity() 
    user = models.User.objects(id=user_id).first()
    if not user.is_admin:
        return jsonify({'error' : 'You do not have permission to view this page'}), 403
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    target_user = models.User(
            username=request.json.get('username', None)
            )
    target_user.set_password(request.json.get('password', None))
    target_user.save()
    app.logger.info(
            dict(action='create_user',
                user=user.to_mongo(),
                target_user = target_user.to_mongo()))
    return jsonify({'status' : 'ok'})

### Make a test user
#target_user = models.User(
#        username='alon'
#        )
#target_user.set_password('the3Qguy')
#target_user.save()

@bp.route('/user/<target_user_id>/delete')
@jwt_required
def delete_user(target_user_id):
    user_id = get_jwt_identity() 
    user = models.User.objects(id=user_id).first()
    if not user.is_admin:
        return jsonify({'error' : 'You do not have permission to view this page'}), 403
    target_user = models.User.objects(id=target_user_id).first()
    target_user.delete()
    app.logger.info(
            dict(action='delete_user',
                user=user.to_mongo(),
                target_user = target_user.to_mongo()))
    return jsonify({'status' : 'ok'})

@bp.route('/user/<target_user_id>/setAdmin')
@jwt_required
def set_admin(target_user_id):
    user_id = get_jwt_identity() 
    user = models.User.objects(id=user_id).first()
    if not user.is_admin:
        return jsonify({'error' : 'You do not have permission to view this page'}), 403
    target_user = models.User.objects(id=target_user_id).first()
    admin = request.args.get('admin')
    if admin == 'true':
        target_user.is_admin = True
    else:
        target_user.is_admin = False
    target_user.save()
    app.logger.info(
            dict(action='set_admin',
                user=user.to_mongo(),
                target_user = target_user.to_mongo()))
    return jsonify({'status' : 'ok'})
