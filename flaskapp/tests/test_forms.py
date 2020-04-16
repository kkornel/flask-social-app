from flask import current_app as app
from flask_testing import TestCase

from flaskapp.tests.base import BaseTestCase
from flaskapp.users.forms import RegistrationForm
from flaskapp.social.forms import PostCreateForm


class TestRegistrationForm(BaseTestCase):
    def test_form_username_label(self):
        form = RegistrationForm()
        self.assertTrue(form.username.label.text == 'Username')

    def test_form_valid_data(self):
        form = RegistrationForm(
            data={
                'email': 'testuser@gmail.com',
                'username': 'testuser',
                'password': 'TemporaryPass123!',
                'confirm_password': 'TemporaryPass123!',
            })
        self.assertTrue(form.validate())

    def test_user_already_existss(self):
        # User exists
        form = RegistrationForm(
            data={
                'email': 'user@gmail.com',
                'username': 'user1',
                'password': 'TemporaryPass123!',
                'confirm_password': 'TemporaryPass123!',
            })
        self.assertFalse(form.validate())
        self.assertEquals(len(form.errors), 1)

    def test_form_not_valid_email(self):
        form = RegistrationForm(
            data={
                'email': 'testuser@gmail',
                'username': 'testuser',
                'password': 'TemporaryPass123!',
                'confirm_password': 'TemporaryPass123!',
            })
        self.assertFalse(form.validate())
        self.assertEquals(len(form.errors), 1)

        form = RegistrationForm(
            data={
                'email': 'testusergmail.com',
                'username': 'testuser',
                'password': 'TemporaryPass123!',
                'confirm_password': 'TemporaryPass123!',
            })
        self.assertFalse(form.validate())
        self.assertEquals(len(form.errors), 1)

        form = RegistrationForm(
            data={
                'email': '@gmail',
                'username': 'testuser',
                'password': 'TemporaryPass123!',
                'confirm_password': 'TemporaryPass123!',
            })
        self.assertFalse(form.validate())
        self.assertEquals(len(form.errors), 1)

        form = RegistrationForm(
            data={
                'email': 'testuser@',
                'username': 'testuser',
                'password': 'TemporaryPass123!',
                'confirm_password': 'TemporaryPass123!',
            })
        self.assertFalse(form.validate())
        self.assertEquals(len(form.errors), 1)

        form = RegistrationForm(
            data={
                'email': '@gmail.com',
                'username': 'testuser',
                'password': 'TemporaryPass123!',
                'confirm_password': 'TemporaryPass123!',
            })
        self.assertFalse(form.validate())
        self.assertEquals(len(form.errors), 1)

        form = RegistrationForm(
            data={
                'email': '',
                'username': 'testuser',
                'password': 'TemporaryPass123!',
                'confirm_password': 'TemporaryPass123!',
            })
        self.assertFalse(form.validate())
        self.assertEquals(len(form.errors), 1)

    def test_form_not_valid_username(self):
        form = RegistrationForm(
            data={
                'email': 'testuser@gmail.com',
                'username': 'user1',
                'password': 'TempraryPass123!',
                'confirm_password': 'TempraryPass123!',
            })
        self.assertFalse(form.validate())
        self.assertEquals(len(form.errors), 1)

        form = RegistrationForm(
            data={
                'email': 'testuser@gmail.com',
                'username': '',
                'password': 'TempraryPass123!',
                'confirm_password': 'TempraryPass123!',
            })
        self.assertFalse(form.validate())
        self.assertEquals(len(form.errors), 1)

        form = RegistrationForm(
            data={
                'email': 'testuser@gmail.com',
                'username': 'MORETHAN20MORETHAN20MORETHAN20MORETHAN20',
                'password': 'TempraryPass123!',
                'confirm_password': 'TempraryPass123!',
            })
        self.assertFalse(form.validate())
        self.assertEquals(len(form.errors), 1)

    def test_form_not_valid_password(self):
        form = RegistrationForm(
            data={
                'email': 'testuser@gmail.com',
                'username': 'user2',
                'password': '',
                'confirm_password': 'TempraryPass123!',
            })
        self.assertFalse(form.validate())
        self.assertEquals(len(form.errors), 2)

        form = RegistrationForm(
            data={
                'email': 'testuser@gmail.com',
                'username': 'user2',
                'password': 'TempraryPass123!',
                'confirm_password': '',
            })
        self.assertFalse(form.validate())
        self.assertEquals(len(form.errors), 1)

        form = RegistrationForm(
            data={
                'email': 'testuser@gmail.com',
                'username': 'user2',
                'password': 'Match',
                'confirm_password': 'NoMatchNoMatch',
            })
        self.assertFalse(form.validate())
        self.assertEquals(len(form.errors), 2)

        form = RegistrationForm(
            data={
                'email': 'testuser@gmail.com',
                'username': 'user2',
                'password': '1234',
                'confirm_password': '1234',
            })
        self.assertFalse(form.validate())
        self.assertEquals(len(form.errors), 1)

        form = RegistrationForm(
            data={
                'email': 'testuser@gmail.com',
                'username': 'user2',
                'password': 'test123',
                'confirm_password': 'test123',
            })
        self.assertFalse(form.validate())
        self.assertEquals(len(form.errors), 1)

    def test_form_no_data(self):
        form = RegistrationForm(data={})
        self.assertFalse(form.validate())
        self.assertEquals(len(form.errors), 4)


class TestPostCreateForm(BaseTestCase):
    def test_form_content_label(self):
        form = PostCreateForm()
        self.assertTrue(form.content.label.text == 'Content')

    def test_form_valid_data(self):
        form = PostCreateForm(
            data={
                'content':
                'Today is the first day of the Spring, it is Saturday 10AM and I am learning how to write tests in Django.',
                'location': 'Tomaszów Mazowiecki'
            })
        self.assertTrue(form.validate())

    def test_form_not_valid_data(self):
        form = PostCreateForm(
            data={
                'content':
                'More than 280 characters. More than 280 characters. More than 280 characters. More than 280 characters. More than 280 characters. More than 280 characters. More than 280 characters. More than 280 characters. More than 280 characters. More than 280 characters. More than 280 characters. More than 280 characters.',
                'location': 'More than 40 characters. More than 40 characters.'
            })
        self.assertFalse(form.validate())

    def test_form_no_data(self):
        form = PostCreateForm(data={})
        self.assertFalse(form.validate())
        self.assertEquals(len(form.errors), 1)