# Full Stack Trivia API 

This project is a game where users can test their knowledge answering trivia questions. implementing the following functionality:

- Display questions.
- Delete questions.
- Create new question.
- Search for questions.
- Play the quiz game.


### Installing Dependencies

this project should already have Python3, pip, node, and npm installed.


## Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```



## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```


### API Reference

## Getting Started
Backend Base URL: http://127.0.0.1:5000/
Frontend Base URL: http://127.0.0.1:3000/
Authentication: Authentication or API keys are not used in the project yet.
Error Handling
Errors are returned in the following json format:

```
 "success": "False",
  "error": 422,
  "message": "unprocessable",
```
The error codes currently returned are:

- 400 – bad request
- 404 – resource not found
- 422 – unprocessable
- 500 – internal server error

## Endpoints

### GET /categories

- Returns all the categories.
for test : ```curl http://127.0.0.1:5000/categories```


### GET /questions

- Returns all questions.
for test : ```curl http://127.0.0.1:5000/questions```

### DELETE /questions/int:id\

- Deletes a question by id.
for test : ```curl -X DELETE http://127.0.0.1:5000/questions/6 ```

### POST /questions

- Creates a new question.
for test : ```curl -X POST -H "Content-Type: application/json" -d '{ "question": "Frankie Fredericks represented which African country in athletics?", "answer": "Namibia", "difficulty": 3, "category": "6" }' http://127.0.0.1:5000/questions```


### POST /questions/search

- returns questions that has the search substring.
for test : ```curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Africa"}' http://127.0.0.1:5000/questions/search  ```


### GET /categories/int:id\/questions

- Gets questions by category using the id.
for test : ```curl http://127.0.0.1:5000/categories/1/questions ```


### POST /quizzes

- Takes the category and previous questions in the request.
- Return random question not in previous questions.

for test : ```curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [5, 9], "quiz_category": {"type": "History", "id": "4"}}' http://127.0.0.1:5000/quizzes  ```








