from flask import current_app as app

from flaskapp.tests.base import BaseTestCase

from flaskapp.models.users import User, Profile
from flaskapp.models.social import Post, Comment


class FlaskTestCase(BaseTestCase):
    def test_login_response(self):
        response = self.client.get('/login/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_main_route_requires_login(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

    def test_assert_register_template_used(self):
        response = self.client.get("/register/")
        self.assert_template_used('users/register.html')

    def test_api_json_response(self):
        response = self.client.get("/api/resources/user/1/")
        self.assertEquals(response.json['status'], 'success')