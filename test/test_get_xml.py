import os
import unittest
from src.get_xml import GetXML
from src.get_xml import well_formed_xml
from src.get_xml import path_is_valid


def clear_old_test_data():
    """Remove all the test data from the previous test run
    """
    folder = '{}{}'.format(os.getcwd(), '/data_TEST/')
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


class TestGetXML(unittest.TestCase):
    def setUp(self):
        self.valid_xml = "<root><child>Child A</child><child>Child " \
                         "B</child></root> "
        self.malformed_xml = "<root<child>Child A</child>/root>"
        self.test_dir = '/data_TEST'
        self.gX = GetXML()
        self.gX.data_dir = '/data_TEST/'

        self.badGX = GetXML(url='mwmcguire.com')
        self.badGX.data_dir = '/data_TEST/'

    def test_well_formed_xml(self):
        """Ensure that the XML is formatted validly
        """
        self.assertTrue(well_formed_xml(self.valid_xml))

    def test_malformed_xml(self):
        self.assertRaises(Exception, well_formed_xml(
            self.malformed_xml))

    def test_path_is_valid(self):
        """Ensure that the path given is valid if the directory
        exists
        """
        self.assertTrue(path_is_valid(os.getcwd()))

    def test_store_xml_no_dir(self):
        """Ensure that when the directory is not present that it can
        be created and the downloaded XML can be saved to disk
        """
        self.assertEqual(None, self.gX.store_xml(self.valid_xml,
                                                 '_TEST_FILE.xml'))

    def test_store_xml_dir_present(self):
        """Ensure that when the directory is already present that the
        downloaded XML file can be written to disk
        """
        pass

    def test_pos_download_xml(self):
        """Ensure that the XML file is being downloaded as expected
        """
        # Clear the data from the last test run, but leave the data
        # from this run
        clear_old_test_data()
        resp_stat_code, content = self.gX.download_xml()
        self.assertEqual(resp_stat_code, 200)
        self.assertTrue(content)

    def test_neg_download_xml(self):
        """Ensure that when a bad URL is given that a failing
        response code is returned and the text value is None
        """
        self.assertRaises(Exception, self.badGX.download_xml())


suite = unittest.TestLoader().loadTestsFromTestCase(TestGetXML)
unittest.TextTestRunner(verbosity=2).run(suite)
