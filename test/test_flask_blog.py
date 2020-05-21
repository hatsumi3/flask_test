import os
import sys
import tempfile
import unittest
# import pytest

# topdir = os.path.join(os.path.dirname(__file__), "..")
# sys.path.append(topdir)
from flask import session

from flask_blog import create_app, db
from flask_blog.scripts.db import InitDB, DropDB
from flask_blog.models.entries import Entry


class TestFlaskBlog(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        print()
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
        with self.client:
            rv = self.login('tmp', 'tmp123')
            assert 'logged in'.encode() in rv.data
            assert session['logged_in']
            rv = self.logout()
            assert 'logged out'.encode() in rv.data
            rv = self.login('admin', 'default')
            assert 'username is differense.'.encode() in rv.data
            rv = self.login('tmp', 'defaultx')
            assert 'password is differense.'.encode() in rv.data

    def test_404_error(self):
        rv = self.client.post('/loginlogin')
        assert rv.status_code == 302


    def test_entries(self):
        with self.client:
            rv = self.login('tmp', 'tmp123')
            assert 'logged in'.encode() in rv.data
            rv = self.client.get('/users/entries/new')
            assert rv.status_code == 200
            # print(rv.get_data(as_text=True))

            rv = self.client.post('/users/entries', data=dict(
                title='おもち',
                text='おもちもちもち'
            ), follow_redirects=True)
            assert rv.status_code == 200
            assert 'new article is created!'.encode() in rv.data
            # print(rv.get_data(as_text=True))

            rv = self.client.get('/users/entries/1')
            assert rv.status_code == 200

            rv = self.client.get('/users/entries/1/edit')
            assert rv.status_code == 200

            rv = self.client.post('/users/entries/1/update', data=dict(
                title='おもち',
                text='おもちもちお'
            ), follow_redirects=True)
            assert rv.status_code == 200
            assert 'article is updated!'.encode() in rv.data
            # print(rv.get_data(as_text=True))

            rv = self.client.post('/users/entries/1/delete', 
                                  follow_redirects=True)
            assert rv.status_code == 200
            assert 'article is deleted ...'.encode() in rv.data
            # print(rv.get_data(as_text=True))

    def test_entry_repr(self):
        entry = Entry(
            title='おもち',
            text='おもちもちお'
        )
        db.session.add(entry)
        db.session.commit()
    
        assert '<Entry id:1 title:おもち text: おもちもちお>' in str(entry)
    

if __name__ == '__main__':
    unittest.main()