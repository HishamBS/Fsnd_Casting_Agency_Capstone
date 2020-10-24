import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import app

CASTING_ASSISTANT_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNsX1hreUs3blg0MTJQWmIyYXA3UyJ9.eyJpc3MiOiJodHRwczovL2hoYnMuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmOTM3ZTQ4OWI4ODIyMDA2ZWUwMDIxYiIsImF1ZCI6ImNhc3RpbmdfYWdlbmN5IiwiaWF0IjoxNjAzNTQzNDIwLCJleHAiOjE2MDM2Mjk4MjAsImF6cCI6ImNjVGhma3JSVDB5aFNpaUVMUU5Mc2VSaHlqWjZWTGwwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.cMN_Qc6pc9x857FRV6Cf4A5fXfWgGtWvkP-EnK3RuCIm_xorkQD6S0RTxJzU3QTJjIy8G6BwzccQTEGf0D5nRDFJqZss9Dli9OxBi1DruRXJZIHgOofsiKz1V39VVlF6I5l21ay8KCx-gqQiDidWZWwakrLuhqRHnI5b8upjmDM2gM_SnTR_sf-qvNz8zhPfnZ9SdmfY4NWx-CevFIZg4-OzGYQY349a20mOLTfuuP1Jz8Vvk_ju0y8QEN9rtnl6G1LysOyVjwb3NzNjW4xOF1ThA-ZkP3gYqIQK-54i34F-p9oWYhvvAy9M-F5kXkdDQlQcC0M_pvypm8cSImRzDw"
CASTING_DIRECTOR_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNsX1hreUs3blg0MTJQWmIyYXA3UyJ9.eyJpc3MiOiJodHRwczovL2hoYnMuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmOTQxNzhhODg4NzA4MDA3MGZkYTI2MyIsImF1ZCI6ImNhc3RpbmdfYWdlbmN5IiwiaWF0IjoxNjAzNTYyMjE4LCJleHAiOjE2MDM2NDg2MTgsImF6cCI6ImNjVGhma3JSVDB5aFNpaUVMUU5Mc2VSaHlqWjZWTGwwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIl19.lplE8xl5HIP0g5GZGDhLvDhLZoF39BYjGaepPr1io3_SnZks6rF4J3tMGyp5ha2pV-baBD5P_o6fWPAW9tUaxeumw0KdnC9erT1AFRqqEY1c0VH6vvNDLWOb1dHTDhD8Pal6uih-yzS-gmXuhOTWcoO3E0I-l6aUhYIFvoBkRtdwgiahDPeOnCg84ZrdMn-P3q56_sEn_krKtNaSPDKPT5dwhz3CWePB4YQ_u5lzAnI1XSaJdK0vQ6rv1wSLejl2O1y5z1gWRj_imB5lECDdnYDE3z0jsDwNh6nce_XrA9R9FF2pCgvoQDZTjUFy4u5Ij0k5LWwzSd1hDLf_SU-MUg"
EXECUTIVE_PRODUCER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNsX1hreUs3blg0MTJQWmIyYXA3UyJ9.eyJpc3MiOiJodHRwczovL2hoYnMuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmOTQxODYyMzM2YTg4MDA3N2RkOWE1ZCIsImF1ZCI6ImNhc3RpbmdfYWdlbmN5IiwiaWF0IjoxNjAzNTQxNDQzLCJleHAiOjE2MDM2Mjc4NDMsImF6cCI6ImNjVGhma3JSVDB5aFNpaUVMUU5Mc2VSaHlqWjZWTGwwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.hoB74StW51bAnLrWdKpKHuhJISARh8igJ6YTupEVO3K0k8aV7EP4Ry1xqumcGwXKPIyVhcLUFmLFy_9ah97x0RjlbbDtPnXovdSD9T79XHQHoN27a6Gkm3GYps5eHtu3T2_vmZjevOqNLNpUUOadwXRWqxJf3LRMHuwI7wqCJWu8zWu8MUjkq8cA4z4nVhlw_iCqIRdp-nrCpELJyIpxGr09BhppmcjNXwQHomEWFglH7yhEXka97ITI3UbDkU0pqbZ5TxaXjvXS6VAxFdcEjzW7_EPoJbeKjlpWSbs713lf_R9ZobKDfX9_TX-sMBPDlncdPa8QfO5Srpx2gjSewg"

DUMMY_MOVIE = {
    "title": "testing movie",
    "release_date": "2022/12/12"



}
DUMMY_ACTOR = {
    "name": "test actor",
    "age": "28",
    "gender": "male"

}


class CastingAgencyTests(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://macbookpro@localhost:5432/casting_agency_tests'
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_movies(self):
        res = self.client().get(
            '/movies', headers={'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), data['movies_count'])

    def test_404_send_beyond_movie_limit(self):
        res = self.client().get(
            '/movies/9999', headers={'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_all_actors(self):
        res = self.client().get(
            '/actors', headers={'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), data['actors_count'])

    def test_404_send_beyond_actors_limit(self):
        res = self.client().get(
            '/actors/9999', headers={'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_movie(self):
        res = self.client().post('/movies',
                                 headers={'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)}, json=DUMMY_MOVIE)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_create_unauthorized_movie(self):
        res = self.client().post('/movies',
                                 headers={'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT_TOKEN)}, json=DUMMY_MOVIE)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_422_wrong_movie_format(self):
        res = self.client().post('/movies',
                                 headers={'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)}, json={"foo": "bar"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_actor(self):
        res = self.client().post('/actors',
                                 headers={'Authorization': 'Bearer {}'.format(CASTING_DIRECTOR_TOKEN)}, json=DUMMY_ACTOR)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_create_unauthorized_actor(self):
        res = self.client().post('/actors',
                                 headers={'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT_TOKEN)}, json=DUMMY_ACTOR)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_422_wrong_actor_format(self):
        res = self.client().post('/actors',
                                 headers={'Authorization': 'Bearer {}'.format(CASTING_DIRECTOR_TOKEN)}, json={"foo": "bar"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_update_movie(self):
        res = self.client().patch('/movies/9',
                                  headers={'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)}, json={"title": "updated test"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_update_unauthorized_movie(self):
        res = self.client().patch('/movies/9',
                                  headers={'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT_TOKEN)}, json={"title": "updated test"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_404_not_existing_update_movie(self):
        res = self.client().patch('/movies/9999',
                                  headers={'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)}, json=DUMMY_MOVIE)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_actor(self):
        res = self.client().patch('/actors/11',
                                  headers={'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)}, json={"name": "updated test"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_update_unauthorized_actor(self):
        res = self.client().patch('/actors/11',
                                  headers={'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT_TOKEN)}, json={"name": "updated test"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_404_not_existing_update_actor(self):
        res = self.client().patch('/actors/9999',
                                  headers={'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)}, json=DUMMY_ACTOR)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie(self):
        res = self.client().delete('/movies/13',
                                   headers={'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_unauthorized_movie(self):
        res = self.client().delete('/movies/9',
                                   headers={'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_404_not_existing_delete_movie(self):
        res = self.client().delete('/movies/9999',
                                   headers={'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_actor(self):
        res = self.client().delete('/actors/12',
                                   headers={'Authorization': 'Bearer {}'.format(CASTING_DIRECTOR_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_unauthorized_actor(self):
        res = self.client().delete('/actors/13',
                                   headers={'Authorization': 'Bearer {}'.format(CASTING_ASSISTANT_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_404_not_existing_delete_actor(self):
        res = self.client().delete('/actors/9999',
                                   headers={'Authorization': 'Bearer {}'.format(EXECUTIVE_PRODUCER_TOKEN)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
