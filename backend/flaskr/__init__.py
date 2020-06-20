import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# Questions pagination
def question_pagination(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  return current_questions




def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  # Set up CORS. Allow '*' for origins
  CORS(app, resources={r"/api/*": {"origins": "*"}})





  # set Access-Control-Allow CORS headers
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response




  # handle GET requests for all available categories
  @app.route('/categories')
  def get_categories():
    try:
      categories = Category.query.all()
      categories_dict = {}
      for category in categories:
        categories_dict[category.id] = category.type

      return jsonify({
        'success': True,
        'categories': categories_dict
    }), 200

    except Exception:
      abort(500)



 # handle GET requests for questions, including pagination (every 10 questions). 
  @app.route('/questions')
  def retrieve_questions():
     
    selection = Question.query.order_by(Question.id).all()
    current_questions = question_pagination(request, selection)

    category_objects = Category.query.order_by(Category.id).all()
    categories = {item.id: item.type for item in category_objects}
    current_categories = [question['category'] for question in current_questions]

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'current_category': current_categories,
      'questions': current_questions,
      'total_questions': len(Question.query.all()),
      'categories': categories
    })



#DELETE question using a question ID. 
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      question.delete()


      return jsonify({
        'success': True,
        'deleted': question_id
     })
    except:
      abort(404)




#POST a new question, require the question and answer text, category, and difficulty score.
  @app.route("/questions", methods=['POST'])
  def add_question():
    body = request.get_json()

    if body.get('question') is None or body.get('answer') is None or body.get('category') is None or body.get('difficulty') is None:
      abort(422)

    new_question = body.get('question')
    new_answer = body.get('answer')
    new_difficulty = body.get('difficulty')
    new_category = body.get('category')

    try:
      question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
      question.insert()

      return jsonify({
        'success': True,
        'created': question.id,
      })

    except:
      abort(422)

 

#get questions by search 
  @app.route('/search', methods=['POST'])
  def search_questions():
  
    body = request.get_json()

    search_term = body.get('searchTerm')

    selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

    if (len(selection) == 0):
      abort(404)

 
      paginated = question_pagination(request, selection)

           
      return jsonify({
        'success': True,
        'questions': paginated,
        'total_questions': len(Question.query.all())
      })

    
   




  

#get questions based on category.
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    

    questions = Question.query.order_by(Question.id).filter_by(category=category_id)
    current_category = [question.category for question in questions]

    if len(current_category) == 0:
      abort(404)


    return jsonify({
      "questions": [question.format() for question in questions.all()],
      "total_questions": len(questions.all()),
      "current_category": current_category,
    })


  


 #get questions to play the quiz. return a random questions within the given category
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():

    try:
      body = request.get_json()

      if not ('quiz_category' in body and 'previous_questions' in body):
        abort(422)

      category = body.get('quiz_category')
      previous_questions = body.get('previous_questions')

      if category['type'] == 'click':
        available_questions = Question.query.filter(Question.id.notin_((previous_questions))).all()
      else:
        available_questions = Question.query.filter_by(category=category['id']).filter(Question.id.notin_((previous_questions))).all()

      new_question = available_questions[random.randrange(0, len(available_questions))].format() if len(available_questions) > 0 else None

      return jsonify({
        'success': True,
        'question': new_question
      })
    except:
      abort(422)


   
  #error handlers for all expected errors 
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Resource not found"
    }), 404

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
    })
 
  
  return app




    