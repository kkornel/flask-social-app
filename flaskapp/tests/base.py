from flask import Flask, current_app as app

from flask_testing import TestCase

from flaskapp import db, bcrypt
from flaskapp.models.users import User, Profile
from flaskapp.models.social import Post, Comment
"""
Running Tests
In the simplest case, go to the directory that includes your project source and run nose2 there:

nose2
"""


class BaseTestCase(TestCase):
    TEST_USER_EMAIL = 'user1@gmail.com'
    TEST_USER_USERNAME = 'user1'
    TEST_USER_PASSWORD = 'test'
    TEST_HASHED_PASSWORD = bcrypt.generate_password_hash(
        TEST_USER_PASSWORD).decode('utf-8')

    def create_app(self):
        from flaskapp import create_app
        from flaskapp.config import TestConfig

        app = create_app(TestConfig)
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        db.create_all()

        user = User(
            email=self.TEST_USER_EMAIL,
            username=self.TEST_USER_USERNAME,
            password=self.TEST_HASHED_PASSWORD,
        )
        user.active = True

        db.session.add(user)
        db.session.commit()

        profile = Profile(user_id=user.id, user=user)

        db.session.add(profile)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """
        db.session.remove()
        db.drop_all()

    def login(self, email, password):
        return self.client.post(
            '/login/',
            data=dict(email=email, password=password),
            follow_redirects=True,
        )

    def logout(self):
        return self.client.get(
            '/logout/',
            follow_redirects=True,
        )