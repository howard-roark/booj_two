import os
import unittest
import xml.etree.ElementTree as eT
from src.transform_xml import TransformXML
from src.transform_xml import update_criteria_file
from src.transform_xml import requirements_met
from config_TEST import test_constants as constant


def clear_test_criteria():
    """Remove all the test criteria files from the previous test run
    """
    criteria_file = '{cwd}{dir_file}'.format(
        cwd=os.getcwd(),
        dir_file='/test/config_TEST/test_transform.criteria')
    open(criteria_file, 'w').close()


class NonBlankFileTransform(unittest.TestCase):
    """Class to make the setup for test cases with different contexts
    to be logically separated.

    This class sets the context for the test cases that are run when
    there is no valid criteria file or it is blank
    """

    def setUp(self):
        # clear_old_test_data()
        # Writing a timestamp to a new test criteria file
        test_cf = '{cwd}{file}'.format(cwd=os.getcwd(),
                                       file='/test/config_TEST'
                                            '/test_transform.criteria')
        with open(test_cf, 'wt') as cf:
            # Using a low number as the timestamp to keep testing easy
            cf.write('10')

        self.t_xml = TransformXML()
        self.t_xml.data_dir = '/test/data_TEST/'
        self.t_xml.criteria = '/test/config_TEST/test_transform' \
                              '.criteria'


class TestTransformXMLWithCF(NonBlankFileTransform):
    """Test cases for when the criteria file has a valid timestamp
    """

    def test_get_new_input(self):
        expected_files = ['10_transform_test.xml',
                          '20_transform_test.xml']
        obtained_files = self.t_xml.get_new_input()
        for ef in expected_files:
            self.assertTrue(ef in obtained_files)

    def test_criteria_file_updated(self):
        with open('{}{}'.format(os.getcwd(), self.t_xml.criteria),
                  'rt') as cf:
            # TODO need a failing test
            criteria_file = '{}{}'.format(os.getcwd(),
                                          self.t_xml.criteria)
            data_files = os.listdir('{}{}'.format(os.getcwd(),
                                                  self.t_xml.data_dir))
            update_criteria_file(criteria_file, data_files)
            '''Assert that the criteria file has a timestamp of at
            least 20.  The oldest file used for this test will be 20
            ms or the timestamp of one of the files created from the
            GetXML test suite.
            '''
            self.assertTrue(cf.readline() >= 20)

    def test_requirements_met(self):
        # Negative test
        listing_node = eT.Element(constant.CONST_LISTING)
        basic_details_node = eT.SubElement(
            listing_node, constant.CONST_BASIC_DETAILS)
        description_node = eT.SubElement(
            basic_details_node, constant.CONST_DESC)
        description_node.text = 'Lions or Tigers or Bears'
        listing_details_node = eT.SubElement(
            listing_node, constant.CONST_LISTING_DETAILS)
        date_listed_node = eT.SubElement(
            listing_details_node, constant.CONST_DATE_LISTED)
        date_listed_node.text = '2016-01-01'
        self.assertFalse(requirements_met(listing_node))

        # Positive test
        description_node.text = 'Lions and Tigers and Bears'
        self.assertTrue(requirements_met(listing_node))

    def test_sort_tree(self):
        """Test that an un-sorted tree can be passed in and tree sorted
        by date will be returned
        """

    def test_subnode_vals(self):
        pass

    def test_get_row(self):
        """When a valid Listing is passed into get row it should be able
        to parse the required data and return a list to be written as a
        row to the CSV
        """
        pass

    def test_write_csv(self):
        pass


class BlankTransformFile(unittest.TestCase):
    """Class to make the setup for test cases with different contexts
    to be logically separated.

    This class sets the context for the test cases that are run when
    there is a valid criteria file that is not blank
    """

    def setUp(self):
        clear_test_criteria()

        self.t_xml = TransformXML()
        self.t_xml.data_dir = '/test/data_TEST/'
        self.t_xml.criteria = '/test/config_TEST/test_transform' \
                              '.criteria '


class TestTransformXMLNoDate(BlankTransformFile):
    """Test cases when the criteria file is blank
    """

    def test_get_new_input(self):
        """Expecting all 3 files to be returned in the list from
        function
        """
        expected_files = ['1_transform_test.xml',
                          '10_transform_test.xml',
                          '20_transform_test.xml']
        obtained_files = self.t_xml.get_new_input()
        for ef in expected_files:
            self.assertTrue(ef in obtained_files)
