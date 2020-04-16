from flask import current_app as app

from flaskapp import db, bcrypt
from flaskapp.tests.base import BaseTestCase

from flaskapp.models.users import User, Profile
from flaskapp.models.social import Post, Comment


class TestProfileModel(BaseTestCase):
    def test_user1_following_user2(self):
        hashed_password = bcrypt.generate_password_hash(
            self.TEST_USER_PASSWORD).decode('utf-8')

        self.user1 = User(email='testuser1@gmail.com',
                          username='testuser1',
                          password=hashed_password)
        self.user2 = User(email='testuser2@gmail.com',
                          username='testuser2',
                          password=hashed_password)

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

        self.profile1.follow(self.profile2)
        self.assertIn(self.profile2, self.profile1.followed.all())
        self.assertIn(self.profile1, self.profile2.followers.all())
        self.assertNotIn(self.profile2, self.profile1.followers.all())
        self.assertNotIn(self.profile1, self.profile2.followed.all())
        self.assertTrue(self.profile1.is_following(self.profile2))
        self.assertFalse(self.profile2.is_following(self.profile1))
        self.assertTrue(self.profile2.is_followed_by(self.profile1))
        self.assertFalse(self.profile1.is_followed_by(self.profile2))

    def test_profile_model(self):
        """
        Test number of records in Profile table
        """
        self.assertEqual(Profile.query.count(), 1)
