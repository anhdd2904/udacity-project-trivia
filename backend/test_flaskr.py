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
        self.database_name = "trivia"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client
    def tearDown(self):
        """Executed after reach test"""
        pass
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_find_all_question(self):
        res = self.client().get('/trivia/v1/questions')
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['totalQuestions']))

    def delete_qes_by_id(self):
        res = self.client().delete('/trivia/v1/questions/1')
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 200)
        self.assertTrue(data['message'])
    def test_add_question(self):
        request = {
            'question':  'Heres a new question string',
            'answer':  'Heres a new answer string',
            'difficulty': 1,
            'category': 3,
        }
        res = self.client().post('/trivia/v1/questions', json=request)
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 200)
        self.assertTrue(data['message'])

    def test_get_next_question(self):
        request = {
            'previous_questions': [1, 4, 20, 15],
            'quiz_category': {
                'id': 3,
                'type': 'Geography'
            }
        }
        res = self.client().post('/trivia/v1/quizzes', json=request)
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertTrue(len(data['question']))

    def search_question(self):
        request = {
            'searchTerm': 'What'
        }
        res = self.client().post('/trivia/v1/questions_search', json=request)
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 200)
        self.assertEquals(data['message'], "successfully")
        self.assertTrue(data['question'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()