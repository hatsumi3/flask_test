import os
import sys
import tempfile
import unittest

# topdir = os.path.join(os.path.dirname(__file__), "..")
# sys.path.append(topdir)

from flask_blog import create_app, db
from flask_blog.scripts.db import InitDB, DropDB


class TestFlaskBlog(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///{}'.format(self.db_path)
        })
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        InitDB().run()

    def tearDown(self):
        DropDB().run()
        self.app_context.pop()
        os.unlink(self.db_path)


    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)


    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('tmp', 'tmp123')
        assert 'logged in'.encode() in rv.data
        rv = self.logout()
        assert 'logged out'.encode() in rv.data
        rv = self.login('admin', 'default')
        assert 'username is differense.'.encode() in rv.data
        rv = self.login('tmp', 'defaultx')
        assert 'password is differense.'.encode() in rv.data

if __name__ == '__main__':
    unittest.main()