from datetime import datetime

from flask import url_for, current_app as app, request, g
from flask_testing import TestCase

from flaskapp import db, bcrypt
from flaskapp.tests.base import BaseTestCase

from flaskapp.models.users import User, Profile
from flaskapp.models.social import Post, Comment


class TestViews(BaseTestCase):
    def test_homepage_view(self):
        """
        Test that homepage is accessible with login
        """
        self.login(self.TEST_USER_EMAIL, self.TEST_USER_PASSWORD)
        response = self.client.get(url_for('main.home'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_redirect_view(self):
        """
        Test that dashboard is inaccessible without login
        and redirects to login page then to homepage
        """
        target_url = url_for('main.home')
        redirect_url = url_for('users.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


class TestProfileView(BaseTestCase):
    def test_view_url_accessible_by_name(self):
        self.login(self.TEST_USER_EMAIL, self.TEST_USER_PASSWORD)
        response = self.client.get(
            url_for('users.profile', username=self.TEST_USER_USERNAME))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.login(self.TEST_USER_EMAIL, self.TEST_USER_PASSWORD)
        response = self.client.get(
            url_for('users.profile', username=self.TEST_USER_USERNAME))
        self.assertEquals(response.status_code, 200)
        self.assert_template_used('users/profile.html')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            url_for('users.profile', username=self.TEST_USER_USERNAME))
        self.assertRedirects(response,
                             f'/login/?next=%2F{self.TEST_USER_USERNAME}%2F')


class TestPostUpdateView(TestCase):
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

        self.user1 = User(
            email='user1@mail.com',
            username='user1',
            password=self.TEST_HASHED_PASSWORD,
        )
        self.user2 = User(
            email='user2@mail.com',
            username='user2',
            password=self.TEST_HASHED_PASSWORD,
        )
        self.user1.active = True
        self.user2.active = True

        db.session.add(self.user1)
        db.session.add(self.user2)
        db.session.commit()

        self.profile1 = Profile(user_id=self.user1.id, user=self.user1)
        self.profile2 = Profile(user_id=self.user2.id, user=self.user2)

        db.session.add(self.profile1)
        db.session.add(self.profile2)
        db.session.commit()

        self.post1 = Post(
            author_id=self.profile1.id,
            content='Post1',
            location='Tomaszów Mazowiecki',
        )
        self.post2 = Post(
            author_id=self.profile2.id,
            content='Post2',
            location='Tomaszów Mazowiecki',
        )
        db.session.add(self.post1)
        db.session.add(self.post2)
        db.session.commit()

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

    def tearDown(self):
        """
        Will be called after every test
        """
        db.session.remove()
        db.drop_all()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            url_for('social.post_update', post_id=self.post1.id))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f'/login/?next=%2Fpost%2F{self.post1.id}%2Fupdate%2F')

    def test_redirect_if_logged_in_but_not_correct_persmission(self):
        self.login(self.user1.email, self.TEST_USER_PASSWORD)

        response = self.client.get(
            url_for('social.post_update', post_id=self.post2.id))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_with_permission_granted(self):
        self.login(self.user1.email, self.TEST_USER_PASSWORD)
        response = self.client.get(
            url_for('social.post_update', post_id=self.post1.id))
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_post_if_logged_in(self):
        # unlikely UID to match any post
        test_uid = 6786856
        self.login(self.user1.email, self.TEST_USER_PASSWORD)
        response = self.client.get(
            url_for('social.post_update', post_id=test_uid))
        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        self.login(self.user1.email, self.TEST_USER_PASSWORD)
        response = self.client.get(
            url_for('social.post_update', post_id=self.post1.id))
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('social/post_update.html')

    def test_redirects_to_post_detail_on_success(self):
        self.login(self.user1.email, self.TEST_USER_PASSWORD)
        response = self.client.post(
            '/new/',
            data={
                'author': self.user1.profile,
                'content': 'TEST',
                'date_posted': datetime.utcnow(),
                'location': 'Tomaszów Mazowiecki',
            },
        )
        self.assertRedirects(response, 'post/3/')


class TestPostCreateView(BaseTestCase):
    def test_post_create_POST(self):
        self.login(self.TEST_USER_EMAIL, self.TEST_USER_PASSWORD)
        profile = User.query.filter_by(
            username=self.TEST_USER_USERNAME).first().profile
        response = self.client.post(
            '/new/',
            data={
                'author': profile,
                'content': 'TEST',
                'date_posted': datetime.utcnow(),
                'location': 'Tomaszów Mazowiecki',
            },
        )
        post = Post.query.get(1)
        self.assertEqual(Post.query.count(), 1)
        self.assertEqual(post.author, profile)
        self.assertEquals(post.content, 'TEST')