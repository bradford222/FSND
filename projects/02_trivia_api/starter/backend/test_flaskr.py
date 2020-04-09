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
        self.database_user = "postgres"
        self.database_pw = "postgres"

        # Note I'm using port 5433 due to the way my system is set up
        self.database_path = "postgres://{}:{}@{}/{}".format(self.database_user, self.database_pw, 'localhost:5433', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertNotEqual(len(data['categories']),0)

    def test_list_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])
        self.assertNotEqual(len(data['questions']),0)
        self.assertNotEqual(len(data['categories']),0)

    def test_delete_question(self):
        question = Question.query.first()
        question_id = question.id

        res = self.client().delete('/questions/' + str(question_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)

    def test_questions_in_category(self):
        category_id = Category.query.first().id
        res = self.client().get('/categories/' + str(category_id) + '/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(data['current_category'], category_id)
        self.assertTrue(data['total_questions'])
        self.assertNotEqual(len(data['questions']),0)
        self.assertNotEqual(len(data['categories']),0)

    def test_quizzes(self):

        category = Category.query.first()
        args = {
            'previous_questions': [1, 2]
        }
        args['quiz_category'] = category.format()

        print(args)

        res = self.client().post('/quizzes', data=json.dumps(args), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['quiz_category'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()