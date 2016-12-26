import os
import sys
import time
from xml.etree import ElementTree as eT
import requests


def well_formed_xml(response_text):
    """Making sure that the payload of the response is a valid XML.

    If the payload is able to parsed into an ElementTree than that
    is enough to verify that the file is valid XML
    :param response_text: content from the response, expected to be
    an XML
    :return: true if the content can be parsed at an XML
    """
    try:
        tree = eT.fromstring(response_text)
    except eT.ParseError as pe:
        print "Downloaded XML is not well formed: {}".format(pe.msg)
    else:
        return tree.tag


def path_is_valid(directory):
    """Check if the path exists and is a directory
    :param directory: the expected path passed in will be relative to
    the project
    :return: true if path exists and is a directory
    """
    path = '{cwd}{dir}'.format(cwd=os.getcwd(), dir=directory)
    if not os.path.exists(path) and not os.path.isdir(path):
        os.makedirs(path)
    return os.path.exists(path) and os.path.isdir(path)


class GetXML:
    """GetXML class will be used to download and store XMLs based on
    the URLs passed in when the object is created.  By default there
    is only one URL to download an XML from.

    Before the XML is written to a file on disk it is verified to be
    syntactically correct XML.  If it is not that it will not be
    written to disk and an error message will be printed to the
    console (until more formal logging is setup)

    When storing the files being downloaded there will be a check to
    make sure that the directories are present and valid, if they are
    not they will be created.
    """

    def __init__(self, url='http://syndication.enterprise.websiteidx'
                           '.com/feeds/BoojCodeTest.xml'):
        self.url = url
        self.response = requests.Response()
        self.data_dir = '/data/'

    def download_xml(self, retries=2):
        """Function to download the XML file from a feed.
        :param retries: How many times to retry downloading the file
        :return: the status code and content of the request

        """
        try:
            self.response = requests.get(self.url)

            # Attempt the download until successful
            if self.response.status_code != 200 and retries:
                self.download_xml(retries - 1)

        except requests.ConnectionError as ce:
            print "Connection Error ({0}): {1}".format(ce.errno,
                                                       ce.strerror)
        except requests.HTTPError as he:
            print "HTTP Error({0}): {1}".format(he.errno, he.strerror)
        except requests.Timeout as te:
            print "Timeout Error({0}): {1}".format(te.errno,
                                                   te.strerror)
        except requests.TooManyRedirects as tmr:
            print "Too Many redirects Error({0}): {1}".format(
                tmr.errno, tmr.strerror)
        except requests.RequestException as re:

            print "General Request Error({0}): {1}".format(re.errno,
                                                           re.strerror)
        else:
            if self.response.status_code:
                xml = self.response.content if well_formed_xml(
                    self.response.content) \
                    else None

                file_name = self.url.split('/')[-1]
                self.store_xml(xml, file_name)
                return self.response.status_code, xml
            else:
                # TODO Capture stacktrace
                sys.exit(1)

    def store_xml(self, xml, filename):
        """Once determined that the path to store the file is valid
        and the XML is valid than insert a millisecond-from-epoch
        timestamp to uniquely identify each downloaded file
        """
        if path_is_valid(self.data_dir) and xml:
            millis = str(int(round(time.time() * 1000)))
            stored_filename = '{timestamp}_{name}'.format(
                timestamp=millis,
                name=filename)
            file_path = '{cwd}{dir}{name}'.format(cwd=os.getcwd(),
                                                  dir=self.data_dir,
                                                  name=stored_filename)
            with open(file_path, 'wt') as f:
                f.write(xml)
        else:
            print 'XML downloaded was empty: {fn}'.format(fn=filename)
