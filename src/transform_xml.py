import os


class TransformXML:
    """This class will be responsible for finding new data to be
    transformed, parsing out the required fields and transforming
    them to the required format.

    The criteria file located in the config folder will hold the date
    of the 'oldest' file in the input so that each time this class is
    run every file will not need to be transformed.

    But if the need every came that the entire directory needed to be
    re-transformed than remove the date from the criteria file.  Or
    if looking to go back in time, but not all, change the criteria
    file date to the earliest date of files being queried.
    """

    def __init__(self, input_format='xml',
                 output_format='csv',
                 criteria='/config/transform.criteria'):
        self.input_format = input_format
        self.output_format = output_format
        self.criteria = criteria

    def get_new_input(self):
        """Read the criteria file for the last time the data has been
        transformed.  And look for new input data.

        If the criteria file is blank than run all transformations
        and write latest date of files to the file once complete.
        """
        criteria_file = '{cwd}{file}'.format(cwd=os.getcwd(),
                                             file=self.criteria)
        with open(criteria_file) as cf:
            try:
                cf_date = cf.readline()[0]
            except IOError as ioe:
                print 'Not able to read the file: {}\n\tIOE: {}'.format(
                    criteria_file, ioe.message)
            except IndexError:
                # TODO criteria file is empty so process all files
                pass
