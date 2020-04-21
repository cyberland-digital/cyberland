import os
import unittest

from flaskr import create_app, db

app = create_app()

TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['DATABASE_URL'] = 'sqlite:///' + \
            os.path.join(app.config['BASE_PATH'], TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
