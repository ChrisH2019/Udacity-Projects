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


'''
Uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()


# ROUTES
'''
GET /drinks
    it should be a public endpoint
    it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
    or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():
    try:
        # Retrieve all drinks from repository
        drinks = Drink.query.order_by(Drink.id).all()

        # No drinks found
        if not drinks:
            abort(404)

        # Return list of drinks in short representation
        return jsonify({
            'success': True,
            'drinks': [drink.short() for drink in drinks]
        }), 200
    except Exception:
        abort(422)


'''
GET /drinks-detail
    it should require the 'get:drinks-detail' permission
    it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
    or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(paylod):
    try:
        # Retrieve all drinks from repository
        drinks = Drink.query.order_by(Drink.id).all()

        # No drinks found
        if not drinks:
            abort(404)
            
        # Return list of drinks in long representation
        return jsonify({
            'success': True,
            'drinks': [drink.long() for drink in drinks]
        }), 200
    except Exception:
        abort(422)


'''
POST /drinks
    it should create a new row in the drinks table
    it should require the 'post:drinks' permission
    it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the newly created drink
    or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def insert_drinks(payload):
    try:
        # Retrieve drink ingredients from user
        body = request.get_json()

        # No title and recipe found
        if not all(key in body for key in ['title', 'recipe']):
            abort(400)

        # Create a new drink
        drink = Drink(
            title=body.get('title'),
            recipe=json.dumps([body.get('recipe')])
            )

        # Insert the newly created drink into repository
        drink.insert()

        # Return drinks in long representation
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200
    except Exception:
        abort(422)


'''
PATCH /drinks/<id>
    where <id> is the existing model id
    it should respond with a 404 error if <id> is not found
    it should update the corresponding row for <id>
    it should require the 'patch:drinks' permission
    it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the updated drink
    or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(payload, id):
    try:
        # Retrieve the drink given the id
        drink = Drink.query.filter(Drink.id == id).one_or_none()

        # Drink not found
        if not drink:
            abort(404)

        # Retrieve drink ingredients from user
        body = request.get_json()

        # Update drink ingredients
        if 'title' in body:
            drink.title = body.get('title')
        if 'recipe' in body:
            drink.recipe = json.dumps([body.get('recipe')])
        drink.update()

        # Return drinks in long representation
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200
    except Exception:
        abort(422)


'''
DELETE /drinks/<id>
    where <id> is the existing model id
    it should respond with a 404 error if <id> is not found
    it should delete the corresponding row for <id>
    it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id}
    where id is the id of the deleted record
    or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, id):
    try:
        # Retrieve the drink given the id
        drink = Drink.query.filter(Drink.id == id).one_or_none()

        # Drink not found
        if not drink:
            abort(404)

        # Delete the drink
        drink.delete()

        # Return the deleted drink id
        return jsonify({
            'success': True,
            'delete': id
        }), 200
    except Exception:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


'''
Implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


'''
Implement error handler for 400
    error handler should conform to general task above
'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400


'''
Implement error handler for 405
    error handler should conform to general task above
'''
@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not found'
    }), 405


'''
Implement error handler for 401
    error handler should conform to general task above
'''
@app.errorhandler(401)
def not_authenticated(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'unauthenticated'
    }), 401


'''
Implement error handler for 403
    error handler should conform to general task above
'''
@app.errorhandler(403)
def not_authorized(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message': 'unauthorized'
    }), 403


'''
Implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def not_auth(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error.get('description')
    }), error.status_code
