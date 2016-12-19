import os
import csv
import xml.etree.ElementTree as eT
import traceback as tb

# Required fields
CONST_LISTING = 'Listing'
CONST_LISTING_DETAILS = 'ListingDetails'
CONST_LOCATION = 'Location'
CONST_BASIC_DETAILS = 'BasicDetails'
CONST_RICH_DETAILS = 'RichDetails'
# Table headers
CONST_DATE_LISTED = 'DateListed'
CONST_MLS_ID = 'MlsId'
CONST_MLS_NAME = 'MlsName'
CONST_PRICE = 'Price'
CONST_BEDROOMS = 'Bedrooms'
CONST_BATHROOMS = 'Bathrooms'
CONST_ADDRESS = 'StreetAddress'
CONST_ROOMS = 'Rooms'
CONST_APPLIANCES = 'Appliances'
CONST_DESC = 'Description'
CONST_TABLE_HEADERS = (CONST_DATE_LISTED, CONST_MLS_ID,
                       CONST_MLS_NAME, CONST_PRICE, CONST_BEDROOMS,
                       CONST_BATHROOMS, CONST_ADDRESS, CONST_ROOMS,
                       CONST_APPLIANCES, CONST_DESC)


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


class TransformXML(object):
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
            criteria='/config/transform.criteria',
            data_dir='/data/',
    ):
        self.criteria = criteria
        self.data_dir = data_dir
        self.new_files = []

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

        try:
            with open(criteria_file, 'rt') as cf:
                cf_date = cf.readline()[0]
                for f in data_files:
                    ts = f.split('_')[0]
                    if ts > cf_date:
                        self.new_files.append(f)

        except IOError:
            # Criteria file is not present, process all files in data
            # directory
            for f in data_files:
                self.new_files.append(f)
        except IndexError:
            print 'IndexError:\n\t{}'.format(tb.print_tb())
        else:
            update_criteria_file(criteria_file, data_files)

        return self.new_files

    def write_csv(self, filename):
        """Method that will reduce the elements that need to be
        transformed based on the requirements passed in.
        """
        file_path = '{cwd}{path}{fname}'.format(cwd=os.getcwd(),
                                                path='/data/',
                                                fname=filename)
        csv_filename = '{}{}'.format(file_path.split('.')[0], '.csv')
        csv_writer = csv.writer(csv_filename)

        tree = eT.parse(file_path)
        root = tree.getroot()

        table_header = True
        for member in root.findall(CONST_LISTING):
            date_listed = member.find(CONST_DATE_LISTED).text
            desc = member.find(CONST_DESC).text
            if '2016' in date_listed and 'and' in desc:
                listing = []
                if table_header:
                    table_header = False
                    csv_writer.writerow(CONST_TABLE_HEADERS)

                for header in CONST_TABLE_HEADERS:
                    listing.append(member.find(header).text)

                csv_writer.writerow(listing)

if __name__ == 'main':
    t_xml = TransformXML
    for i in t_xml.get_new_input():
        t_xml.write_csv(i)
