from operator import ne
import os
from flask import Flask, request, jsonify, abort, redirect, render_template
from sqlalchemy import exc
import json
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth import AuthError, requires_auth
from dotenv import load_dotenv
load_dotenv('.env')

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
setup_db(app)
CORS(app)


# ROUTES
# Authorize
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET'])
def login():
    return redirect(os.environ.get('AUTH_0'))


@app.route('/get_token', methods=['GET'])
def get_token():
    return render_template('token_page.html')


# GET REQUESTS
# Movies
# GET ALL MOVIES WITH ACTORS


@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(jwt):
    movies = Movie.query.all()
    return jsonify({
        'success': True,
        'movies_count': len(movies),
        'movies': [movie.format() for movie in movies]
    }), 200


# GET 1 MOVIE BY ID
@app.route('/movies/<int:movies_id>', methods=['GET'])
@requires_auth('get:movies')
def get_movie_by_id(jwt, movies_id):
    movie = Movie.query.get(movies_id)
    if not movie:
        abort(404)

    return jsonify({
        'success': True,
        'movie': movie.format(),
    }), 200


# ACTORS
# GET ALL ACTORS
@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(jwt):
    actors = Actor.query.all()
    return jsonify({
        'success': True,
        'actors_count': len(actors),
        'actors': [actor.format() for actor in actors]
    }), 200


# GET 1 ACTOR BY ID
@app.route('/actors/<int:actor_id>', methods=['GET'])
@requires_auth('get:actors')
def get_actor_by_id(jwt, actor_id):
    actor = Actor.query.get(actor_id)
    if not actor:
        abort(404)

    return jsonify({
        'success': True,
        'actor': actor.format(),
    }), 200


# POST REQUESTS
# Movies
# POST A NEW MOVIE
@app.route('/movies', methods=['POST'])
@requires_auth('post:movie')
def post_movies(jwt):
    data = request.get_json()
    if 'title' and 'release_date' not in data:
        abort(422)

    new_movie = Movie(title=data['title'], release_date=data['release_date'])
    new_movie.insert()

    return jsonify({
        'success': True,
        'added_movie': [new_movie.format()]
    })


# Actors
# POST A NEW Actor
@app.route('/actors', methods=['POST'])
@requires_auth('post:actor')
def post_actors(jwt):
    data = request.get_json()
    if 'name' and 'age' and 'gender' not in data:
        abort(422)

    new_actor = Actor(name=data['name'],
                      age=data['age'], gender=data["gender"])
    # movie id can be left blank for later assignation
    if 'movie_id' in data:
        new_actor.movie_id = data['movie_id']

    new_actor.insert()

    return jsonify({
        'success': True,
        'added_actor': [new_actor.format()]
    })


# PATCH REQUESTS
# Movies
# PATCH AN EXISTING MOVIE
@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movie')
def update_movies(jwt, movie_id):
    data = request.get_json()
    updated_movie = Movie.query.get(movie_id)
    if updated_movie is None:
        abort(404)

    if 'title' in data:
        updated_movie.title = data['title']

    if 'release_date' in data:
        updated_movie.release_date = data["release_date"]

    updated_movie.update()

    return jsonify({
        'success': True,
        'updated_movie': [updated_movie.return_movie()]
    })

# Movies
# PATCH AN EXISTING ACTOR


@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actor')
def update_actors(jwt, actor_id):
    data = request.get_json()
    updated_actor = Actor.query.get(actor_id)
    if updated_actor is None:
        abort(404)

    if 'name' in data:
        updated_actor.name = data['name']

    if 'age' in data:
        updated_actor.age = data["age"]

    if 'gender' in data:
        updated_actor.gender = data["gender"]

    if 'movie_id' in data:
        updated_actor.movie_id = data["movie_id"]

    updated_actor.update()

    return jsonify({
        'success': True,
        'updated_actor': [updated_actor.format()]
    })


# DELETE REQUESTS
# Movies
# DELETE AN EXISTING MOVIE
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movie')
def delete_movie(jwt, movie_id):
    deleted_movie = Movie.query.get(movie_id)

    if not deleted_movie:
        abort(404)

    try:
        deleted_movie.delete()
    except:
        abort(422)

    return jsonify({'success': True, 'deleted_movie_id': movie_id}), 200


# Actors
# DELETE AN EXISTING ACTOR
@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actor')
def delete_actor(jwt, actor_id):
    deleted_actor = Actor.query.get(actor_id)

    if not deleted_actor:
        abort(404)

    try:
        deleted_actor.delete()
    except:
        abort(422)

    return jsonify({'success': True, 'deleted_actor_id': actor_id}), 200


# Error Handling
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(500)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code
