import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# db_drop_and_create_all()

# ROUTES


@app.route('/drinks', methods=['GET'])
def retrieve_drinks():

    drinks = Drink.query.all()
    drinks_formatted = [drink.short() for drink in drinks]

    if len(drinks_formatted) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'drinks': drinks_formatted
    })


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def retrieve_drinks_details():
    drinks = Drink.query.all()
    drinks_formatted = [drink.long() for drink in drinks]

    if len(drinks_formatted) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'drinks': drinks_formatted
    })


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drinks():
    body = request.get_json()

    title = body.get('title')
    recipe = body.get('recipe')

    try:
        drink = Drink(
                        title=title,
                        recipe=json.dumps(recipe)
                    )

        drink.insert()

        return jsonify({
            'success': True,
            'drinks': [drink.long()],
        })

    except Exception as e:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(drink_id):
    body = request.get_json()

    title = body.get('title')
    recipe = body.get('recipe')

    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        drink.title = title
        drink.recipe = json.dumps(recipe)

        drink.update()

        return jsonify({
            'success': True,
            'drinks': [drink.long()],
        })

    except Exception as ex:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(drink_id):
    body = request.get_json()

    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        id = drink.id
        drink.delete()

        return jsonify({
            'success': True,
            'delete': id
        })
    except Exception as ex:
        abort(422)

# Error Handling


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def unauthorized_error(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500
