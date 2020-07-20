import os
import dateutil.parser
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, db_drop_and_create_all, Movie, Actor
from auth import AuthError, requires_auth

ENTRIES_PER_PAGE = 10


def paginate_entries(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ENTRIES_PER_PAGE
    end = start + ENTRIES_PER_PAGE

    entries = [entry.format() for entry in selection]
    current_entries = entries[start:end]

    return current_entries


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    Uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    '''
    # db_drop_and_create_all()

    '''
    Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # ROUTES
    '''
    GET /movies
        get all available movies
    '''
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            # Retrieve all movies from repository
            movies = Movie.query.order_by(Movie.id).all()
        except Exception:
            abort(500)

        # No movies found
        if not movies:
            abort(404)

        current_movies = paginate_entries(request, movies)

        # Return list of movies
        return jsonify({
            'success': True,
            'movies': current_movies,
            'total_movies': len(movies)
        }), 200

    '''
    GET /actors
        get all available actors
    '''
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            # Retrieve all actors from repository
            actors = Actor.query.order_by(Actor.id).all()
        except Exception:
            abort(500)

        # No movies found
        if not actors:
            abort(404)

        current_actors = paginate_entries(request, actors)

        # Return list of movies
        return jsonify({
            'success': True,
            'actors': current_actors,
            'total_actors': len(actors)
        }), 200

    '''
    POST /movies
        insert a new row in the movies table
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def insert_movies(payload):
        # Retieve movie contents from user request
        body = request.get_json()

        # No title found
        if (not body) or (not body.get('title', None)):
            abort(422)
        title = body.get('title')
        release_date = dateutil.parser.parse(
            body.get('release_date'))

        try:
            # Create a new movie
            new_movie = Movie(
                title=title,
                release_date=release_date)

            # Insert a new movie into repository
            new_movie.insert()

            return jsonify({
                'success': True,
                'movies': [new_movie.format()]
            }), 200
        except Exception:
            abort(422)

    '''
    POST /actors
        create a new row in the actors table
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def insert_actors(payload):
        # Retieve movie contents from user request
        body = request.get_json()

        # No name found
        if (not body) or (not body.get('name', None)):
            abort(422)
        name = body.get('name')
        age = body.get('age', None)
        gender = body.get('gender', None)

        try:
            # Create a new actor
            new_actor = Actor(
                name=name,
                age=age,
                gender=gender)

            # Insert a new movie into repository
            new_actor.insert()

            return jsonify({
                'success': True,
                'actors': [new_actor.format()]
            }), 200
        except Exception:
            abort(422)

    '''
    DELETE /movies/<id>
        where <id> is the existing model id
        delete the corresponding row for <id>
    '''
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(payload, id):
        try:
            # Retrieve the movie given the id
            movie = Movie.query.filter(Movie.id == id).one_or_none()
        except Exception:
            abort(500)
        # No movie found
        if not movie:
            abort(404)
        try:
            # Delete the movie
            movie.delete()

            return jsonify({
                'success': True,
                'delete': id
            }), 200
        except Exception:
            abort(422)

    '''
    DELETE /actors/<id>
        where <id> is the existing model id
        delete the corresponding row for <id>
    '''
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(payload, id):
        try:
            # Retrieve the actor given the id
            actor = Actor.query.filter(Actor.id == id).one_or_none()
        except Exception:
            abort(500)
        # No actor found
        if not actor:
            abort(404)
        try:
            # Delete the actor
            actor.delete()

            return jsonify({
                'success': True,
                'delete': id
            }), 200
        except Exception:
            abort(422)

    '''
    PATCH /movies/<id>
        where <id> is the existing model id
        update the corresponding row for <id>
    '''
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movies(payload, id):
        try:
            # Retrieve the movie given the id
            movie = Movie.query.filter(Movie.id == id).one_or_none()
        except Exception:
            abort(500)

        # No movie found
        if not movie:
            abort(404)

        try:
            # Retrieve movie contents from user request
            body = request.get_json()

            # Update movie contents
            if 'title' in body:
                movie.title = body.get('title')
            if 'release_date' in body:
                movie.release_date = dateutil.parser.parse(
                    body.get('release_date'))
            if 'actor_id' in body:
                movie.actor_id = body.get('actor_id')

            movie.update()

            return jsonify({
                'success': True,
                'movies': [movie.format()]
            }), 200
        except Exception:
            abort(422)

    '''
    PATCH /actors/<id>
        where <id> is the existing model id
        update the corresponding row for <id>
    '''
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actors(payload, id):
        try:
            # Retrieve the actor given the id
            actor = Actor.query.filter(Actor.id == id).one_or_none()
        except Exception:
            abort(500)

        # No actor found
        if not actor:
            abort(404)

        try:
            # Retrieve actor contents from user request
            body = request.get_json()

            # Update actor contents
            if 'name' in body:
                actor.name = body.get('name')
            if 'age' in body:
                actor.age = body.get('age')
            if 'gender' in body:
                actor.gender = body.get('gender')

            actor.update()

            return jsonify({
                'success': True,
                'actors': [actor.format()]
            }), 200
        except Exception:
            abort(422)

    # Error Handling
    '''
    Implement error handler for 422
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
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    '''
    Implement error handler for 500
    '''
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    '''
    Implement error handler for 405
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
    '''
    @app.errorhandler(AuthError)
    def not_auth(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error.get('description')
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
