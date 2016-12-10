from src.get_xml import download_xml
from src.get_xml import store_xml
from unittest import TestCase


class TestGetXML(TestCase):
    def test_download_xml(self):
        """Ensure that the XML file is being downloaded as expected"""
        func = download_xml
        pass

    def test_store_xml(self):
        """Ensure that once the XML is successfully downloaded it can
        be saved to disk for use later
        """
        func = store_xml
        pass
