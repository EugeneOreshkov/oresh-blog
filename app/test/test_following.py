from datetime import datetime, timezone, timedelta

from app.models import User, Post
from app import db

class TestFollowing:
    def test_follow(self, user_pair, client):
        """Test user following functionality."""       

        user1, user2 = user_pair

        following = db.session.scalars(user1.following.select()).all()
        followers = db.session.scalars(user2.followers.select()).all()
        assert following == []
        assert followers == []

        user1.follow(user2)
        db.session.commit()

        assert user1.is_following(user2) is True
        assert user2.followers_count() == 1
        assert user1.following_count() == 1

        user1_following = db.session.scalars(user1.following.select()).all()
        user2_followers = db.session.scalars(user2.followers.select()).all()
        assert user1_following[0].username == 'user2'
        assert user2_followers[0].username == 'user1'

    def test_unfollow(self, user_pair, client):
        """Test user unfollowing functionality."""       

        user1, user2 = user_pair

        user1.follow(user2)
        db.session.commit()

        assert user1.is_following(user2) is True
        assert user2.followers_count() == 1

        user1.unfollow(user2)
        db.session.commit()

        assert user1.is_following(user2) is False
        assert user2.followers_count() == 0
        assert user1.following_count() == 0
    
    def test_followers_count(self, user_pair, client):
        """Test followers count functionality."""       

        user1, user2 = user_pair

        assert user1.followers_count() == 0
        assert user2.followers_count() == 0

        user1.follow(user2)
        db.session.commit()

        assert user1.followers_count() == 0
        assert user2.followers_count() == 1

    def test_follow_posts(self, user_pair, client):
        """Test fetching posts from followed users."""        
        
        user1, user2 = user_pair
        # Additionally, create two more users to test fetching posts
        user3 = User(username='user3', email='user3@example.com', phone='1234567892')
        user4 = User(username='user4', email='user4@example.com', phone='1234567893')
        user3.set_password('password123')
        user4.set_password('password123')
        db.session.add_all([user3, user4])

        now = datetime.now(timezone.utc)

        # Create four posts
        post1 = Post(body="post from user1", title="Post 1", author=user1, timestamp=now + timedelta(seconds=1))
        post2 = Post(body="post from user2", title="Post 2", author=user2, timestamp=now + timedelta(seconds=2))
        post3 = Post(body="post from user3", title="Post 3", author=user3, timestamp=now + timedelta(seconds=3))
        post4 = Post(body="post from user4", title="Post 4", author=user4, timestamp=now + timedelta(seconds=4))
        db.session.add_all([post1, post2, post3, post4])
        db.session.commit() 

        # Setup the followers        
        user1.follow(user2)
        user1.follow(user3)
        user1.follow(user4)        
        user2.follow(user3)
        user2.follow(user4)
        user3.follow(user4)
        user4.follow(user1)
        db.session.commit()

        # Check the followed posts for each user
        user1_followed_posts = db.session.scalars(user1.following_posts()).all()
        user2_followed_posts = db.session.scalars(user2.following_posts()).all()
        user3_followed_posts = db.session.scalars(user3.following_posts()).all()
        user4_followed_posts = db.session.scalars(user4.following_posts()).all()

        assert list(user1_followed_posts) == [post4, post3, post2, post1]
        assert list(user2_followed_posts) == [post4, post3, post2]
        assert list(user3_followed_posts) == [post4, post3]
        assert list(user4_followed_posts) == [post4, post1]