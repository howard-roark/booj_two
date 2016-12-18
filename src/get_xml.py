import os
import sys
from xml.etree import ElementTree as eT
import requests


def well_formed_xml(response_text):
    """Making sure that the payload of the response is a valid XML.

    If the payload is able to parsed into an ElementTree than that
    is enough to verify that the file is valid XML
    """
    try:
        tree = eT.fromstring(response_text)
    except eT.ParseError as pe:
        print "Downloaded XML is not well formed: {}".format(pe.msg)
    else:
        return tree.tag


def path_is_valid(path):
    """Check if the path exists and is a directory
    """
    return os.path.exists(path) and os.path.isdir(path)


class GetXML:
    def __init__(self, urls=('http://syndication.enterprise.websiteidx'
                             '.com/feeds/BoojCodeTest.xml',)):
        self.urls = urls
        self.response = requests.Response()

    def download_xml(self, retries=2):
        """Function to download the XML file from a feed.

        """
        try:
            for url in self.urls:
                self.response = requests.get(url)

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
            print "Too Many redirects Error({0}): {1}".format(tmr.errno,
                                                              tmr.strerror)
        except requests.RequestException as re:

            print "General Request Error({0}): {1}".format(re.errno,
                                                           re.strerror)
        else:
            if self.response.status_code:
                xml = self.response.content if well_formed_xml(
                    self.response.content) \
                    else None

                self.store_xml(xml)
                return self.response.status_code, xml
            else:
                # TODO Capture stacktrace
                sys.exit(1)

    def store_xml(self, xml, path='./data'):
        if path_is_valid(path):

            pass
