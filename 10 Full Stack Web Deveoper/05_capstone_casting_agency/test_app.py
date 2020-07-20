import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import db, Movie, Actor

CASTING_ASSISTANT = {
    "Authorization": (
        "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtp"
        "ZCI6Ik93TGh1cE1sUEIweE1BdVRZeXNiSiJ9.eyJpc3MiOi"
        "JodHRwczovL2Rldi1vdWhhaWMxOS51cy5hdXRoMC5jb20vI"
        "iwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDgxMTQ3MzI0MzM4"
        "MjQ5NjE4MDAiLCJhdWQiOlsibW92aWVzIiwiaHR0cHM6Ly9"
        "kZXYtb3VoYWljMTkudXMuYXV0aDAuY29tL3VzZXJpbmZvIl"
        "0sImlhdCI6MTU5NTIyOTM3MiwiZXhwIjoxNTk1MzE1NzcyL"
        "CJhenAiOiJxbm9yUHBweE0ySzhWY0FFQzVYclZxOGFYQWhq"
        "cGIwRSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWw"
        "iLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om"
        "1vdmllcyJdfQ.k1ch0L9pZA-3ipoQ80MYu9lS-qQ8gT2CfV"
        "6IDsJfEWyVIMwU9RPy4HKT5p6ftB6RvUBEh0cSYiN94wEFf"
        "NrKIlEuKCiI-Zd7h3pvNxB0Te09MNjSs4jZ9UVP2jGhI7jD"
        "zB1qXrWHmYlee_wLV59FeJcuh8AXTss_lCj-SK0qWNKImCM"
        "NOwCCzD7gRLchykQ9T6gXLJBwcE88NbRdmshsJiqAUusmzr"
        "Ig5mJaXsK9jNi0WPiLW-aySb-uwFykwu4GvbeIiq98y8495"
        "JsaY1lmPozEdYnhHcuNPP-GocBh4HIMf0pn4vIWBym9T7pv"
        "C-27GaOHtluC_8Wewc74kshvlg"
    )
}

CASTING_DIRECTOR = {
    "Authorization": (
        "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZ"
        "CI6Ik93TGh1cE1sUEIweE1BdVRZeXNiSiJ9.eyJpc3MiOiJo"
        "dHRwczovL2Rldi1vdWhhaWMxOS51cy5hdXRoMC5jb20vIiwi"
        "c3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTYxNDA1MjkzMTk3NjM3"
        "NTA4MjIiLCJhdWQiOlsibW92aWVzIiwiaHR0cHM6Ly9kZXYt"
        "b3VoYWljMTkudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlh"
        "dCI6MTU5NTIyOTQyMywiZXhwIjoxNTk1MzE1ODIzLCJhenAi"
        "OiJxbm9yUHBweE0ySzhWY0FFQzVYclZxOGFYQWhqcGIwRSIs"
        "InNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJt"
        "aXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9y"
        "cyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRj"
        "aDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.o77aewn1aUv0S"
        "EdG0A2mkGY7iEDxzwY1KbbNnVrCWDBAa9dkgpJBLoJKZ6c0e"
        "rjx7OmELt3DkL_eIvhusCsxLBjkv1SlOVVBmz5XI943dzkhj"
        "rLnkm29x6kN9qq3VNJ93F2-4GIoyfPVU2WzqTvWhtSbewOgg"
        "XQoDKKthf9YJavd3gqi1WntTfzJTAbamLnMi6zJ7kla6PISZ"
        "2iQ1xB_JpMBDVST-xku1eA4NXoMD8lHubjJzcbcLBPJF2-CZ"
        "99Lq60Rn5s4Pmz5xrH8Ye7EfKXDuvELMat_qHuKvomT_77Gw"
        "snB92D9DaFCG8xp4zxx0f0ZragwUlf-QbcsWEWxLQ"
    )
}

EXECUTIVE_PRODUCER = {
    "Authorization": (
        "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZC"
        "I6Ik93TGh1cE1sUEIweE1BdVRZeXNiSiJ9.eyJpc3MiOiJodH"
        "RwczovL2Rldi1vdWhhaWMxOS51cy5hdXRoMC5jb20vIiwic3V"
        "iIjoiZ29vZ2xlLW9hdXRoMnwxMTAwNjcxNzAyOTQ2NjcyNzk4"
        "MTUiLCJhdWQiOlsibW92aWVzIiwiaHR0cHM6Ly9kZXYtb3VoY"
        "WljMTkudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MT"
        "U5NTIyOTQ3MCwiZXhwIjoxNTk1MzE1ODcwLCJhenAiOiJxbm9"
        "yUHBweE0ySzhWY0FFQzVYclZxOGFYQWhqcGIwRSIsInNjb3Bl"
        "Ijoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9uc"
        "yI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsIm"
        "dldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3J"
        "zIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0"
        "Om1vdmllcyJdfQ.TD0VkYTTKPxPS11qX84SqksgXMUaJqkYxc"
        "lhDRAT7rU84x5S8D4eCGTJhaFw1MXZinG1aYCcIKVmp8_5O1o"
        "QiLuiKgsEvLdqdkbsVSC0-oZ0_Otf7_ERUnsOZVXiwlf2IxQR"
        "MP9095VfhmjHaBM3vkJFNCUjfALDkpkAfKy_VXHp6wX1Ufmsk"
        "jpB0gzJm7TgnkWLmSx28_KbY5kiv9Zb2A9z5JlpPR6ZTqVXLg"
        "Jsrk3M_1yxdJAbQuPM1KBj6H5WQ96qCCcftXzDYd1fgPdXxzr"
        "26slxeXkbQb4ziSXCw-tPcN8JlKe0q7C5zYItXcBDgU3LLDv8"
        "woi4C7JdJTee_A"
    )
}

database_filename = "database_test.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(
    os.path.join(project_dir, database_filename))


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = database_path
        self.client = app.test_client
        db.drop_all()
        db.create_all()

        self.new_movie = {
            "title": "The Dark Knight Rises",
            "release_date": "2012-07-20"
        }

        self.new_movie_patch = {
            "title": "The Dark Knight Rises A Fire Will Rise",
            "release_date": "2012-07-20"
        }

        self.new_actor = {
            "name": "Anne Hathaway",
            "age": 38,
            "gender": "Female"
        }

        self.new_actor_patch = {
            "name": "Anne Jacqueline Hathaway",
            "age": 38,
            "gender": "Female"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_403_insert_movies(self):
        res = self.client().post(
            '/movies',
            headers=CASTING_DIRECTOR,
            json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_200_insert_movies(self):
        res = self.client().post(
            '/movies',
            headers=EXECUTIVE_PRODUCER,
            json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['movies'])

    def test_403_insert_actors(self):
        res = self.client().post(
            '/actors',
            headers=CASTING_ASSISTANT,
            json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_200_insert_actors(self):
        res = self.client().post(
            '/actors',
            headers=CASTING_DIRECTOR,
            json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['actors'])

    def test_403_update_movies(self):
        res = self.client().post(
            '/movies',
            headers=EXECUTIVE_PRODUCER,
            json=self.new_movie)
        res = self.client().patch(
            '/movies/1',
            headers=CASTING_ASSISTANT,
            json=self.new_movie_patch
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_200_update_movies(self):
        res = self.client().post(
            '/movies',
            headers=EXECUTIVE_PRODUCER,
            json=self.new_movie)
        res = self.client().patch(
            '/movies/1',
            headers=CASTING_DIRECTOR,
            json=self.new_movie_patch
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['movies'])

    def test_403_update_actors(self):
        res = self.client().post(
            '/actors',
            headers=CASTING_DIRECTOR,
            json=self.new_actor)
        res = self.client().patch(
            '/actors/1',
            headers=CASTING_ASSISTANT,
            json=self.new_actor_patch
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_200_update_actors(self):
        res = self.client().post(
            '/actors',
            headers=CASTING_DIRECTOR,
            json=self.new_actor)
        res = self.client().patch(
            '/actors/1',
            headers=CASTING_DIRECTOR,
            json=self.new_actor_patch
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['actors'])

    def test_403_delete_movies(self):
        res = self.client().post(
            '/movies',
            headers=EXECUTIVE_PRODUCER,
            json=self.new_movie)
        res = self.client().delete(
            '/movies/1',
            headers=CASTING_ASSISTANT,
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_200_delete_movies(self):
        res = self.client().post(
            '/movies',
            headers=EXECUTIVE_PRODUCER,
            json=self.new_movie)
        res = self.client().delete(
            '/movies/1',
            headers=EXECUTIVE_PRODUCER,
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)

    def test_403_delete_actors(self):
        res = self.client().post(
            '/actors',
            headers=CASTING_DIRECTOR,
            json=self.new_actor)
        res = self.client().delete(
            '/actors/1',
            headers=CASTING_ASSISTANT,
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_200_delete_actors(self):
        res = self.client().post(
            '/actors',
            headers=CASTING_DIRECTOR,
            json=self.new_actor)
        res = self.client().delete(
            '/actors/1',
            headers=CASTING_DIRECTOR,

        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)

    def test_401_get_movies(self):
        res = self.client().get(
            '/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_200_get_movies(self):
        res = self.client().post(
            '/movies',
            headers=EXECUTIVE_PRODUCER,
            json=self.new_movie)
        res = self.client().get(
            '/movies',
            headers=CASTING_ASSISTANT
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['movies'])
        self.assertTrue(data['total_movies'] > 0)

    def test_401_get_actors(self):
        res = self.client().get(
            '/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_200_get_actors(self):
        res = self.client().post(
            '/actors',
            headers=CASTING_DIRECTOR,
            json=self.new_actor)
        res = self.client().get(
            '/actors',
            headers=CASTING_ASSISTANT
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['actors'])
        self.assertTrue(data['total_actors'] > 0)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
