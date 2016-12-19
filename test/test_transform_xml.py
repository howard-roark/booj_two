import os
import unittest


def clear_test_criteria():
    """Remove all the test criteria files from the previous test run
    """
    folder = '{}{}'.format(os.getcwd(), '/config_TEST/')
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


class NonBlankFileTransform(unittest.TestCase):
    """Class to make the setup for test cases with different contexts
    to be logically separated.

    This class sets the context for the test cases that are run when
    there is no valid criteria file or it is blank
    """
    def setUp(self):
        clear_test_criteria()
        # Writing a timestamp to a new test criteria file
        test_cf = '{cwd}{file}'.format(cwd=os.getcwd(),
                                       file='/config_TEST'
                                            '/test_transform.criteria')
        with open(test_cf, 'wt') as cf:
            # Using a low number as the timestamp to keep testing easy
            cf.write('10')


class BlankTransformFile(unittest.TestCase):
    """Class to make the setup for test cases with different contexts
    to be logically separated.

    This class sets the context for the test cases that are run when
    there is a valid criteria file that is not blank
    """
    def setUp(self):
        clear_test_criteria()


class TestTransformXMLNoDate(BlankTransformFile):
    """Test cases when the criteria file is blank
    """
    def test_get_new_input(self):
        pass


class TestTransformXMLWithCF(NonBlankFileTransform):
    """Test cases for when the criteria file has a valid timestamp
    """
    def test_get_new_input(self):
        pass
