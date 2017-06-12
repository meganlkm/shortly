from unittest import TestCase

from mock import patch, MagicMock

import shortly


class ShortlyTest(TestCase):

    @patch('shortly.get', return_value=False)
    @patch('shortly.ddb.get_client')
    def test_create(self, put_mock, get_mock):
        rec = shortly.create('foo')
        self.assertTrue(rec.startswith('example.com/'))

    @patch('shortly.ddb.get_client')
    def test_retrieve(self, client_mock):
        client_mock.return_value.Table = MagicMock()
        client_mock.return_value.Table.return_value.query = MagicMock(
            return_value={
                'Items': [
                    {'id': 'foo', 'url': 'bar'}
                ]
            }
        )
        self.assertEqual(shortly.retrieve('foo'), 'FORWARDING TO bar')

    @patch('shortly.ddb.get_client')
    def test_retrieve_404(self, client_mock):
        client_mock.return_value.Table = MagicMock()
        client_mock.return_value.Table.return_value.query = MagicMock(return_value={'Items': []})
        self.assertEqual(shortly.retrieve('foo'), '404')
