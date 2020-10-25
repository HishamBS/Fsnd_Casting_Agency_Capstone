# Casting Agency API 

## Simple Information About the App
* deployed link : https://hbs-casting-agency.herokuapp.com/
* This is an api that was made for a casting agency , with all endpoints authenticated with auth0.
* There are 2 main endpoints `/moivs` and `/actors`.
* This api demonestrate the full CRUD operations on those endpoints.
* To get authenticated , navigate to the home end point `/` and click on the authentication button , which will redirect you to the auth0
website to either sign in , or sign up with a new account. once authenticated you will be redirected to a page which will show you the 
generated token to be used with the REST calls.
* A post man collection can be found in the root of this repo , which can be used to test and access all end points.

### Users and Roles
there are 3 users with the following permissions :
next to each user , you will find an email to use it to access
the api , all passwords are : `Aa@12345`
* **Casting Assistant** _casting_assistant@casting-agency.com_
  
    `Can view actors and movies`

* **Casting Director** _casting_director@casting-agency.com_
  
    `1.All permissions a Casting Assistant has`

    `2.Add or delete an actor from the database`

    `3.Modify actors or movies`

* **Executive Producer** _executive_producer@casting-agency.com_
  
    `1.All permissions a Casting Director has.`

    `2.Add or delete a movie from the database`



## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.


## Database Setup
Database need to be created locally first using the comand
```bash
createdb casting_agency
```
With Postgres running, restore a database using the casting_agency.psql file provided. From the root folder in terminal run:
```bash
psql casting_agency < casting_agency.psql
```

## Running the server

From within the `root` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
flask run --reload
```

## API Documentation
### GET Requests
---
#### GET `'/movies'`
- Fetches a dictionary of all movies with an array of all actors 
in each movie.
- Example :
```
curl -H "Authorization: Bearer {TOKEN_HERE}" http://127.0.0.1:5000/movies
```
- Response :
```
"success": true,
    "movies_count": 9,
    "movies": [
        {
            "id": 1,
            "title": "The Equalizer",
            "release_date": "Mon, 22 Sep 2014 00:00:00 GMT",
            "actors": [
                {
                    "id": 2,
                    "name": "Denzel Washington",
                    "age": 50,
                    "gender": "Male"
                }
            ]
        },
        {
            "id": 2,
            "title": "Cast Away",
            "release_date": "Thu, 07 Dec 2000 00:00:00 GMT",
            "actors": [
                {
                    "id": 1,
                    "name": "Tom Hanks",
                    "age": 55,
                    "gender": "Male"
                }
            ]
        }
```
#### GET `'/movies/<int:movie_id>'`
- Fetches a dictionary of a single movie for the given id with an array of all actors 
in this movie.
- Example :
```
curl -H "Authorization: Bearer {TOKEN_HERE}" http://127.0.0.1:5000/movies/1
```
- Response :
```
{
    "success": true,
    "movie": {
        "id": 1,
        "title": "The Equalizer",
        "release_date": "Mon, 22 Sep 2014 00:00:00 GMT",
        "actors": [
            {
                "id": 2,
                "name": "Denzel Washington",
                "age": 50,
                "gender": "Male"
            }
        ]
    }
}
```

#### GET `'/actors'`
- Fetches a dictionary of all actors with a movie object if exists for each actor.
- Example :
```
curl -H "Authorization: Bearer {TOKEN_HERE}" http://127.0.0.1:5000/actors
```
- Response :
```
"success": true,
    "actors_count": 10,
    "actors": [
        {
            "id": 2,
            "name": "Denzel Washington",
            "age": 50,
            "gender": "Male",
            "movie": {
                "id": 1,
                "title": "The Equalizer",
                "release_date": "Mon, 22 Sep 2014 00:00:00 GMT"
            }
        },
        {
            "id": 1,
            "name": "Tom Hanks",
            "age": 55,
            "gender": "Male",
            "movie": {
                "id": 2,
                "title": "Cast Away",
                "release_date": "Thu, 07 Dec 2000 00:00:00 GMT"
            }
        }
```
#### GET `'/actors/<int:actor_id>'`
- Fetches a dictionary of a single actor for the given id with an object of the movie that this actor stars in , if exists. 
- Example :
```
curl -H "Authorization: Bearer {TOKEN_HERE}" http://127.0.0.1:5000/actors/1
```
- Response :
```
{
    "success": true,
    "actor": {
        "id": 1,
        "name": "Tom Hanks",
        "age": 55,
        "gender": "Male",
        "movie": {
            "id": 2,
            "title": "Cast Away",
            "release_date": "Thu, 07 Dec 2000 00:00:00 GMT"
        }
    }
}
```


---

### DELETE Requests
---
#### DELETE `'/movies/<int:movie_id>'`
- Deletes a movie from the database given its ID.
- Example :
```
curl -H "Authorization: Bearer {TOKEN_HERE}" http://127.0.0.1:5000/movies/1 -X DELETE
```
- Response :
```
 {
      "deleted_movie_id": 1 
      "success": true
  }

```

#### DELETE `'/actors/<int:actor_id>'`
- Deletes an actor from the database given its ID.
- Example :
```
curl -H "Authorization: Bearer {TOKEN_HERE}" http://127.0.0.1:5000/actors/1 -X DELETE
```
- Response :
```
 {
      "deleted_actor_id": 1 
      "success": true
  }

```

### POST Requests
---
#### POST `'/movies'`
- Creates a new movie with a request body containing.
```
{
  
	"title":"death from beneath",
	"release_date":"2022/12/12"

}
```
- Example :
```
curl -H "Authorization: Bearer {TOKEN_HERE}" http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{ "title":"death from beneath","release_date":"2022/12/12"} '
```
- Response :
```
    "success": true,
    "added_movie": [
        {
            "id": 10,
            "title": "death from beneath",
            "release_date": "Mon, 12 Dec 2022 00:00:00 GMT",
            "actors": []
        }
    ]
```

#### POST `'/actors'`
- Creates a new actor with a request body containing.
```
{
	"name":"test actor",
	"age":"28",
	"gender":"male",
	"movie_id":null
}
```
- Example :
```
curl -H "Authorization: Bearer {TOKEN_HERE}" http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{"name":"test actor","age":"28","gender":"male","movie_id":null} '
```
- Response :
```
{
    "success": true,
    "added_actor": [
        {
            "id": 11,
            "name": "test actor",
            "age": 28,
            "gender": "male",
            "movie": ""
        }
    ]
}
```

### PATCH Requests
---
#### PATCH `'/movies/<int:movie_id>'`
- Updates an existing movie with a request body containing.
```
{
  
	"title":"updating",
	"release_date":"2022/12/12"

}
```
- Example :
```
curl -H "Authorization: Bearer {TOKEN_HERE}" http://127.0.0.1:5000/movies/10 -X PATCH -H "Content-Type: application/json" -d '{ "title":"updating","release_date":"2022/12/12"} '
```
- Response :
```
{
    "success": true,
    "updated_movie": [
        {
            "id": 10,
            "title": "updating",
            "release_date": "Mon, 12 Dec 2022 00:00:00 GMT"
        }
    ]
}
```

#### PATCH `'/actors/<int:actor_id>'`
- Updates an existing actor with a request body containing.
```
{
	"name":"test actor",
	"age":"29",
	"gender":"",
	"movie_id":null
}
```
- Example :
```
curl -H "Authorization: Bearer {TOKEN_HERE}" http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{"name":"test actor","age":"28","gender":"male","movie_id":null} '
```
- Response :
```
{
    "success": true,
    "updated_actor": [
        {
            "id": 11,
            "name": "testing patch",
            "age": 29,
            "gender": "",
            "movie": ""
        }
    ]
}
```
--- 
### Expected Errors
```
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

```

## Testing
To run the tests, run
```
dropdb casting_agency_test
createdb casting_agency_test
psql casting_agency_test < casting_agency.psql
python test_app.py
```
