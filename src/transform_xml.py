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
# Paths to required text fields
CONST_DATE_LISTED_PATH = (CONST_DATE_INDEX, '{}/{}'.format(
    CONST_LISTING_DETAILS, CONST_DATE_LISTED))

CONST_MLSID_PATH = ((CONST_ID_INDEX, '{}/{}'.format(
    CONST_LISTING_DETAILS, CONST_MLS_ID)))

CONST_MLSNAME_PATH = ((CONST_NAME_INDEX, '{}/{}'.format(
        CONST_LISTING_DETAILS, CONST_MLS_NAME)))

CONST_PRICE_PATH = ((CONST_PRICE_INDEX, '{}/{}'.format(
    CONST_LISTING_DETAILS, CONST_PRICE)))

CONST_BEDR_PATH = ((CONST_BEDR_INDEX, '{}/{}'.format(
    CONST_BASIC_DETAILS, CONST_BEDROOMS)))

CONST_BATHR_PATH = ((CONST_BATHR_INDEX, '{}/{}'.format(
    CONST_BASIC_DETAILS, CONST_BATHROOMS)))

CONST_ADDR_PATH = ((CONST_ADDR_INDEX, '{}/{}'.format(
    CONST_LOCATION, CONST_ADDRESS)))

CONST_ROOMS_PATH = ((CONST_ROOMS_INDEX, '{}/{}'.format(
    CONST_RICH_DETAILS, CONST_ROOMS)))

CONST_APPS_PATH = ((CONST_APPS_INDEX, '{}/{}'.format(
    CONST_RICH_DETAILS, CONST_APPLIANCES)))

CONST_DESC_PATH = ((CONST_DESC_INDEX, '{}/{}'.format(
    CONST_BASIC_DETAILS, CONST_DESC)))

CONST_PATHS_TO_FIELDS = (CONST_DATE_LISTED_PATH, CONST_MLSID_PATH,
                         CONST_MLSNAME_PATH, CONST_PRICE_PATH,
                         CONST_BEDR_PATH, CONST_BATHR_PATH,
                         CONST_ADDR_PATH, CONST_ROOMS_PATH,
                         CONST_APPS_PATH, CONST_DESC_PATH)
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


def sort_tree(tree):
    listings = tree.findall(CONST_DATE_LISTED)
    element_tuples = []
    for listing in listings:
        find_date_listed = '{}/{}'.format(CONST_LISTING,
                                          CONST_LISTING_DETAILS)
        key = listing.findtext(find_date_listed)
        element_tuples.append((key, listing))

    element_tuples.sort()
    listings[:] = [element[-1] for element in listings]
    return tree


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

            listings = sort_tree(eT.parse(file_path))

            req_fields = []
            for listing in listings:
                if requirements_met(listing):
                    for path in CONST_PATHS_TO_FIELDS.sort():
                        if path is CONST_APPS_PATH:
                            # Comma seperated nodes in csv cell
                            pass
                        elif path is CONST_DESC_PATH:
                            # Same as apps
                            pass
                        elif path is CONST_DESC_PATH:
                            # Trim to 200 chars
                            pass
                        else:
                            req_fields.append(listing.findtext(path[1]))

                    writer.writerow(req_fields)
