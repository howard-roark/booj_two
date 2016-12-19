import os
import traceback as tb


def update_criteria_file(criteria_file, data_files):
    """Sort a list of the timestamps from the data files and write
    the latest one to the criteria file
    """
    timestamps = []
    for f in data_files:
        timestamps.append(int(f.split('_')[0]))

    timestamps = sorted(timestamps, key=int)
    with open(criteria_file, 'wt') as cf:
        cf.write(str(timestamps[-1]))


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

    def __init__(
            self,
            input_format='xml',
            output_format='csv',
            criteria='/config/transform.criteria',
            data_dir='/data/',
            required_fields=('MlsId', 'MlsName', 'DateListed',
                             'StreetAddress', 'Price',
                             'Bedrooms', 'Bathrooms',
                             'Appliances', 'Rooms', 'Description'),
            requirements={'DateListed': '2016',
                          'Description': 'and'}
    ):
        self.input_format = input_format
        self.output_format = output_format
        self.criteria = criteria
        self.data_dir = data_dir
        self.required_fields = required_fields
        self.requirements = requirements

    def get_new_input(self):
        """Read the criteria file for the last time the data has been
        transformed.  And look for new input data.

        If the criteria file is blank than run all transformations
        and write latest date of files to the file once complete.
        """
        criteria_file = '{cwd}{file}'.format(cwd=os.getcwd(),
                                             file=self.criteria)
        data_files = \
            os.listdir('{cwd}{path}'.format(cwd=os.getcwd(),
                                            path=self.data_dir))

        new_files = []
        try:
            with open(criteria_file, 'rt') as cf:
                cf_date = cf.readline()[0]
                for f in data_files:
                    ts = f.split('_')[0]
                    if ts > cf_date:
                        new_files.append(f)

        except IOError:
            # Criteria file is not present, process all files in data
            # directory
            for f in data_files:
                new_files.append(f)
        except IndexError:
            print 'IndexError:\n\t{}'.format(tb.print_tb())
        else:
            update_criteria_file(criteria_file, data_files)

        return new_files

    def reduce_elements(self):
        """Method that will reduce the elements that need to be
        transformed based on the requirements passed in.

        Requirements are in the form of a dictionary where the key
        will be the XML element to be examined and
        """
        pass
