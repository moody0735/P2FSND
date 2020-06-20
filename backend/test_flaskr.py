import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', '9520099', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()



        self.question = {
            'question': "Who is the best striker in the world?",
            'answer': "Robert Lewandowski",
            'difficulty': "1",
            'category': 6
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['categories']), 6)
        self.assertTrue(data['categories'])
        self.assertEqual(data['success'], True)




    # Test for get all paginated questions
    def test_get_paginated_questions(self):
        
        response = self.client().get('/questions')
        data = json.loads(response.data)

        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 10)



    # Test for invalid requested page
    def test_invalid_qustions_page(self):
       
        response = self.client().get('/questions?page=1000')
        data = json.loads(response.data)

       
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')


    # Test for delete question
    def test_delete_question_by_ID(self):
        new_question = Question(
            question='This is a test question that should deleted',
            answer='this answer should be deleted',
            difficulty=1,
            category='1'
        )

        new_question.insert()
        response = self.client().delete('/questions/{}'.format(new_question.id))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    

    # Test for delete a guestion does not exist
    def test_delete_question(self):
        response = self.client().delete('/question/1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')



    # Test for create a new question
    def test_create_question(self):
        response = self.client().post('/questions', json=self.question)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


    # Test for post empty question 
    def test_uncreated_question(self):
        request_data = {
            'question': '',
            'answer': '',
            'difficulty': '',
            'category': '',
        }

        response = self.client().post('/questions', json=request_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')



    # Test for search
    def test_search_question(self):
        response = self.client().post('/questions', json={'searchTerm': "Africa"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

   

    # Test for unseccessful search
    def test_search_not_found(self):
        response = self.client().post('/questions', json={'searchTerm': ""})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    # Test for play quiz
    def test_get_quiz_question(self):
        response = self.client().post('/quizzes', json={'quiz_category': {'type': 'Science', 'id': '1'},'previous_questions': []})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

        

    # Test for unfound category in quiz
    def test_notfound_quiz_question(self):
        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')






# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()