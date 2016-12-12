import os
import unittest
from src.get_xml import download_xml
from src.get_xml import well_formed_xml
from src.get_xml import store_xml
from src.get_xml import path_is_valid


class TestGetXML(unittest.TestCase):
    def setUp(self):
        self.valid_xml = """
            <root>
                <child>Child A</child>
                <child>Child B</child>
            </root>
            """
        self.malformed_xml = """
            <root
                <child>Child A</child>
            /root>
            """
        self.test_dir = '/TEST_DATA'

    def test_pos_download_xml(self):
        """Ensure that the XML file is being downloaded as expected
        """
        resp_stat_code, content = download_xml()
        self.assertEqual(resp_stat_code, 200)
        self.assertTrue(content)

    def test_neg_download_xml(self):
        """Ensure that when a bad URL is given that a failing
        response code is returned and the text value is None
        """
        self.assertRaises(Exception, download_xml(
            url='mwmcguire.com'))

    def test_well_formed_xml(self):
        """Ensure that the XML is formatted validly
        """
        self.assertTrue(well_formed_xml(self.valid_xml))

    def test_malformed_xml(self):
        self.assertRaises(Exception, well_formed_xml(
            self.malformed_xml))

    def test_path_is_valid(self):
        """Ensure that the path given is valid and a directory
        """
        self.assertFalse(path_is_valid('./fake_path'))
        self.assertTrue(path_is_valid(os.getcwd()))

    def test_store_xml_no_dir(self):
        """Ensure that when the directory is not present that it can
        be created and the downloaded XML can be saved to disk
        """
        self.assertEqual(None, store_xml())

    def test_store_xml_dir_present(self):
        """Ensure that when the directory is already present that the
        downloaded XML file can be written to disk
        """
        self.assertEqual(True, path_is_valid(os.getcwd()))

    def tearDown(self):
        # Remove the test XML File Dir after each run
        pass

suite = unittest.TestLoader().loadTestsFromTestCase(TestGetXML)
unittest.TextTestRunner(verbosity=2).run(suite)
