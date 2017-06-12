from unittest import TestCase

from mock import patch, MagicMock

from shortly import ddb


class DdbTest(TestCase):

    @patch('shortly.ddb.get_client')
    def test_put(self, client_mock):
        client_mock.return_value.Table = MagicMock()
        client_mock.return_value.Table.return_value.put_item = MagicMock()

        self.assertTrue(ddb.put('foo', 'bar'))
        client_mock.assert_called_once_with('dynamodb', 'resource')
        client_mock.return_value.Table.assert_called_once_with('shortly-urls')
        client_mock.return_value.Table.return_value.put_item.assert_called_once_with(Item={'id': 'foo', 'url': 'bar'})

    @patch('shortly.ddb.get_client')
    @patch('shortly.ddb.Key')
    def test_get(self, key_mock, client_mock):
        client_mock.return_value.Table = MagicMock()
        client_mock.return_value.Table.return_value.query = MagicMock()

        ddb.get('foo')
        client_mock.return_value.Table.return_value.query.assert_called_once()

    @patch('shortly.ddb.get_client')
    @patch('shortly.ddb.Key')
    def test_get_not_found(self, key_mock, client_mock):
        client_mock.return_value.Table = MagicMock()
        client_mock.return_value.Table.return_value.query = MagicMock(return_value={'Items': []})
        self.assertFalse(ddb.get('foo'))

    def test_lookup(self):
        pass
