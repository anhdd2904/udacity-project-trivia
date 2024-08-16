import os
import unittest
import json


from flaskr import create_app

from settings import DB_NAME, DB_USER,DB_PASSWORD

database_name= DB_NAME
database_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER,DB_PASSWORD,'localhost:5432', database_name)


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_path = database_path
        
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

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['totalQuestions'])

    def test_no_data_find_all_question(self):
        res = self.client().get('/trivia/v1/questions?page=1000')
        data = json.loads(res.data)

        self.assertTrue(len(data['questions']) == 0)

    def delete_qes_by_id(self):
        res = self.client().delete('/trivia/v1/questions/1')
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 200)
        self.assertTrue(data['message'])

    def test_500_delete_qes_by_id_notfound(self):
        res = self.client().delete('/trivia/v1/questions/-1')
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 500)

    def test_add_question(self):
        request = {
            'question':  'Heres a new question string',
            'answer':  'Heres a new answer string',
            'difficulty': 1,
            'category': 3,
        }
        res = self.client().post('/trivia/v1/questions', json=request)
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 201)
        self.assertTrue(data['message'])

    def test_500_add_question(self):
        request = {
            'question':  'Heres a new question string',
            'answer':  'Heres a new answer string',
            'difficulty': 1,
            'category': '',
        }
        res = self.client().post('/trivia/v1/questions', json=request)
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 500)
        self.assertEqual(data['message'],'Create question error')
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

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertTrue(len(data['question']))

    def test_404_get_next_question(self):
        request = {
            'previous_questions': [1, 4, 20, 15],
            'quiz_category': {
                'id': 3,
                'type': 'Geography'
            }
        }
        res = self.client().post('/trivia/v1/quizzessssss', json=request)
        self.assertEqual(res.status_code, 404)

    def test_search_question(self):
        request = {
            'searchTerm': 'What'
        }
        res = self.client().post('/trivia/v1/questions_search', json=request)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], "successfully")
        self.assertTrue(data['questions'])

    def test_404_error_search_question(self):
        request = {
            'searchTerm': "abc"
        }
        res = self.client().post('/trivia/v1/questions_search_data', json=request)
        self.assertEqual(res.status_code, 404)


    def test_search_questio_by_category(self):

        res = self.client().get('/trivia/v1/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], "successfully")
        self.assertTrue(data['questions'])

    def test_404_search_questio_by_category(self):

        res = self.client().get('/trivia/v1/categories/1/questionsssss')
        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()