# Full Stack Trivia API Backend

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

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET '/questions'
POST '/questions'
DELETE '/questions/<int:question_id>'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'

GET '/categories'
- Fetches an array of categories where the location in the array equals one less than the category id
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an array of category types 
[0] = "Science"
[1] = "Art"
[2] = "Geography"
[3] = "History"
[4] = "Entertainment"
[5] = "Sports"

GET '/questions'
- Returns information on a single page of questions in the trivia game along with a list of categories
- Request Arguments: page (defaults to 1) specifying which page of questions to return, beginning with 1
- Returns: A dictionary with keys:
success: True or False depending on whether the operation was successful. 
questions: An array of questions dictionary objects
total_questions: A count of total questions in the gave across all categories and pages
categories: An array of category types

Sample JSON Response:
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {...},
    {...}
  ], 
  "success": true, 
  "total_questions": 22
}

POST '/questions'
- This endpoint is used to add new questions to the trivia game or to search for a question containing some text
- I would have broken this out into two endpoints but that would have required a front-end refactor
- Request Arguments: 
  searchTerm: A string to search within the question text of all questions. This is case insensitive.
  page: The page number within the search results to return
  question: Question text for new question
  answer: Answer to new question
  difficulty: Integer specifying the difficuly level
  category: Integer specifying the category of the question
- Returns: If adding a questions the endpoint return success = True/False and created which specified the id of the new question
  When searching it returns:
    questions: An array of dictionary objects which are the questions matching the search criteria up to the limit that can fit on a page
    total_questions: A count of the total questions matching the criteria
    categories: A list of all categories in the game
    
Sample JSON Response for a search:
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "questions": [
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
	
DELETE '/questions/<int:question_id>'
- This endpoint will remove question with id question_id from the game
- Request Arguments:
    question_id: The id of the question to delete
- Returns:
    success: true or false depending on whether the operation succeeded
    deleted: id of the deleted question
    
GET '/categories/<int:category_id>/questions'
- Returns all questions for the given page within the specified category
- Request Arguments:
    page: The page number of questions to return
    category_id: Used within the URL to specify which category to limit questions to
- Returns: A dictionary with keys:
    success: True or False depending on whether the operation was successful. 
    questions: An array of questions dictionary objects
    total_questions: A count of total questions in the gave across all categories and pages
    current_category: The id of the category being filtered to
    categories: An array of category types

JSON Response:
    
{
  "categories": [
    "Art", 
    "Entertainment", 
    "Geography", 
    "History", 
    "Science", 
    "Sports"
  ], 
  "current_category": 3, 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    { .. }, 
    { .. }
  ], 
  "success": true, 
  "total_questions": 4
}

POST '/quizzes'
- Returns a question for the user to answer in a given category which the user has not yet answered
- Request Arguments:
    previous_questions: An array containing the ids of previously asked questions to avoid
    quiz_category: A dictionary specifying the id and type of the category to quiz from. If type = 'click' then questions are not filtered to a single category
- Returns: A dictionary containing a success flag and 'question', the question to be asked

JSON Response:

{
  "question": {
    "answer": "Lake Victoria", 
    "category": 3, 
    "difficulty": 2, 
    "id": 13, 
    "question": "What is the largest lake in Africa?"
  }, 
  "quiz_category": {
    "id": 3, 
    "type": "Geography"
  }, 
  "success": true
}



```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```