import unittest
from src.get_xml import download_xml, well_formed_xml, store_xml


class TestGetXML(unittest.TestCase):
    def test_pos_download_xml(self):
        """Ensure that the XML file is being downloaded as expected
        """
        resp_stat_code, text = download_xml()
        self.assertEqual(resp_stat_code, 200)
        self.assertTrue(text)

    # TODO Failing test, may be issue with assert on exception
    def test_neg_download_xml(self):
        """Ensure that when a bad URL is given that a failing
        response code is returned and the text value is None
        """
        self.assertRaises(Exception, download_xml(
            url='mwmcguire.com'))

    def test_well_formed_xml(self):
        valid_xml = """
            <root>
                <child>Child A</child>
                <child>Child B</child>
            </root>
            """
        self.assertTrue(well_formed_xml(valid_xml))

    # TODO Failing test, may be issue with assert on exception
    def test_malformed_xml(self):
        malformed_xml = """
            <root
                <child>Child A</child>
            /root>
            """
        self.assertRaises(Exception, well_formed_xml(malformed_xml))

    def test_store_xml(self):
        """Ensure that once the XML is successfully downloaded it
        can be saved to disk for use later
        """
        self.assertEqual('./raw_data', store_xml())
        pass

    def test_path_exists(self):
        self.assertEqual('./raw_data', store_xml())

    def test_make_path(self):
        self.assertEqual('./raw_data', store_xml())

suite = unittest.TestLoader().loadTestsFromTestCase(TestGetXML)
unittest.TextTestRunner(verbosity=1).run(suite)
