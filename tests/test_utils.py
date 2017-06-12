from unittest import TestCase

from shortly import utils


class UtilsTest(TestCase):

    def test_get_client(self):
        s3 = utils.get_client('s3', client_type='resource')
        self.assertEquals(str(type(s3)), "<class 'boto3.resources.factory.s3.ServiceResource'>")
