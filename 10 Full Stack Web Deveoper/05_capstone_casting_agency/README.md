# Casting Agency

The API is curretnly hosting at https://casting-agency-api-2020.herokuapp.com/

## Motivation

This Capstone project serves to showcase the concepts and the skills learned in Udacity's Full Stack Web Developer Nanodegree Program.

- Coding in Python 3
- Relational Database Architecture
- Modeling Data Objects with SQLAlchemy
- Internet Protocols and Communication
- Developing a Flask API
- Authentication and Access
- Authentication with Auth0
- Authentication in Flask
- Role-Based Access Control (RBAC)
- Testing Flask Applications
- Deploying Applications

## Introduction

- This project models a company that is responsible for creating movies and managing and assigning actors to those movies.

- Models:
    - Movies with attributes title and release date
    - Actors with attributes name, age and gender

- Endpoints:
    - GET /actors and /movies
    - DELETE /actors/ and /movies/
    - POST /actors and /movies and
    - PATCH /actors/ and /movies/

- Roles:

    - Casting Assistant
        - Can view actors and movies

    - Casting Director
        - All permissions a Casting Assistant has and…
        - Add or delete an actor from the database
        - Modify actors or movies

    - Executive Producer
        - All permissions a Casting Director has and…
        - Add or delete a movie from the database

## Getting Started

### Development Setup

1. Install Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. Install Virtual Environment

Follow instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. Install the Dependencies

Navigate to the root directory of this project and run:

```bash
pip install -r requirements.txt
```

### Running the Server

From within the root directory of this project, first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
python app.py
```

### Setting Environment Variables

Excute the `setup.sh` to set the auth0 credentials:

```bash
bash setup.sh
```

### Running the Test Cases

Once setting up the autho0 credientials, excute the following commmand the run the test case:

```bash
python test_app.py
```

### Testing the live API

Please follow API reference below to test the endpoints.

## API Reference

### Errors

A typical error is return as a JSON object:

```
{
  "error": 401,
  "message": "unauthenticated",
  "success": false
}
```

### Endpoints

GET '/movies?page=<page_number>'
- Fetches a paginated list of dictionary of movies
- Request Arguments (optional): page_number
- Sample response:
```
{
  "movies": [
    {
      "id": 1,
      "release_date": "2012-07-20",
      "title": "The Dark Knight Rises"
    },
    {
      "id": 2,
      "release_date": "2019-04-26",
      "title": "Avengers: Endgame"
    }
  ],
  "success": true,
  "total_movies": 2
}
```

GET '/movies?page=<page_number>'
- Fetches a paginated list of dictionary of actors
- Request Arguments (optional): page_number
- Sample response:
```
{
  "actors": [
    {
      "age": 38,
      "gender": "Female",
      "id": 1,
      "name": "Anne Hathaway"
    },
    {
      "age": 37,
      "gender": "Male",
      "id": 2,
      "name": "Henry Cavill"
    }
  ],
  "success": true,
  "total_actors": 2
}
```

POST '/movies'
- Create a new row in the movies table
- Request Arguments: None
- Sample Request Body: `{"title": "The Dark Knight Rises", "release_date": "2012-07-20"}`
- Sample response:
```
{
  "movies": [
    {
      "id": 1,
      "release_date": "2012-07-20",
      "title": "The Dark Knight Rises"
    }
  ],
  "success": true
}
```

POST '/actors'
- Create a new row in the actors table
- Request Arguments: None
- Sample Request Body: `{"name": "Anne Hathaway", "age": 38, "gender": "Female"}`
- Sample response:
```
{
  "actors": [
    {
      "age": 38,
      "gender": "Female",
      "id": 1,
      "name": "Anne Hathaway"
    }
  ],
  "success": true
}
```

PATCH '/movies/<id>'
- Update a existing row corresponding to the given id in the movies table
- Request Arguments: id
- Sample Request Body: `{"title": "The Dark Knight Rises A Fire Will Rise", "release_date": "2012-07-20"}`
- Sample response:
```
{
  "movies": [
    {
      "id": 1,
      "release_date": "2012-07-20",
      "title": "The Dark Knight Rises A Fire Will Rise"
    }
  ],
  "success": true
}
```

PATCH '/actors/<id>'
- Update a existing row corresponding to the given id in the actors table
- Request Arguments: id
- Sample Request Body: `{"name": "Anne Jacqueline Hathaway", "age": 38, "gender": "Female"}`
- Sample response:
```
{
  "actors": [
    {
      "age": 38,
      "gender": "Female",
      "id": 1,
      "name": "Anne Jacqueline Hathaway"
    }
  ],
  "success": true
}
```

DELETE '/movies/<id>'
- Delete an existing row corresponding to the given id in the movies table
- Request Arguments: id
- Sample response:
```
{
  "delete": 2,
  "success": true
}
```

DELETE '/actors/<id>'
- Delete an existing row corresponding to the given id in the actors table
- Request Arguments: id
- Sample response:
```
{
  "delete": 2,
  "success": true
}
```
