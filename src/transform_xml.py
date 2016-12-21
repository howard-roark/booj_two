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
# Relevant children
CONST_RELEVANT_CHILDREN = (CONST_LISTING_DETAILS, CONST_RICH_DETAILS,
                           CONST_LOCATION, CONST_BASIC_DETAILS)
# Indices for table headers
CONST_DATE_INDEX = 0
CONST_ID_INDEX = 1
CONST_NAME_INDEX = 2
CONST_PRICE_INDEX = 3
CONST_BEDR_INDEX = 4
CONST_BATHR_INDEX = 5
CONST_ADDR_INDEX = 6
CONST_ROOMS_INDEX = 7
CONST_APPS_INDEX = 8
CONST_DESC_INDEX = 9

# Table headers
CONST_DATE_LISTED = (CONST_DATE_INDEX, 'DateListed')
CONST_MLS_ID = (CONST_ID_INDEX, 'MlsId')
CONST_MLS_NAME = (CONST_NAME_INDEX, 'MlsName')
CONST_PRICE = (CONST_PRICE_INDEX, 'Price')
CONST_BEDROOMS = (CONST_BEDR_INDEX, 'Bedrooms')
CONST_BATHROOMS = (CONST_BATHR_INDEX, 'Bathrooms')
CONST_ADDRESS = (CONST_ADDR_INDEX, 'StreetAddress')
CONST_ROOMS = (CONST_ROOMS_INDEX, 'Rooms')
CONST_APPLIANCES = (CONST_APPS_INDEX, 'Appliances')
CONST_DESC = (CONST_DESC_INDEX, 'Description')
CONST_TABLE_HEADERS = (CONST_DATE_LISTED[1], CONST_MLS_ID[1],
                       CONST_MLS_NAME[1], CONST_PRICE[1],
                       CONST_BEDROOMS[1],
                       CONST_BATHROOMS[1], CONST_ADDRESS[1],
                       CONST_ROOMS[1],
                       CONST_APPLIANCES[1], CONST_DESC)
# Dict for holding listing requirements, key is Element / Tag and
# value is the condition that needs to be met for the listing to be
# written to the CSV.

CONST_LISTING_REQUIREMENTS = {CONST_DATE_LISTED: '>2016-',
                              CONST_DESC: ' and '}


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


def requirements_met(member):
    """This is a helper function to put in any of the
    requirements that need to be met for a listing element to be
    written as a row in the csv"""
    for tag, req in CONST_LISTING_REQUIREMENTS.iteritems():
        if member.tag == tag[1]:
            return req in member.text


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
            report_year='2016',
    ):
        self.criteria = criteria
        self.data_dir = data_dir
        self.report_year = report_year
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
        with open(csv_filename, 'w', newline='') as output:
            writer = csv.writer(output)
            tags = sorted(CONST_TABLE_HEADERS, key=lambda h: h[0])
            headers = []
            for tag in tags:
                headers.append(tag[1])
            writer.writerow(headers)
        #
        # tree = eT.parse(file_path)
        # root = tree.getroot()
        #
        # table_header = True
        # for member in root.findall(CONST_LISTING):
        #     date_listed = member.find(CONST_DATE_LISTED).text
        #     if self.report_year in date_listed:
        #         if requirements_met(member):
        #             listing = []
        #             if table_header:
        #                 table_header = False
        #                 writer.writerow(CONST_TABLE_HEADERS)
        #
        #             for header in CONST_TABLE_HEADERS:
        #                 listing.append(member.find(header).text)
        #
        #             writer.writerow(listing)


if __name__ == 'main':
    t_xml = TransformXML
    for i in t_xml.get_new_input():
        t_xml.write_csv(i)
