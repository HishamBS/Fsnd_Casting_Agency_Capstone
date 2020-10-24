import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import app

CASTING_ASSISTANT_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNsX1hreUs3blg0MTJQWmIyYXA3UyJ9.eyJpc3MiOiJodHRwczovL2hoYnMuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmOTM3ZTQ4OWI4ODIyMDA2ZWUwMDIxYiIsImF1ZCI6ImNhc3RpbmdfYWdlbmN5IiwiaWF0IjoxNjAzNTc4MzA2LCJleHAiOjE2MDM2NjQ3MDYsImF6cCI6ImNjVGhma3JSVDB5aFNpaUVMUU5Mc2VSaHlqWjZWTGwwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.iy4SlaRD_VFHTj6Mp8MGVEjic6YT6Hx8D-8P_dkluhNElLQU06pj2bAXgzUIctVeBjnAVwTZr1VwLnbSQD7-iP4PHFqq35SbIasOcGu5iCiJD2fKihbJFhurLF13JM0qabjZjfpiHy3YmVH9hOaImFN7rCkCiK1eNBYK7ThMglHM-KWHg-SUC8RsokyyB-04FmSxQ9cwJKdFxViqMmcuiVy3Q0jaD5ldKeHhL-KpmAzv1GoRD6AwVlT21my5R44Gn6jGR9K35S9mdKUzcs5WablKhMbDJB99DkJWxAjtQu9klG1ukI1j7w1pic_ew74UuzPRa0NbaJEB2yUraRfW3A"
CASTING_DIRECTOR_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNsX1hreUs3blg0MTJQWmIyYXA3UyJ9.eyJpc3MiOiJodHRwczovL2hoYnMuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmOTQxNzhhODg4NzA4MDA3MGZkYTI2MyIsImF1ZCI6ImNhc3RpbmdfYWdlbmN5IiwiaWF0IjoxNjAzNTc4NDQxLCJleHAiOjE2MDM2NjQ4NDEsImF6cCI6ImNjVGhma3JSVDB5aFNpaUVMUU5Mc2VSaHlqWjZWTGwwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIl19.NyUgXL_SbYIVdu1Y2Pwqk1RBc8Gp9ea0KGX6iF9qWiOz7oeNRRJTBDmukkCeNE-T9PCtvq-Pk5RHgW_GJBeSxgRZDltIwPzfxhigoMWitGrl-8fZde-KBstB0le4PFJsQ_x2oAzOGe-VOoyB1boyzHn0896Do5OwFUg64ReVhJTN8EHkBf5lgBSp0bmifQZqBvPtUtcfXytAnukzTyfGofcEWEg2DbEhwpr8B1Brd3RnhN9URLT2ZIIm4Fl73m26e2bjlozpbNtSaSBCl90-fJpFkhU-z3JvcTlfEK399jzjf9fXckpL7kxSZmPtBw93vi-RuAh33jieevxVX5LERg"
EXECUTIVE_PRODUCER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNsX1hreUs3blg0MTJQWmIyYXA3UyJ9.eyJpc3MiOiJodHRwczovL2hoYnMuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmOTQxODYyMzM2YTg4MDA3N2RkOWE1ZCIsImF1ZCI6ImNhc3RpbmdfYWdlbmN5IiwiaWF0IjoxNjAzNTc4NTIwLCJleHAiOjE2MDM2NjQ5MjAsImF6cCI6ImNjVGhma3JSVDB5aFNpaUVMUU5Mc2VSaHlqWjZWTGwwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.bOfvj6KYbrwaoWujjX9XoXmUmZTOlhQK46MdP4fKSa3aDi6oC403eAJPElab4OYGVJPOhDbv27MPbduLAnG4nHNmt4kaw9UERX7UtQioi42ldagjL0jkY878674n88wFXnl0LjUQECo8rkUBXcZaomHIR7CyJsdQ1h_0iA_u7kEG7Br8VlXxLs5EwoTpMsaN8erO8GG6uEXorH6eLOf9OWXx-sGhEAxFymj_BtcMhg_Q-ufX-Srrn9M_orlvwoAGMBcnvodAt6BfT0koiy2P7dS1tSFeA4nGiQOCdB1ylIuKHsJ_IdE5VyFA_NG8MNjBoXQvoD7RvsWEi80w6zQ4Tw"

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
