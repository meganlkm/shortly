from unittest import TestCase

from mock import patch

from shortly import ddb


class DdbTest(TestCase):

    @patch('shortly.ddb.get_table')
    def test_put(self, table_mock):
        ddb.put('foo', 'bar')
        table_mock.put_item.assert_called()

    def test_get(self):
        pass

    def test_lookup(self):
        pass
