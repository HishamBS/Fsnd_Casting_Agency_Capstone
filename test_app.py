import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import setup_db, Actor, Movie


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.dummy_question = {
            'question': 'New Question',
            'answer': 'No Answer',
            'difficulty': 2,
            'category': 2
        }

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
    DONE 14 tests all pass
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], len(Question.query.all()))
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(len(data['categories']))

    def test_404_send_beyond_page_limit(self):
        res = self.client().get('/questions?page=20')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), len(Category.query.all()))

    def test_404_send_beyond_category_limit(self):
        res = self.client().get('/categories/7')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_all_questions_in_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), len(
            Question.query.filter_by(category=3).all()))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], "Geography")

    def test_400_send_category_zero(self):
        res = self.client().get('/categories/0/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_create_question(self):
        total_questions_before = (len(Question.query.all()))
        res = self.client().post('/questions/new', json=self.dummy_question)
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(Question.query.all()),
                         total_questions_before+1)

    def test_422_send_wrong_json(self):
        wrong_question = "hi"
        res = self.client().post('/questions/new', json=wrong_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_search(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': 'what'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])

    def test_400_json_missing_key(self):
        res = self.client().post('/questions/search', json={"foo": "bar"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_delete_question(self):
        to_be_deleted_question = Question(question='FOOOOO', answer='BAAAAAAR',
                                          difficulty=3, category=4)
        to_be_deleted_question.insert()
        res = self.client().delete('/questions/{}'.format(to_be_deleted_question.id))
        data = json.loads(res.data)

        question = Question.query.filter(
            Question.id == to_be_deleted_question.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], to_be_deleted_question.id)
        self.assertEqual(question, None)

    def test_404_send_no_id(self):
        res = self.client().delete('/questions/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_new_game(self):
        res = self.client().post(
            '/newgame', json={"previous_questions": [], "quiz_category": {"id": 3}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['question'])
        self.assertEqual(data['question']['category'], 3)

    def test_404_send_no_previous_key(self):
        res = self.client().post('/quizzes', json={"quiz_category": {"id": 3}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
