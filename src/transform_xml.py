import os
import csv
import xml.etree.ElementTree as eT
import traceback as tb
import config.constants as constant


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


def requirements_met(listing):
    """This is a helper function to put in any of the
    requirements that need to be met for a listing element to be
    written as a row in the csv.

    Weakness here if there are multiple elements in the listing
    that have duplicate tag names.  For example if ListingDetails
    has a Description tag and BasicDetails has a Descriptin tag as
    well
    """
    reqs_met = True
    for req_tag, req_text in constant.CONST_LISTING_REQUIREMENTS.iteritems():
        for element in listing.iter():
            if element.tag == req_tag:
                """If there is an un-expected duplicate tag being
                queried here than we will not write the row even if
                one of the tags is correct."""
                if req_text not in element.text:
                    reqs_met = False
    return reqs_met


def sort_tree(tree_root, element_tag, sort_by_tag):
    listings = []
    for listing in tree_root.findall(element_tag):
        for tag in listing.iter():
            if tag.tag == sort_by_tag:
                listings.append((tag.text, listing))
    listings.sort()
    children = []
    children[:] = [l[-1] for l in listings]
    tree_root.clear()
    tree_root.extend(children)
    return tree_root


def get_subnode_vals(path, listing, const):
    apps = listing.findall(const)
    app_str = []
    for app in apps:
        app_str.append(app.findtext(path[1]))
    return ','.join(app_str)


def get_row(listing):
    """Once verified that the listing meets the requirements to
    be written to the CSV, this method accepts the listing and
    returns a list of all the fields to be written in the row
    """
    req_fields = []
    for path in constant.CONST_PATHS_TO_FIELDS.sort():
        if path is constant.CONST_APPS_PATH:
            apps = get_subnode_vals(path, listing,
                                    constant.CONST_APPS_PATH)
            req_fields.append(apps)

        elif path is constant.CONST_ROOMS_PATH:
            rooms = get_subnode_vals(path, listing,
                                     constant.CONST_ROOMS)
            req_fields.append(rooms)

        elif path is constant.CONST_DESC_PATH:
            # Trim to 200 chars
            req_fields.append(listing.findtext(path[1])[:201])

        else:
            req_fields.append(listing.findtext(path[1]))

    return req_fields


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
            criteria='/config/transform.criteria',
            data_dir='/data/',
            report_year='2016',
    ):
        self.criteria = '{cwd}{file}'.format(cwd=os.getcwd(),
                                             file=criteria)
        self.data_dir = data_dir
        self.report_year = report_year
        self.new_files = []

    def get_new_input(self):
        """Read the criteria file for the last time the data has been
        transformed.  And look for new input data.

        If the criteria file is blank than run all transformations
        and write latest date of files to the file once complete.
        """
        data_files = os.listdir('{cwd}{path}'.format(cwd=os.getcwd(),
                                                     path=self.data_dir))

        try:
            with open(self.criteria, 'rt') as cf:
                cf_date = cf.readline()[0]
                for f in self.data_dir:
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
            update_criteria_file(self.criteria,
                                 self.data_dir)

        return self.new_files

    def write_csv(self):
        self.get_new_input()

        for filename in self.new_files:
            file_path = '{cwd}{path}{fname}'.format(cwd=os.getcwd(),
                                                    path='/data/',
                                                    fname=filename)
            csv_filename = '{}{}'.format(filename.split('.')[0], '.csv')
            with open(csv_filename, 'w', newline='') as output:
                writer = csv.writer(output)
                tags = sorted(constant.CONST_TABLE_HEADERS,
                              key=lambda h: h[0])
                headers = []
                for tag in tags:
                    headers.append(tag[1])
                writer.writerow(headers)

                listings = sort_tree(eT.parse(file_path))

                for listing in listings:
                    if requirements_met(listing):
                        writer.writerow(get_row(listing))
