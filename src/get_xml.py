import sys
from xml.etree import ElementTree as eT
import requests


def download_xml(
        url='http://syndication.enterprise.websiteidx.com/feeds'
            '/BoojCodeTest.xml',
        retries=2  # TODO need to make sure that retries works right
):
    """Function to download the XML file from a feed.


    Both arguments are optional, default URL is the URl that was
    given with the assignment and default retries is 2 if the
    download fails.

    Function will return a tuple with the response status code and
    the payload if it is a valid XML, else None.
    :type url: str
    :type retries: int
    """
    try:
        response = requests.get(url)

        # If the request does not succeed attempt to re-download
        if response.status_code != 200 and retries:
            download_xml(url, retries - 1)

        xml = response.content if well_formed_xml(response.content) \
            else \
            None

    except requests.ConnectionError as ce:
        print "Connection Error ({0}): {1}".format(ce.errno,
                                                   ce.strerror)
    except requests.HTTPError as he:
        print "HTTP Error({0}): {1}".format(he.errno, he.strerror)
    except requests.Timeout as te:
        print "Timeout Error({0}): {1}".format(te.errno, te.strerror)
    except requests.TooManyRedirects as tmr:
        print "Too Many redirects Error({0}): {1}".format(tmr.errno,
                                                          tmr.strerror)
    except requests.RequestException as re:

        print "General Request Error({0}): {1}".format(re.errno,
                                                       re.strerror)
    else:
        if response.status_code:
            return response.status_code, xml
        else:
            sys.exit(1)


def well_formed_xml(response_text):
    """Making sure that the payload of the response is a valid XML.

    If the payload is able to parsed into an ElementTree than that
    is enough to verify that the file is valid XML
    """
    try:
        xml_tree = eT.fromstring(response_text)
    except eT.ParseError as pe:
        print "Downloaded XML is not well formed: {}".format(pe.msg)
    else:
        return True if xml_tree.tag else False


def store_xml(path='./raw_data'):
    """Once it is verified that the directory exists store the
    downloaded file to the disk for later processing
    """
    return path


def path_exists(path):
    """Check if the path exists and return a boolean
    """
    return path


def make_path(path):
    """If the path does not exist than it needs to be made
    """
    return path
