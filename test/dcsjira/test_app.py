import unittest
from dcsjira.app import app


class AppTest(unittest.TestCase):

    def setUp(self):
        app.config.from_object('config.TestingConfig')
        app.config['PORT'] = 5000
        self.app = app.test_client()

    def test_get_status(self):
        # test case for non-existed batch id
        url = '/get_status/%s/%s' % ('12345678', '2')
        res = self.app.get(url)
        self.assertEqual(200, res.status_code)
        self.assertTrue('SMS delivery status for batch id:' in res.data)

        # test case for invalid batch id
        url = '/get_status/%s/%s' % ('12345678f', '2')
        res = self.app.get(url)
        self.assertEqual(200, res.status_code)
        self.assertTrue('Internal System Error' in res.data)

        # test case for valid batch id
        url = '/get_status/%s/%s' % ('768791424', '2')
        res = self.app.get(url)
        self.assertEqual(200, res.status_code)
        self.assertTrue('Please refresh (Ctrl + r) the page to update the status' in res.data)

    def test_get_image(self):
        # test case for getting image
        url = '/get_image/%s/%s' % ('768791424', '2')
        res = self.app.get(url)
        self.assertEqual(200, res.status_code)
        self.assertEqual(res.headers['Content-Type'], 'image/png')
