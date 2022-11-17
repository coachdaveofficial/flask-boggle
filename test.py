from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    # test that home page loads
    def test_home_page(self):
        with app.test_client() as client:
            resp = client.get()
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<span>High Score:</span>', html)
    # test that session info exists and works
    def test_session_info(self):
        with app.test_client() as client:
            
            with client.session_transaction() as change_session:
                change_session['high_score'] = 25
                change_session['num_plays'] = 999
            resp = client.get('/')

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session['high_score'], 25)
            self.assertEqual(session['num_plays'], 999)
    # test that submitting a score as a query string returns the appropriate response
    def test_score_submit(self):
        with app.test_client() as client:
            resp = client.get('/new-score/?score=10')
            json = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('"score": "10"', json)
            self.assertIn('"num_plays": 1', json)
    # test that response is ok if word is on board
    def test_word_check(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [['T', 'L', 'G', 'H', 'S'], 
                ['F', 'W', 'M', 'M', 'C'], 
                ['H', 'Q', 'J', 'I', 'H'], 
                ['B', 'R', 'N', 'D', 'G'], 
                ['N', 'L', 'E', 'Y', 'F']]

            resp = client.get('/word-check?word=dine')
            json = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('"result": "ok"', json)

